import streamlit as st
from pathlib import Path
import os
import shutil
from src.core.logger import Logger
from src.core.config import settings

class Sidebar:
    def __init__(self):
        """Inicializa el componente de la barra lateral"""
        self.logger = Logger()

    def render(self, rag_model):
        """Renderiza la barra lateral con sus funcionalidades"""
        with st.sidebar:
            # Logo y título
            st.image("assets/logo.png", width=250)
            st.markdown("<p style='text-align: left; font-style: italic; color: #31333F; margin-top: -15px;'>Tu asistente de análisis de documentos</p>", unsafe_allow_html=True)
            
            # Sección de documentos
            st.markdown("<h2 style='text-align: left; color: #31333F;'>📁 Documentos cargados</h2>", unsafe_allow_html=True)
            
            # Mostrar documentos actuales
            self._show_current_documents()
            
            # Subida de nuevos documentos
            uploaded_files = st.file_uploader(
                label="",
                type=["pdf", "txt"],
                accept_multiple_files=True,
                key="doc_uploader"
            )

            st.divider()

            # Inicializar el modelo

            # Estado del modelo
            is_initialized = (hasattr(rag_model, 'vectorstore') and 
                            hasattr(rag_model, 'qa_chain') and
                            st.session_state.initialized)
            
            st.write("Estado:", "✅ Inicializado" if is_initialized else "❌ No inicializado")

            # Botón para inicializar/reinicializar
            col1, col2 = st.columns([4,1])
            with col1:
                initialize_button = st.button(
                    "Inicializar Modelo",
                    type="primary",
                    key="init_button",
                    use_container_width=True
                )
            if initialize_button:
                self._initialize_model(uploaded_files, rag_model)
            
            # Mostrar estado y métricas
            st.subheader("📊 Métricas del Modelo")

            # Métricas de tokens usando TokenCounter
            if is_initialized:
                metrics = rag_model.token_counter.get_metrics()
                
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Total Tokens", f"{metrics['total_tokens']:,}")
                with col2:
                    st.metric("Costo Est.", f"${metrics['total_cost']:.2f}")
                
                # Botón para reiniciar contadores
                if st.button("Reiniciar Contadores"):
                    rag_model.token_counter.reset()
                    st.rerun()

    def _show_current_documents(self):
        """Muestra y permite gestionar los documentos actuales"""
        raw_docs_path = settings.RAW_DATA_DIR
        if not raw_docs_path.exists():
            raw_docs_path.mkdir(parents=True, exist_ok=True)
            
        docs = list(raw_docs_path.glob("*.*"))
        
        if docs:
            for doc in docs:
                col1, col2 = st.columns([3,1])
                with col1:
                    st.text(f"• {doc.name}")
                with col2:
                    if st.button("🗑️", key=f"delete_{doc.name}", help=f"Eliminar {doc.name}"):
                        self._delete_document(doc)
                        st.rerun()
        else:
            st.info("No hay documentos cargados")

    def _delete_document(self, doc_path: Path):
        """Elimina un documento y sus archivos procesados relacionados"""
        try:
            # Eliminar archivo original
            if doc_path.exists():
                os.remove(doc_path)
                self.logger.info(f"Documento eliminado: {doc_path.name}")

            # Eliminar archivos procesados relacionados
            processed_path = settings.PROCESSED_DATA_DIR / doc_path.name
            if processed_path.exists():
                os.remove(processed_path)
                self.logger.info(f"Archivo procesado eliminado: {processed_path.name}")

            # Eliminar índices o cachés relacionados si existen
            index_path = settings.PROCESSED_DATA_DIR / f"{doc_path.stem}_index"
            if index_path.exists():
                shutil.rmtree(index_path)
                self.logger.info(f"Índice eliminado: {index_path.name}")

            st.success(f"Documento {doc_path.name} eliminado correctamente")
            
        except Exception as e:
            self.logger.error(f"Error eliminando documento {doc_path.name}: {str(e)}")
            st.error(f"Error al eliminar el documento: {str(e)}")

    def _initialize_model(self, uploaded_files, rag_model):
        """Inicializa o reinicializa el modelo con los documentos"""
        try:
            # Procesar archivos subidos
            if uploaded_files:
                raw_docs_path = settings.RAW_DATA_DIR
                raw_docs_path.mkdir(parents=True, exist_ok=True)
                
                for file in uploaded_files:
                    file_path = raw_docs_path / file.name
                    with open(file_path, "wb") as f:
                        f.write(file.getvalue())
                    self.logger.info(f"Documento guardado: {file.name}")

            # Inicializar modelo
            with st.spinner("Inicializando modelo..."):
                if rag_model.initialize(str(settings.RAW_DATA_DIR)):
                    st.session_state.initialized = True
                    st.success("¡Modelo inicializado correctamente! 🚀")
                    self.logger.info("Modelo inicializado correctamente")
                else:
                    st.error("Error al inicializar el modelo")
                    self.logger.error("Error en inicialización del modelo")

        except Exception as e:
            st.error(f"Error: {str(e)}")
            self.logger.error(f"Error en inicialización: {str(e)}")

    def _show_model_info(self):
        """Muestra información del estado del modelo"""
        if st.session_state.get('initialized', False):
            st.success("Modelo activo")
        else:
            st.warning("Modelo no inicializado")