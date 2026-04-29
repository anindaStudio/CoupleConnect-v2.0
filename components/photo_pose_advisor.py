import streamlit as st
from components.ai_utils import ask_ai

def app():
    st.title("📸 Couple Photo Position Advisor 💕")

    situation = st.text_input("Describe your situation (location/mood) 💭")

    if st.button("Get Photo Idea ✨"):

        if not situation:
            st.warning("Please describe your situation")
            return

        prompt = f"""
You are a professional couple photographer.

Give a romantic couple photo pose idea.

Situation: {situation}

Return format:
📸 Pose:
📷 Camera:
💡 Lighting:
🎨 Vibe:

Keep it short and clear.
"""

        result = ask_ai(prompt)

        st.success(result)