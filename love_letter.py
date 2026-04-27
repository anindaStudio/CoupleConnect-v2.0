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
# AI FUNCTION
# =========================
def generate_love_letter(data):
    try:
        api_key = st.secrets.get("GROQ_API_KEY")

        if not api_key:
            return "Error: GROQ_API_KEY missing ❌"

        client = get_client()

        prompt = f"""
Write a deeply emotional and personalized love letter.

Details:
- Sender name: {data['sender']}
- Partner name: {data['partner']}
- Tone: {data['tone']}
- Occasion: {data['occasion']}
- Special memory: {data['memory']}

Requirements:
- Romantic and heartfelt
- 150-250 words
- Natural human tone
- Include emotions, appreciation, and future hope
- Use light emojis optionally
- Can mix English + Bengali if romantic

Return ONLY the letter.
"""

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}]
        )

        return response.choices[0].message.content

    except Exception as e:
        return f"Error: {str(e)}"

# =========================
# MAIN UI
# =========================
def render_love_letter():

    st.markdown("""
    <div style="padding:20px 0 10px;">
        <div style="font-size:13px; color:#FF4D6D;">✦ AI GENERATED</div>
        <div class="section-title">💌 Love Letter Generator</div>
        <div style="color:#b89aa2;">Express your feelings beautifully 💕</div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        sender = st.text_input("Your Name")
        partner = st.text_input("Partner Name")
        tone = st.selectbox("Tone", [
            "Romantic 💖",
            "Deep Emotional 🥺",
            "Cute & Playful 😄",
            "Apology 😔",
            "Long Distance 💕"
        ])

    with col2:
        occasion = st.selectbox("Occasion", [
            "Anniversary",
            "Birthday",
            "Valentine's Day",
            "Sorry Letter",
            "Just Because"
        ])
        memory = st.text_area("Special Memory")

    if st.button("💌 Generate Love Letter", use_container_width=True):

        if not sender or not partner:
            st.warning("Please enter both names 💕")
            return

        data = {
            "sender": sender,
            "partner": partner,
            "tone": tone,
            "occasion": occasion,
            "memory": memory
        }

        with st.spinner("Writing something beautiful... ✨"):
            letter = generate_love_letter(data)

        st.markdown("### 💌 Your Letter")
        st.write(letter)

        # Download
        st.download_button(
            "📥 Download Letter",
            letter,
            file_name="love_letter.txt"
        )