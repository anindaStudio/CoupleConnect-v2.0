import streamlit as st
from components.ai_utils import ask_ai

def app():
    # 🎨 Custom CSS (Romantic Dark Theme)
    st.markdown("""
    <style>
    .stApp {
        background: radial-gradient(circle at top left, #1a002b, #000000);
        color: white;
    }

    h1 {
        color: #ff4b8b;
    }

    input, textarea {
        background-color: #1e1e2f !important;
        color: white !important;
        border: 1px solid #ff4b8b !important;
        border-radius: 10px !important;
    }

    div[data-baseweb="select"] {
        background-color: #1e1e2f !important;
        border-radius: 10px !important;
        border: 1px solid #ff4b8b !important;
    }

    .stButton>button {
        background: linear-gradient(90deg, #ff4b8b, #ff1e56);
        color: white;
        border-radius: 12px;
        font-weight: bold;
        border: none;
        padding: 10px 20px;
    }

    .result-box {
        border: 1px dashed #ff4b8b;
        padding: 15px;
        border-radius: 12px;
        background-color: #1e1e2f;
    }
    </style>
    """, unsafe_allow_html=True)

    # 💖 Title
    st.markdown("""
    <h1>🎁 AI Surprise Generator</h1>
    <p style='color:lightgray;'>Get a unique and romantic surprise idea for your special one 💖</p>
    """, unsafe_allow_html=True)

    # 📦 Layout (2 column like your screenshot)
    col1, col2 = st.columns([1, 1.2])

    with col1:
        situation = st.text_area("Your Situation 💭")
        budget = st.selectbox("Budget 💰", ["Low", "Medium", "High"])
        generate = st.button("Generate Surprise 🎁")

    with col2:
        if generate:
            if not situation:
                st.warning("Please enter your situation first!")
                return

            with st.spinner("Creating something special... 💖"):
                user_input = f"Situation: {situation}, Budget: {budget}"
                result = ask_ai(user_input)

            st.markdown("### ✨ Your Surprise Idea")

            # 💎 Styled result box
            st.markdown(f"""
            <div class="result-box">
            🎁 <b>Surprise Idea:</b><br><br>
            {result}
            </div>
            """, unsafe_allow_html=True)

            # 🎯 Buttons (UI only)
            st.button("📋 Copy to Clipboard")
            st.button("✨ Generate Another")

    # ❤️ Footer
    st.markdown("""
    <p style='text-align:center; color:gray; margin-top:30px;'>
    ❤️ Made with love for CoupleConnect 💕
    </p>
    """, unsafe_allow_html=True)