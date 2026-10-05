import streamlit as st, pandas as pd, plotly.express as px
from database.connection import Database

def show():
    st.title("📝 Feedback")
    with st.form("f_form"):
        n, e, r, c = st.text_input("Name"), st.text_input("Email"), st.slider("Rating", 1, 5, 5), st.text_area("Comments")
        if st.form_submit_button("Submit"):
            db = Database()
            if db.connect():
                db.insert_feedback(n, e, r, c); st.success("Thanks!"); st.balloons(); db.close()
    db = Database()
    if db.connect():
        db.cursor.execute("SELECT rating, COUNT(*) as c FROM feedback GROUP BY rating")
        rows = db.cursor.fetchall()
        if rows: st.plotly_chart(px.pie(pd.DataFrame(rows, columns=['Rating', 'Count']), values='Count', names='Rating'))
        db.close()
