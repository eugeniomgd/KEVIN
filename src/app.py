from pathlib import Path
import streamlit as st
from src.models.rag_model import RAGModel
from dotenv import load_dotenv
import os
import base64
from PIL import Image

class OperationsApp:
    def __init__(self):
        # Configurar rutas
        self.base_dir = Path(__file__).resolve().parent.parent
        self.data_dir = self.base_dir / "data" / "raw"
        self.data_dir.mkdir(parents=True, exist_ok=True)
        
        # Inicializar estado de la sesión
        if 'messages' not in st.session_state:
            st.session_state.messages = []
        if 'rag_model' not in st.session_state:
            st.session_state.rag_model = RAGModel()
            st.session_state.initialized = False
        
        # Verificar si el modelo está realmente inicializado
        if not hasattr(st.session_state.rag_model, 'vectorstore'):
            st.session_state.initialized = False

    def handle_user_input(self):
        """Maneja la entrada del usuario"""
        if prompt := st.chat_input("¿Qué quieres saber sobre los documentos cargados?"):
            if not st.session_state.initialized:
                st.error("Por favor, inicializa el modelo primero.")
                return

            # Añadir mensaje del usuario al historial
            st.session_state.messages.append({"role": "user", "content": prompt})
            
            try:
                # Generar respuesta
                response = st.session_state.rag_model.query(prompt)
                
                # Añadir respuesta al historial
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": response["answer"],
                    "sources": response.get("sources", {}),
                    "metrics": response.get("metrics", {})
                })
                
            except Exception as e:
                st.error(f"Error al generar respuesta: {str(e)}")

    def setup_sidebar(self):
        """Configura la barra lateral"""
        with st.sidebar:
            st.header("Configuración")
            
            # Sección de carga de documentos
            st.subheader("Cargar Documentos")
            uploaded_files = st.file_uploader(
                "Sube tus documentos PDF o TXT",
                type=["pdf", "txt"],
                accept_multiple_files=True
            )

            if uploaded_files:
                for uploaded_file in uploaded_files:
                    file_path = self.data_dir / uploaded_file.name
                    with open(file_path, "wb") as f:
                        f.write(uploaded_file.getvalue())
                    st.success(f"Archivo guardado: {uploaded_file.name}")

            # Mostrar documentos actuales
            current_files = list(self.data_dir.glob("*.*"))
            if current_files:
                st.write("Documentos cargados:")
                for file in current_files:
                    st.write(f"📄 {file.name}")
                
                # Botón de inicialización
                if st.button("Inicializar/Reinicializar Modelo"):
                    with st.spinner("Inicializando modelo..."):
                        try:
                            success = st.session_state.rag_model.initialize("data/raw")
                            if success and hasattr(st.session_state.rag_model, 'vectorstore'):
                                st.session_state.initialized = True
                                st.success("✅ Modelo inicializado correctamente")
                            else:
                                st.session_state.initialized = False
                                st.error("❌ Error al inicializar el modelo")
                        except Exception as e:
                            st.session_state.initialized = False
                            st.error(f"Error: {str(e)}")

            # Mostrar estado y métricas
            st.divider()
            st.subheader("📊 Métricas del Modelo")
            
            # Verificación más estricta del estado del modelo
            is_initialized = (hasattr(st.session_state.rag_model, 'vectorstore') and 
                            hasattr(st.session_state.rag_model, 'qa_chain') and
                            st.session_state.initialized)
            
            # Estado del modelo
            st.write("Estado:", "✅ Inicializado" if is_initialized else "❌ No inicializado")
            
            # Métricas de tokens solo si el modelo está realmente inicializado
            if is_initialized:
                total_tokens = st.session_state.rag_model.total_tokens
                cost_per_1k = 0.03
                total_cost = (total_tokens / 1000) * cost_per_1k
                
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Total Tokens", f"{total_tokens:,}")
                with col2:
                    st.metric("Costo Est.", f"${total_cost:.2f}")
                
                # Botón para reiniciar contadores
                if st.button("Reiniciar Contadores"):
                    st.session_state.rag_model.total_tokens = 0
                    st.rerun()
            else:
                # Si no está inicializado, mostrar valores en cero
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Total Tokens", "0")
                with col2:
                    st.metric("Costo Est.", "$0.00")

    def setup_header(self):
        """Configura la cabecera con logo y título"""
        # Crear contenedor para la cabecera
        header_container = st.container()
        
        with header_container:
            col1, col2 = st.columns([1, 4])
            
            # Logo en la primera columna
            with col1:
                logo_path = self.base_dir / "assets" / "logo.png"
                if logo_path.exists():
                    st.image(str(logo_path), width=100)
            
            # Título y subtítulo en la segunda columna
            with col2:
                st.markdown("""
                    <h1 style='margin-bottom: 0px; padding-bottom: 0px;'>Kevin</h1>
                    <p style='color: #666; font-size: 1.1em; margin-top: 0px;'>Tu asistente para el analisis de documentos</p>
                    """, 
                    unsafe_allow_html=True
                )
        
        # Añadir un separador después de la cabecera
        st.divider()

    def run(self):
        """Ejecuta la aplicación"""
        self.setup_header()  # Llamar al nuevo método de cabecera
        self.setup_sidebar()
        
        # Mostrar mensajes existentes
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
                
                # Mostrar detalles solo para mensajes del asistente
                if message["role"] == "assistant" and "metrics" in message:
                    with st.expander("📚 Detalles"):
                        # Fuentes internas
                        if "internal" in message.get("sources", {}):
                            st.write("📄 Documentos internos:")
                            for doc in message["sources"]["internal"]:
                                st.markdown(f"**Fuente:** {doc['source']}")
                                st.markdown(f"```\n{doc['content'][:200]}...\n```")
                        
                        # Fuentes web
                        if "web" in message.get("sources", {}):
                            st.write("🌐 Información de internet:")
                            st.markdown(f"```\n{message['sources']['web'][:200]}...\n```")
                        
                        # Métricas
                        st.subheader("📊 Métricas")
                        metrics = message["metrics"]
                        col1, col2 = st.columns(2)
                        with col1:
                            st.write(f"⏱️ Tiempo: {metrics['time']}")
                            st.write(f"🕒 Timestamp: {metrics['timestamp']}")
                        with col2:
                            st.write(f"🔤 Tokens: {metrics['tokens']['total']}")
                            st.write(f"💰 Costo: {metrics['cost']}")

        # Procesar nueva entrada
        if prompt := st.chat_input("¿Qué quieres saber sobre las operaciones?"):
            if not st.session_state.initialized:
                st.error("Por favor, inicializa el modelo primero.")
                return

            # Mostrar mensaje del usuario
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            # Generar y mostrar respuesta
            with st.chat_message("assistant"):
                try:
                    response = st.session_state.rag_model.query(prompt)
                    st.markdown(response["answer"])
                    
                    # Mostrar detalles de la respuesta actual
                    with st.expander("📚 Detalles"):
                        # Fuentes internas
                        if "internal" in response.get("sources", {}):
                            st.write("📄 Documentos internos:")
                            for doc in response["sources"]["internal"]:
                                st.markdown(f"**Fuente:** {doc['source']}")
                                st.markdown(f"```\n{doc['content'][:200]}...\n```")
                        
                        # Fuentes web
                        if "web" in response.get("sources", {}):
                            st.write("🌐 Información de internet:")
                            st.markdown(f"```\n{response['sources']['web'][:200]}...\n```")
                        
                        # Métricas
                        st.subheader("📊 Métricas")
                        metrics = response["metrics"]
                        col1, col2 = st.columns(2)
                        with col1:
                            st.write(f"⏱️ Tiempo: {metrics['time']}")
                            st.write(f"🕒 Timestamp: {metrics['timestamp']}")
                        with col2:
                            st.write(f"🔤 Tokens: {metrics['tokens']['total']}")
                            st.write(f"💰 Costo: {metrics['cost']}")
                    
                    # Guardar respuesta en el historial
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": response["answer"],
                        "sources": response.get("sources", {}),
                        "metrics": response.get("metrics", {})
                    })
                    
                except Exception as e:
                    st.error(f"Error al generar respuesta: {str(e)}")

if __name__ == "__main__":
    app = OperationsApp()
    app.run()