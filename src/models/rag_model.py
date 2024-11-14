from pathlib import Path
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import AzureOpenAIEmbeddings, AzureChatOpenAI
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain_community.tools import DuckDuckGoSearchRun
import time
from datetime import datetime
import requests
from src.core.config import settings
from src.core.logger import Logger
from src.utils.document_processor import DocumentProcessor
from src.utils.token_counter import TokenCounter
from src.prompts.qa_prompts import QA_PROMPT

class RAGModel:
    def __init__(self):
        """Inicializa el modelo RAG"""
        self.logger = Logger()
        self.doc_processor = DocumentProcessor()
        self.token_counter = TokenCounter()
        self.total_tokens = 0
        self.web_search_enabled = True
        
        # Configuración del modelo
        self.chunk_size = settings.CHUNK_SIZE
        self.chunk_overlap = settings.CHUNK_OVERLAP
        self.temperature = settings.TEMPERATURE
        self.max_tokens = settings.MAX_TOKENS

    def _check_internet_connection(self) -> bool:
        """Verifica la conexión a internet"""
        try:
            # Intenta conectar a un servicio confiable
            requests.get("https://www.google.com", timeout=5)
            return True
        except requests.RequestException:
            self.logger.warning("No se detectó conexión a internet")
            return False

    def _get_web_results(self, question: str) -> tuple[str, int]:
        """
        Obtiene resultados de búsqueda web.
        
        Returns:
            tuple: (resultados, número_de_tokens)
        """
        if not self.web_search_enabled:
            return "Búsqueda web deshabilitada.", 0

        if not self._check_internet_connection():
            return "No hay conexión a internet disponible.", 0

        try:
            # Configurar timeout y número de resultados
            self.search_tool = DuckDuckGoSearchRun(
                max_results=3,
                timeout=10
            )
            results = self.search_tool.run(question)
            return results, self.token_counter.count_tokens(results)
            
        except Exception as e:
            self.logger.warning(f"Error en búsqueda web: {str(e)}")
            return f"Error en búsqueda web: {str(e)}", 0

    def initialize(self, documents_path: str) -> bool:
        """Inicializa el modelo RAG"""
        try:
            # Configurar LLM
            self.llm = AzureChatOpenAI(
                azure_deployment=settings.CHAT_DEPLOYMENT,
                openai_api_version=settings.API_VERSION,
                azure_endpoint=settings.AZURE_OPENAI_ENDPOINT,
                api_key=settings.AZURE_OPENAI_API_KEY,
                temperature=self.temperature,
                max_tokens=self.max_tokens
            )
            
            # Configurar embeddings
            embeddings = AzureOpenAIEmbeddings(
                azure_deployment=settings.EMBEDDING_DEPLOYMENT,
                openai_api_version=settings.EMBEDDING_API_VERSION,
                azure_endpoint=settings.AZURE_OPENAI_ENDPOINT,
                openai_api_key=settings.AZURE_OPENAI_API_KEY
            )
            
            # Procesar documentos
            documents = []
            docs_path = Path(documents_path)
            for file_path in docs_path.glob('**/*.*'):
                if file_path.suffix.lower() in ['.pdf', '.txt']:
                    docs = self.doc_processor.process_file(str(file_path))
                    documents.extend(docs)
            
            if not documents:
                raise ValueError("No se pudieron cargar documentos")
            
            # Dividir documentos
            splitter = RecursiveCharacterTextSplitter(
                chunk_size=self.chunk_size,
                chunk_overlap=self.chunk_overlap
            )
            texts = splitter.split_documents(documents)
            
            # Crear vectorstore
            self.vectorstore = FAISS.from_documents(
                documents=texts,
                embedding=embeddings
            )
            
            # Configurar búsqueda web
            self.search_tool = DuckDuckGoSearchRun()
            
            # Configurar QA chain
            self.qa_chain = RetrievalQA.from_chain_type(
                llm=self.llm,
                chain_type="stuff",
                retriever=self.vectorstore.as_retriever(search_kwargs={"k": 3}),
                return_source_documents=True,
                chain_type_kwargs={"prompt": QA_PROMPT}
            )
            
            self.logger.info("Modelo inicializado correctamente")
            return True
            
        except Exception as e:
            self.logger.error(f"Error al inicializar el modelo: {str(e)}")
            raise

    def query(self, question: str) -> dict:
        """Procesa una pregunta y retorna la respuesta con métricas"""
        try:
            start_time = time.time()
            
            # Contar tokens de la pregunta
            question_tokens = self.token_counter.count_tokens(question)
            
            # Búsqueda en documentos internos
            docs = self.vectorstore.similarity_search(question, k=3)
            internal_context = "\n".join([doc.page_content for doc in docs])
            context_tokens = self.token_counter.count_tokens(internal_context)
            
            # Búsqueda web
            web_results, web_tokens = self._get_web_results(question)
            
            # Combinar contexto
            full_context = f"""
            Contexto de documentos internos:
            {internal_context}
            
            Información de internet:
            {web_results}
            """
            
            # Generar respuesta
            response = self.qa_chain({"query": question})
            response_tokens = self.token_counter.count_tokens(response["result"])
            
            # Actualizar métricas
            execution_time = time.time() - start_time
            total_query_tokens = question_tokens + context_tokens + web_tokens + response_tokens
            self.total_tokens += total_query_tokens
            
            return {
                "answer": response["result"],
                "sources": {
                    "internal": [
                        {
                            "content": doc.page_content,
                            "source": doc.metadata.get("source", "Desconocido")
                        } for doc in docs
                    ],
                    "web": web_results
                },
                "metrics": {
                    "time": f"{execution_time:.2f}s",
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "tokens": {
                        "question": question_tokens,
                        "context": context_tokens,
                        "web": web_tokens,
                        "response": response_tokens,
                        "total": total_query_tokens,
                        "accumulated": self.total_tokens
                    },
                    "cost": f"${self.token_counter.calculate_cost(total_query_tokens):.4f}"
                }
            }
            
        except Exception as e:
            self.logger.error(f"Error en consulta: {str(e)}")
            raise