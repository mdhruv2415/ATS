import streamlit as st

recruiter = st.Page("recruiter.py", title="Recruiter", icon=":material/add_circle:")
applicant = st.Page("applicant.py", title="Applicant", icon=":material/thumb_up:")

pg = st.navigation([recruiter, applicant])
# st.tabs()
st.set_page_config(page_title="Applicant Tracking", page_icon=":random:", layout='centered',
    menu_items={
        'Get Help': 'https://www.extremelycoolapp.com/help',
        'Report a bug': "https://www.extremelycoolapp.com/bug",
        'About': "# This is a header. This is an *extremely* cool app!"
    })
pg.run()