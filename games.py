import streamlit as st
from openai import OpenAI
import json
import random

# 🔥 DB functions (already in auth_db.py)
from components.auth_db import get_partner, save_answer, get_partner_answer

# =========================
# CLIENT (GROQ)
# =========================
def get_client():
    return OpenAI(
        base_url="https://api.groq.com/openai/v1",
        api_key=st.secrets.get("GROQ_API_KEY")
    )

# =========================
# AI FUNCTION
# =========================
def get_quiz_questions(category):
    try:
        client = get_client()

        prompt = f"""
Create 5 fun couple quiz questions about {category}.

IMPORTANT:
- Return ONLY valid JSON array
- No explanation
- No markdown

Format:
[
  {{
    "question": "question text",
    "options": ["opt1", "opt2", "opt3", "opt4"],
    "correct": "A",
    "explanation": "why correct",
    "points": 10
  }}
]
"""

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=800
        )

        text = response.choices[0].message.content.strip()

        # 🔥 SAFE JSON PARSE
        start = text.find("[")
        end = text.rfind("]") + 1

        if start != -1 and end != -1:
            text = text[start:end]

        return json.loads(text)

    except:
        # fallback
        return [
            {
                "question": "What builds trust in a relationship?",
                "options": ["Honesty", "Lies", "Ignoring", "Fights"],
                "correct": "A",
                "explanation": "Honesty builds trust 💖",
                "points": 10
            }
        ]

# =========================
# MAIN UI
# =========================
def render_games():
    st.title("🎮 Love Games 💕")

    user = st.session_state.get("user")
    partner = get_partner(user)

    if "quiz_active" not in st.session_state:
        st.session_state.quiz_active = False
    if "quiz_questions" not in st.session_state:
        st.session_state.quiz_questions = []
    if "quiz_index" not in st.session_state:
        st.session_state.quiz_index = 0
    if "quiz_score" not in st.session_state:
        st.session_state.quiz_score = 0
    if "quiz_answered" not in st.session_state:
        st.session_state.quiz_answered = False

    # =========================
    # START SCREEN
    # =========================
    if not st.session_state.quiz_active:
        category = st.selectbox("Choose Category:", [
            "Love", "Movies", "Psychology", "Date Ideas"
        ])

        if st.button("🚀 Start Quiz"):
            with st.spinner("Generating questions..."):
                questions = get_quiz_questions(category)

            if questions:
                st.session_state.quiz_questions = questions
                st.session_state.quiz_active = True
                st.session_state.quiz_index = 0
                st.session_state.quiz_score = 0
                st.session_state.quiz_answered = False
                st.rerun()
            else:
                st.error("Failed to load questions 😢")

    # =========================
    # QUIZ MODE
    # =========================
    else:
        qlist = st.session_state.quiz_questions
        idx = st.session_state.quiz_index

        if idx < len(qlist):
            q = qlist[idx]

            st.markdown(f"### {q.get('question','')}")

            if not st.session_state.quiz_answered:

                for opt_letter, opt_text in zip(["A","B","C","D"], q.get('options', [])):

                    if st.button(f"{opt_letter}. {opt_text}"):

                        # 🔥 save answer
                        if user:
                            save_answer(user, q['question'], opt_letter)

                        st.session_state.quiz_answered = True

                        if opt_letter == q.get('correct'):
                            st.session_state.quiz_score += q.get('points',10)
                            st.success("Correct! 💕")
                        else:
                            st.error(f"Wrong! Correct: {q.get('correct')}")

                        st.info(q.get("explanation",""))

                        st.rerun()

            else:
                # 🔥 partner answer show
                if partner:
                    partner_ans = get_partner_answer(partner, q['question'])
                    if partner_ans:
                        st.info(f"💞 Partner chose: {partner_ans}")

                if st.button("Next"):
                    st.session_state.quiz_index += 1
                    st.session_state.quiz_answered = False
                    st.rerun()

        else:
            st.success(f"Final Score: {st.session_state.quiz_score} 🎉")

            if st.button("Play Again"):
                st.session_state.quiz_active = False
                st.session_state.quiz_questions = []
                st.rerun()

    # =========================
    # TRUTH OR DARE
    # =========================
    st.markdown("---")
    st.markdown("### 🎯 Truth or Dare")

    truths = [
        "What do you love most about me?",
        "When did you fall for me?",
        "What is your favorite memory with me?"
    ]

    dares = [
        "Send a sweet message 💕",
        "Give a compliment 😊",
        "Say something romantic right now 💖"
    ]

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Truth"):
            st.write(random.choice(truths))

    with col2:
        if st.button("Dare"):
            st.write(random.choice(dares))