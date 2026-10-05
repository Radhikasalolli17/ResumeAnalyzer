import streamlit as st

def show():
    st.title("🎯 AI Resume Intelligence Dashboard")
    st.markdown("""
    Welcome to the **AI Resume Intelligence & Career Assistant**.
    
    👈 **Select 'Resume Analyzer' from the sidebar to get started!**
    """)
    if st.session_state.get('parsed_resume') and st.session_state.get('analysis_results'):
        st.divider()
        st.subheader("Your Latest Analysis Summary")
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("ATS Score", f"{st.session_state.analysis_results.get('ats_score', {}).get('total_score', 0)}%")
        col2.metric("Job Match", f"{st.session_state.analysis_results.get('match_results', {}).get('overall_match_percentage', 0)}%")
        col3.metric("Skills Found", len(st.session_state.parsed_resume.get('skills', [])))
        col4.metric("Resume Pages", st.session_state.parsed_resume.get('no_of_pages', 0))
