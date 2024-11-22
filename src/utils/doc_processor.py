from langchain_community.document_loaders import DirectoryLoader, TextLoader, PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import os

class DocProcessor:
    def __init__(self):
        """Inicializa el procesador de documentos"""
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len,
        )

    def process_file(self, file_path: str):
        """Procesa un archivo individual
        
        Args:
            file_path (str): Ruta al archivo
            
        Returns:
            list: Lista de documentos procesados
        """
        try:
            # Determinar el tipo de archivo
            if file_path.endswith('.txt'):
                loader = TextLoader(file_path)
            elif file_path.endswith('.pdf'):
                loader = PyPDFLoader(file_path)
            else:
                raise ValueError(f"Tipo de archivo no soportado: {file_path}")
            
            # Cargar y dividir el documento
            documents = loader.load()
            return self.text_splitter.split_documents(documents)
            
        except Exception as e:
            print(f"Error processing file {file_path}: {str(e)}")
            return []

    def load_documents(self, directory: str):
        """Carga documentos desde un directorio"""
        loaders = {
            '.txt': (DirectoryLoader(directory, glob="**/*.txt", loader_cls=TextLoader)),
            '.pdf': (DirectoryLoader(directory, glob="**/*.pdf", loader_cls=PyPDFLoader))
        }
        
        documents = []
        for ext, loader in loaders.items():
            if any(f.endswith(ext) for f in os.listdir(directory)):
                try:
                    docs = loader.load()
                    documents.extend(docs)
                except Exception as e:
                    print(f"Error loading {ext} files: {str(e)}")
        
        if documents:
            return self.text_splitter.split_documents(documents)
        return []

    def process_documents(self, directory: str):
        """Procesa los documentos de un directorio"""
        return self.load_documents(directory) 