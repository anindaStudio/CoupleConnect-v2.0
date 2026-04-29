import streamlit as st
from openai import OpenAI

# =========================
# CLIENT (GROQ FIX)
# =========================
def get_client():
    return OpenAI(
        base_url="https://api.groq.com/openai/v1",
        api_key=st.secrets.get("GROQ_API_KEY")
    )

# =========================
# AI RESPONSE FUNCTION
# =========================
def get_ai_response(messages, system_prompt):
    try:
        api_key = st.secrets.get("GROQ_API_KEY")

        if not api_key:
            return "Error: GROQ_API_KEY not found in secrets.toml ❌"

        client = get_client()

        response = client.chat.completions.create(
            model = "llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": system_prompt},
                *messages
            ]
        )

        return response.choices[0].message.content

    except Exception as e:
        return f"Error: {str(e)}"

# =========================
# MAIN UI
# =========================
def render_ai_advisor():

    st.markdown("""
    <div style="padding:20px 0 10px;">
        <div style="font-size:13px; color:#C77DFF; letter-spacing:3px;">✦ AI POWERED</div>
        <div class="section-title">💜 Relationship Advisor</div>
        <div style="color:#b89aa2;">
            Your personal AI counselor for love & relationships 💕
        </div>
    </div>
    """, unsafe_allow_html=True)

    SYSTEM_PROMPT = """You are Dr. Luna, an empathetic and wise AI relationship counselor.
You give warm, practical advice.
Keep answers short (under 200 words).
Mix Bangla + English naturally if needed."""

    # SESSION INIT
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # QUICK TOPICS
    st.markdown("**Quick Topics:**")

    topics = [
        "💬 Communication Issues",
        "💔 Trust Problems",
        "❤️ Strengthen Bond",
        "🌍 Long Distance",
        "💑 First Date Tips",
        "😤 Handling Fights"
    ]

    cols = st.columns(3)

    for i, topic in enumerate(topics):
        with cols[i % 3]:
            if st.button(topic, key=f"topic_{i}", use_container_width=True):

                st.session_state.chat_history.append({
                    "role": "user",
                    "content": f"Give me advice about: {topic}"
                })

                with st.spinner("Dr. Luna is thinking... 💭"):
                    reply = get_ai_response(
                        st.session_state.chat_history,
                        SYSTEM_PROMPT
                    )

                st.session_state.chat_history.append({
                    "role": "assistant",
                    "content": reply
                })

                st.rerun()

    st.markdown('<div class="heart-divider">♥</div>', unsafe_allow_html=True)

    # CHAT DISPLAY
    if not st.session_state.chat_history:
        st.markdown("""
        <div style="text-align:center; padding:40px;">
            <div style="font-size:40px;">🌸</div>
            <div>Hello! I'm Dr. Luna 💜</div>
        </div>
        """, unsafe_allow_html=True)

    for msg in st.session_state.chat_history:
        if msg["role"] == "user":
            st.markdown(f"""
            <div class="chat-msg-user">
                <b>You 💬</b><br>{msg['content']}
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="chat-msg-ai">
                <b>Dr. Luna 🌸</b><br>{msg['content']}
            </div>
            """, unsafe_allow_html=True)

    # INPUT
    user_input = st.text_input("Ask Dr. Luna...", key="advisor_input")

    col1, col2 = st.columns([3, 1])

    with col1:
        if st.button("💬 Send", use_container_width=True) and user_input:

            st.session_state.chat_history.append({
                "role": "user",
                "content": user_input
            })

            with st.spinner("Thinking... 💭"):
                reply = get_ai_response(
                    st.session_state.chat_history,
                    SYSTEM_PROMPT
                )

            st.session_state.chat_history.append({
                "role": "assistant",
                "content": reply
            })

            st.rerun()

    with col2:
        if st.button("🗑️ Clear", use_container_width=True):
            st.session_state.chat_history = []
            st.rerun()