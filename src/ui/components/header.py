import streamlit as st
from src.prompts.qa_prompts import PROMPTS

class Header:
    def render(self):
        """Renderiza el header con el selector de prompts"""
        st.write("### Selecciona el estilo de respuesta")
        
        cols = st.columns(len(PROMPTS))
        
        for idx, (prompt_id, prompt_info) in enumerate(PROMPTS.items()):
            with cols[idx]:
                button_key = f"header_prompt_selector_{prompt_id}_{idx}"
                
                if st.button(
                    label=prompt_info['name'],
                    help=prompt_info['description'],
                    key=button_key,
                    use_container_width=True,
                    type="primary" if st.session_state.selected_prompt == prompt_id else "secondary"
                ):
                    st.session_state.selected_prompt = prompt_id