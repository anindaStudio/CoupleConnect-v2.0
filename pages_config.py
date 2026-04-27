import streamlit as st

def apply_global_styles():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700&family=DM+Sans:wght@300;400;500;600&display=swap');

    :root {
        --rose: #FF4D6D;
        --wine: #C9184A;
        --dark: #120610;
        --text: #f8e8ec;
    }

    /* ===== GLOBAL ===== */
    html, body, [class*="css"] {
        font-family: 'DM Sans', sans-serif;
        background-color: var(--dark) !important;
        color: var(--text) !important;
    }

    .stApp {
        background: linear-gradient(135deg, #120610 0%, #1e0a18 50%, #0d1520 100%) !important;
    }

    #MainMenu, footer, header {
        visibility: hidden;
    }

    /* ===== BUTTON ===== */
    .stButton > button {
        background: linear-gradient(135deg, #FF4D6D, #C9184A);
        color: white !important;
        border-radius: 50px;
        border: none;
        padding: 10px 20px;
        font-weight: 600;
    }

    /* =============================== */
    /* 🔥 INPUT FINAL FIX (IMPORTANT) */
    /* =============================== */

    /* Container */
    div[data-baseweb="input"] {
        background-color: white !important;
        border-radius: 12px !important;
        border: 1px solid #FF4D6D !important;
    }

    /* Text inside input */
    div[data-baseweb="input"] input {
        background-color: transparent !important;
        color: black !important;
        -webkit-text-fill-color: black !important;
        font-size: 16px !important;
        caret-color: #FF4D6D !important;
    }

    /* Password field */
    input[type="password"] {
        color: black !important;
        -webkit-text-fill-color: black !important;
    }

    /* Textarea */
    textarea {
        background-color: white !important;
        color: black !important;
        -webkit-text-fill-color: black !important;
    }

    /* Placeholder */
    input::placeholder, textarea::placeholder {
        color: gray !important;
        opacity: 1 !important;
    }

    /* Autofill fix */
    input:-webkit-autofill,
    input:-webkit-autofill:focus {
        -webkit-text-fill-color: black !important;
        box-shadow: 0 0 0px 1000px white inset !important;
    }

    /* =============================== */

    /* Cards */
    .love-card {
        background: rgba(45,20,32,0.9);
        border-radius: 20px;
        padding: 20px;
        margin: 10px 0;
    }

    .section-title {
        font-family: 'Playfair Display', serif;
        font-size: 30px;
        font-weight: 700;
    }

    </style>
    """, unsafe_allow_html=True)