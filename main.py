import streamlit as st
from pages_config import apply_global_styles

st.set_page_config(
    page_title="CoupleConnect ❤️",
    page_icon="❤️",
    layout="wide",
    initial_sidebar_state="expanded"
)

apply_global_styles()

# =========================
# SESSION STATE INIT
# =========================
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "user_profile" not in st.session_state:
    st.session_state.user_profile = None
if "relationship_status" not in st.session_state:
    st.session_state.relationship_status = None
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "quiz_score" not in st.session_state:
    st.session_state.quiz_score = 0
if "love_score" not in st.session_state:
    st.session_state.love_score = None
if "partner_profile" not in st.session_state:
    st.session_state.partner_profile = None
if "page" not in st.session_state:
    st.session_state.page = "home"

# =========================
# IMPORTS
# =========================
from components.auth_db import render_auth
from components.sidebar import render_sidebar
from components.home import render_home
from components.ai_advisor import render_ai_advisor
from components.dating_locations import render_dating_locations
from components.games import render_games
from components.single_ai import render_single_ai
from components.love_score import render_love_score
from components.love_letter import render_love_letter
from components.date_planner import render_date_planner
from components.partner_connect import render_partner_connect
from components.couple_chat import render_couple_chat   # 🔥 NEW

# =========================
# 🔐 LOGIN GATE
# =========================
if not st.session_state.logged_in:
    render_auth()
    st.stop()

# =========================
# MAIN APP
# =========================
render_sidebar()

page = st.session_state.get("page", "home")

if page == "home":
    render_home()

elif page == "ai_advisor":
    render_ai_advisor()

elif page == "dating_locations":
    render_dating_locations()

elif page == "games":
    render_games()

elif page == "single_ai":
    render_single_ai()

elif page == "love_score":
    render_love_score()

elif page == "love_letter":
    render_love_letter()

elif page == "date_planner":
    render_date_planner()

elif page == "partner_connect":
    render_partner_connect()

# 🔥 NEW CHAT PAGE
elif page == "couple_chat":
    render_couple_chat()