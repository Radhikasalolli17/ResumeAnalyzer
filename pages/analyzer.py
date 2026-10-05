import streamlit as st
import os, plotly.express as px, pandas as pd
from modules.resume_parser import ResumeParser
from modules.jd_matcher import JDMatcher
from modules.ats_scorer import ATSScorer
from modules.resume_improver import AIResumeAssistant
from database.connection import Database

def show():
    st.title("📄 Resume Analyzer & Job Matcher")
    col1, col2 = st.columns(2)
    with col1: uploaded_file = st.file_uploader("Upload PDF Resume", type=["pdf"])
    with col2:
        target_role = st.text_input("Target Role")
        jd_text = st.text_area("Job Description (Optional)", height=100)

    if st.button("Analyze", type="primary"):
        if not uploaded_file: return st.error("Please upload a resume.")
        with st.spinner("Analyzing..."):
            file_path = os.path.join("Uploaded_Resumes", uploaded_file.name)
            with open(file_path, "wb") as f: f.write(uploaded_file.getbuffer())
            
            parsed = ResumeParser(file_path).get_extracted_data()
            st.session_state.parsed_resume = parsed
            jd_skills = list(set(w.strip(",.") for w in jd_text.split() if len(w)>2)) if jd_text else []
            match_results = JDMatcher().analyze_match(parsed.get("raw_text", ""), jd_text, parsed.get("skills", []), jd_skills)
            ats_score = ATSScorer().score_resume(parsed, match_results)
            st.session_state.analysis_results = {"match_results": match_results, "ats_score": ats_score, "target_role": target_role}
            
            db = Database()
            if db.connect():
                u_id = db.insert_user(parsed.get("name") or "Unknown", parsed.get("email") or "Unknown", parsed.get("phone") or "Unknown")
                db.insert_analysis(u_id, target_role, ats_score.get("total_score"), match_results.get("overall_match_percentage"), uploaded_file.name)
                db.close()
            st.success("Complete!")
            
    if st.session_state.get('parsed_resume') and st.session_state.get('analysis_results'):
        parsed = st.session_state.parsed_resume
        res = st.session_state.analysis_results
        st.divider()
        tab1, tab2, tab3 = st.tabs(["📊 ATS Analysis", "💼 Skill Gaps", "📝 Parsed Data"])
        with tab1:
            st.subheader("ATS Score Breakdown")
            df = pd.DataFrame(list(res['ats_score']['breakdown'].items()), columns=['Category', 'Score'])
            st.plotly_chart(px.bar(df, x='Score', y='Category', orientation='h', color='Score'), use_container_width=True)
        with tab2:
            st.subheader("Skill Gaps")
            m_col, miss_col = st.columns(2)
            with m_col:
                st.success("Matched")
                for s in res['match_results']['matched_skills']: st.write(f"- {s}")
            with miss_col:
                st.error("Missing")
                for s in res['match_results']['missing_skills']: st.write(f"- {s}")
            if res['match_results']['missing_skills'] and st.button("Generate Roadmap"):
                st.info(AIResumeAssistant().generate_learning_roadmap(res['match_results']['missing_skills']))
        with tab3: st.json({k: v for k, v in parsed.items() if k != 'raw_text'})
