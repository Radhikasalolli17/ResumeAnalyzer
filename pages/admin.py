import streamlit as st, pandas as pd, plotly.express as px
from database.connection import Database

def show():
    st.title("🔐 Admin Dashboard")
    if not st.session_state.get('admin_logged_in'):
        if st.button("Login") if st.text_input("Username") == "admin" and st.text_input("Password", type="password") == "admin" else False:
            st.session_state.admin_logged_in = True
            st.rerun()
        return
    if st.button("Logout"): st.session_state.admin_logged_in = False; st.rerun()
    
    db = Database()
    if not db.connect(): return st.error("No DB.")
    stats = db.get_admin_stats()
    c1, c2, c3 = st.columns(3)
    c1.metric("Users", stats.get('total_users', 0))
    c2.metric("Analyses", stats.get('total_analyses', 0))
    c3.metric("Avg ATS", f"{stats.get('avg_ats_score', 0)}%")
    if stats.get('top_roles'):
        st.plotly_chart(px.bar(pd.DataFrame(stats['top_roles'], columns=['Role', 'Count']), x='Role', y='Count'))
    if st.button("Export CSV"):
        db.cursor.execute("SELECT * FROM resume_analysis")
        st.download_button("Download", pd.DataFrame(db.cursor.fetchall(), columns=[x[0] for x in db.cursor.description]).to_csv(index=False).encode(), "data.csv", "text/csv")
    db.close()
