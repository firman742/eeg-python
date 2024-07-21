import streamlit as st 

# ---- Page Setup -----

dashboard_page = st.Page(
        page="views/dashboard.py",
        title="Dashboard",
        icon=":material/bar_chart:",
        default=True
)

analysis_page = st.Page(
        page="views/analysis.py",
        title="Analysis",
        icon=":material/account_circle:",
)

about_page = st.Page(
        page="views/about.py",
        title="About",
        icon=":material/account_circle:",
)
#  --- Navigation Setup ---
pg = st.navigation(pages=[dashboard_page, analysis_page, about_page])

pg.run()
