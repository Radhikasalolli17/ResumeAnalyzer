import streamlit as st
from streamlit_option_menu import option_menu
import os

if 'page' not in st.session_state: st.session_state.page = 'Dashboard'
if 'parsed_resume' not in st.session_state: st.session_state.parsed_resume = None
if 'analysis_results' not in st.session_state: st.session_state.analysis_results = None

st.set_page_config(page_title="AI Resume Intelligence & Career Assistant", page_icon="📄", layout="wide")

from pages import dashboard, analyzer, chat, feedback, admin

def main():
    st.sidebar.title("📄 AI Resume Assistant")
    with st.sidebar:
        selected = option_menu(
            menu_title=None,
            options=["Dashboard", "Resume Analyzer", "AI Assistant", "Feedback", "Admin"],
            icons=["house", "file-earmark-text", "robot", "chat-left-text", "gear"],
            default_index=0,
        )

    if selected == "Dashboard": dashboard.show()
    elif selected == "Resume Analyzer": analyzer.show()
    elif selected == "AI Assistant": chat.show()
    elif selected == "Feedback": feedback.show()
    elif selected == "Admin": admin.show()

if __name__ == "__main__":
    os.makedirs("./Uploaded_Resumes", exist_ok=True)
    main()
