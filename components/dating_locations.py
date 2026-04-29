import streamlit as st
from openai import OpenAI
import json

# =========================
# CLIENT
# =========================
def get_client():
    return OpenAI(
        base_url="https://api.groq.com/openai/v1",
        api_key=st.secrets.get("GROQ_API_KEY")
    )

# =========================
# FUNCTION
# =========================
def get_location_suggestions(city, vibe, budget, occasion):
    try:
        client = get_client()

        prompt = f"""
You are a travel expert in Bangladesh.

Generate 6 realistic romantic dating locations in {city}, Bangladesh.

IMPORTANT:
- Always return ONLY valid JSON array
- No explanation
- No markdown
- Even if unsure, create realistic places (parks, cafes, beaches)

Format:
[
  {{
    "name": "Place name",
    "type": "Cafe/Park/etc",
    "description": "Short description",
    "why_perfect": "Why good",
    "best_time": "Time",
    "tip": "Tip",
    "rating": "4.5",
    "emoji": "💖",
    "price_range": "$$"
  }}
]
"""

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=800
        )

        text = response.choices[0].message.content.strip()

        # 🔥 JSON SAFE PARSE
        start = text.find("[")
        end = text.rfind("]") + 1

        if start != -1 and end != -1:
            text = text[start:end]

        return json.loads(text)

    except:
        # 🔥 fallback
        return [
            {
                "name": f"{city} Park",
                "type": "Outdoor",
                "description": "Nice place for couples",
                "why_perfect": "Peaceful & romantic",
                "best_time": "Evening",
                "tip": "Walk together",
                "rating": "4.3",
                "emoji": "🌿",
                "price_range": "$"
            }
        ]

# =========================
# UI
# =========================
def render_dating_locations():
    st.title("📍 Dating Location Finder 💕")

    col1, col2 = st.columns(2)

    with col1:
        city = st.text_input("City", placeholder="Dhaka")
        vibe = st.selectbox("Vibe", ["Romantic", "Fun", "Chill", "Luxury", "Nature"])

    with col2:
        budget = st.selectbox("Budget", ["Low", "Medium", "High"])
        occasion = st.selectbox("Occasion", ["First Date", "Anniversary", "Casual", "Special"])

    if st.button("🔍 Find Spots", use_container_width=True):

        if not city:
            st.warning("Enter a city first!")
            return

        with st.spinner("Finding places... 💕"):
            locations = get_location_suggestions(city, vibe, budget, occasion)

        for loc in locations:
            st.markdown(f"""
### {loc.get('emoji','📍')} {loc.get('name','')}
**Type:** {loc.get('type','')}

{loc.get('description','')}

💡 {loc.get('why_perfect','')}
🕐 {loc.get('best_time','')}
✨ {loc.get('tip','')}

⭐ {loc.get('rating','4')} | 💰 {loc.get('price_range','$$')}
---
""")