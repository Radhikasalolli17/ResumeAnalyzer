import streamlit as st
from modules.resume_improver import AIResumeAssistant

def show():
    st.title("🤖 AI Resume Assistant")
    if not st.session_state.get('parsed_resume'): return st.warning("Analyze a resume first.")
    ast = AIResumeAssistant()
    if not ast.available: return st.error("GEMINI_API_KEY needed in .env.")
    
    t1, t2, t3, t4 = st.tabs(["💬 Chat", "✨ Improve", "📝 Interview", "✉️ Cover Letter"])
    parsed = st.session_state.parsed_resume
    role = st.session_state.analysis_results.get("target_role", "Role")
    
    with t1:
        q = st.text_input("Ask a question about your resume:")
        if st.button("Ask"): st.write(ast.chat_with_resume(parsed, q))
    with t2:
        if st.button("Generate Quality Report"): st.markdown(ast.analyze_resume_quality(parsed))
        if st.button("Generate Summary"): st.info(ast.generate_professional_summary(parsed, role))
    with t3:
        if st.button("Generate Interview Qs"): st.markdown(ast.generate_interview_questions(parsed, role))
    with t4:
        jd = st.text_area("JD for Cover Letter")
        if st.button("Generate Letter"): st.markdown(ast.generate_cover_letter(parsed, role, jd))
