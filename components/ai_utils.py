from groq import Groq
import streamlit as st

# Initialize client once
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# Config
MODEL_NAME = "llama-3.3-70b-versatile"

def ask_ai(user_input):
    try:
        # Better structured prompt
        prompt = f"""
You are a romantic AI assistant for a couple app called "CoupleConnect".

Task: Generate ONE unique surprise idea.

Context: {user_input}

Rules:
- Make it emotional ❤️
- Keep it practical (low budget if possible)
- Max 3-4 lines
- Make it feel personal and sweet

Output format:
🎁 Surprise Idea:
<your answer>
"""

        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": "You are creative, romantic, and concise."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.9,   # more creative
            max_tokens=150     # control response size
        )

        return response.choices[0].message.content.strip()

    except Exception as e:
        return f"⚠️ Error: {str(e)}"