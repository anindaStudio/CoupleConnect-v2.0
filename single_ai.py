import streamlit as st
from openai import OpenAI

# =========================
# CLIENT (GROQ)
# =========================
def get_client():
    return OpenAI(
        base_url="https://api.groq.com/openai/v1",
        api_key=st.secrets.get("GROQ_API_KEY")
    )

# =========================
# AI RESPONSE FUNCTION
# =========================
def get_ai_partner_response(messages, personality):
    try:
        api_key = st.secrets.get("GROQ_API_KEY")

        if not api_key:
            return "Error: GROQ_API_KEY missing ❌"

        client = get_client()

        system_prompt = f"""
You are a virtual romantic partner.

Personality: {personality}

You behave like a real human partner:
- Emotionally engaging
- Caring, loving, playful
- Sometimes flirty but respectful
- Ask questions back
- Keep replies short (1-3 sentences)
- Use emojis naturally

Speak Bangla + English naturally.
"""

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": system_prompt},
                *messages
            ]
        )

        return response.choices[0].message.content

    except Exception as e:
        return f"Error: {str(e)}"

# =========================
# MAIN UI FUNCTION
# =========================
def render_single_ai():

    st.markdown("""
    <div style="padding:20px 0 10px;">
        <div style="font-size:13px; color:#FF4D6D;">✦ AI PARTNER</div>
        <div class="section-title">🌟 Your AI Companion</div>
        <div style="color:#b89aa2;">Not in a relationship? I'm here for you 💕</div>
    </div>
    """, unsafe_allow_html=True)

    # SESSION INIT
    if "ai_chat" not in st.session_state:
        st.session_state.ai_chat = []

    if "ai_personality" not in st.session_state:
        st.session_state.ai_personality = "Sweet & Caring 💖"

    # PERSONALITY SELECT
    personality = st.selectbox(
        "Choose personality:",
        [
            "Sweet & Caring 💖",
            "Flirty & Playful 😏",
            "Calm & Supportive 🌿",
            "Funny & Chaotic 😂",
            "Romantic & Deep 💌"
        ]
    )

    st.session_state.ai_personality = personality

    st.markdown("---")

    # CHAT UI
    if not st.session_state.ai_chat:
        st.info("Start chatting with your AI partner 💕")

    for msg in st.session_state.ai_chat:
        if msg["role"] == "user":
            st.markdown(f"**You 💬:** {msg['content']}")
        else:
            st.markdown(f"**AI 💖:** {msg['content']}")

    # INPUT
    user_input = st.text_input("Type your message...", key="ai_input")

    col1, col2 = st.columns([3, 1])

    with col1:
        if st.button("💬 Send", use_container_width=True) and user_input:

            st.session_state.ai_chat.append({
                "role": "user",
                "content": user_input
            })

            with st.spinner("Typing... 💭"):
                reply = get_ai_partner_response(
                    st.session_state.ai_chat,
                    st.session_state.ai_personality
                )

            st.session_state.ai_chat.append({
                "role": "assistant",
                "content": reply
            })

            st.rerun()

    with col2:
        if st.button("🗑️ Reset", use_container_width=True):
            st.session_state.ai_chat = []
            st.rerun()