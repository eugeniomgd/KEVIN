import streamlit as st
from pathlib import Path
from src.core.config import settings
from src.core.logger import Logger
from src.models.rag_model import RAGModel
from src.ui.components.header import Header
from src.ui.components.sidebar import Sidebar
from src.ui.components.chat import Chat
from src.prompts.qa_prompts import PROMPTS

class OperationsApp:
    def __init__(self):
        """Inicializa la aplicación"""
        self.logger = Logger()
        
        # Inicializar estado de la sesión
        if 'messages' not in st.session_state:
            st.session_state.messages = []
        if 'rag_model' not in st.session_state:
            st.session_state.rag_model = RAGModel()
        if 'initialized' not in st.session_state:
            st.session_state.initialized = False
        
        # Inicializar componentes
        self.header = Header()
        self.sidebar = Sidebar()
        self.chat = Chat()

    def setup_page_config(self):
        """Configura las opciones de la página"""
        st.set_page_config(
            page_title="Kevin",
            page_icon=str(Path("assets/logo.ico")),
            layout="wide",
            initial_sidebar_state="expanded",
            menu_items=None
        )
        
        # Inicializar el prompt seleccionado si no existe
        if "selected_prompt" not in st.session_state:
            st.session_state.selected_prompt = "analista"

    def run(self):
        """Ejecuta la aplicación"""
        try:
            # Configurar página
            self.setup_page_config()
            
            # Renderizar sidebar primero
            self.sidebar.render(st.session_state.rag_model)
            
            # Renderizar header (ahora vacío)
            self.header.render()
            
            # Renderizar historial del chat
            self.chat.render_history()
            
            # Manejar nueva entrada
            self.chat.handle_input(st.session_state.rag_model)
            
        except Exception as e:
            self.logger.error(f"Error en la aplicación: {str(e)}")
            st.error("Ha ocurrido un error en la aplicación. Por favor, revisa los logs.")

def main():
    app = OperationsApp()
    app.run()

if __name__ == "__main__":
    main() 