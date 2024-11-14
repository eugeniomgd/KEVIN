import streamlit as st
from typing import Dict, List
from src.core.logger import Logger

class Chat:
    """Componente de chat para la interfaz de usuario"""
    
    def __init__(self):
        """Inicializa el componente de chat"""
        self.logger = Logger()

    def render_message(self, message: Dict):
        """Renderiza un mensaje individual con sus detalles"""
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            
            if message["role"] == "assistant" and "metrics" in message:
                with st.expander("📚 Detalles"):
                    self._render_sources(message.get("sources", {}))
                    self._render_metrics(message.get("metrics", {}))

    def _render_sources(self, sources: Dict):
        """Renderiza las fuentes de información"""
        if "internal" in sources:
            st.write("📄 Documentos internos:")
            for doc in sources["internal"]:
                st.markdown(f"**Fuente:** {doc['source']}")
                st.markdown(f"```\n{doc['content'][:200]}...\n```")
        
        if "web" in sources:
            st.write("🌐 Información de internet:")
            st.markdown(f"```\n{sources['web'][:200]}...\n```")

    def _render_metrics(self, metrics: Dict):
        """Renderiza las métricas de la respuesta"""
        st.subheader("📊 Métricas")
        col1, col2 = st.columns(2)
        with col1:
            st.write(f"⏱️ Tiempo: {metrics['time']}")
            st.write(f"🕒 Timestamp: {metrics['timestamp']}")
        with col2:
            st.write(f"🔤 Tokens: {metrics['tokens']['total']}")
            st.write(f"💰 Costo: {metrics['cost']}")

    def handle_input(self, rag_model) -> None:
        """Maneja la entrada del usuario y genera la respuesta"""
        if prompt := st.chat_input("¿Qué quieres saber sobre los documentos cargados?"):
            if not st.session_state.initialized:
                st.error("Por favor, inicializa el modelo primero.")
                return

            # Añadir mensaje del usuario al historial
            st.session_state.messages.append({"role": "user", "content": prompt})
            self.render_message(st.session_state.messages[-1])

            try:
                # Generar respuesta
                response = rag_model.query(prompt)
                
                # Crear mensaje de respuesta
                assistant_message = {
                    "role": "assistant",
                    "content": response["answer"],
                    "sources": response.get("sources", {}),
                    "metrics": response.get("metrics", {})
                }
                
                # Añadir al historial y mostrar
                st.session_state.messages.append(assistant_message)
                self.render_message(assistant_message)
                
            except Exception as e:
                self.logger.error(f"Error generando respuesta: {str(e)}")
                st.error(f"Error al generar respuesta: {str(e)}")

    def render_history(self):
        """Renderiza el historial completo de mensajes"""
        for message in st.session_state.messages:
            self.render_message(message) 