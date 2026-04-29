import streamlit as st
from datetime import datetime
from components.ai_utils import ask_ai

def app():
    st.markdown("""
    <h1 style='color:#ff4b8b;'>📅 Daily Love Activity</h1>
    <p style='color:lightgray;'>Small daily actions to grow your relationship 💖</p>
    """, unsafe_allow_html=True)

    # =========================
    # 📅 DATE
    # =========================
    today = datetime.now()
    formatted_date = today.strftime("%A, %d %B %Y")
    date_key = today.strftime("%Y-%m-%d")

    st.markdown(f"### 📆 {formatted_date}")

    # =========================
    # 💾 SESSION STATE INIT
    # =========================
    if "daily_task" not in st.session_state:
        st.session_state.daily_task = {}

    if "task_done" not in st.session_state:
        st.session_state.task_done = {}

    if "love_score" not in st.session_state:
        st.session_state.love_score = 0

    # =========================
    # 🎯 GET TODAY TASK (CACHED)
    # =========================
    if date_key not in st.session_state.daily_task:

        user_profile = st.session_state.get("user_profile", "a couple")
        relationship = st.session_state.get("relationship_status", "in love")

        prompt = f"""
You are a romantic AI assistant.

User: {user_profile}
Relationship status: {relationship}

Today is: {formatted_date}

Generate ONE unique daily activity for a couple.

Rules:
- Must be simple and doable today
- Fun or emotional
- Max 2-3 lines
- Not repetitive

Make it meaningful and realistic.
"""

        with st.spinner("Generating today's special task... 💖"):
            result = ask_ai(prompt + date_key)

        # save task
        st.session_state.daily_task[date_key] = result
        st.session_state.task_done[date_key] = False

    # =========================
    # 🎁 SHOW TASK
    # =========================
    task = st.session_state.daily_task[date_key]

    st.markdown("### 🌟 Today's Love Task")

    st.markdown(f"""
    <div style="
        border:1px dashed #ff4b8b;
        padding:15px;
        border-radius:12px;
        background-color:#1e1e2f;
        color:white;
    ">
    💌 {task}
    </div>
    """, unsafe_allow_html=True)

    # =========================
    # ✅ MARK AS DONE
    # =========================
    if not st.session_state.task_done[date_key]:

        if st.button("✅ Mark as Done"):
            st.session_state.task_done[date_key] = True
            st.session_state.love_score += 5
            st.success("💖 Task completed! Love Score +5")

    else:
        st.success("🎉 You already completed today's task!")

    # =========================
    # ❤️ LOVE SCORE DISPLAY
    # =========================
    st.markdown(f"### ❤️ Love Score: {st.session_state.love_score}")

    # =========================
    # 🔄 GENERATE NEW TASK (optional)
    # =========================
    if st.button("🔄 Generate Another Task"):
        prompt = f"""
Generate a different romantic daily task for today.
Keep it short and unique.
"""

        with st.spinner("Creating another idea... 💫"):
            new_task = ask_ai(prompt + date_key)

        st.session_state.daily_task[date_key] = new_task
        st.session_state.task_done[date_key] = False

        st.rerun()