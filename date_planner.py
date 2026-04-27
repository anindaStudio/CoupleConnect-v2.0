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
# AI FUNCTION
# =========================
def generate_date_plan(city, mood, budget):
    try:
        client = get_client()

        prompt = f"""
You are a romantic date planner in Bangladesh.

Create a detailed, realistic date plan in {city}.

Rules:
- Always return valid JSON only
- No explanation, no markdown
- Even if city is unknown, create realistic plan (park, cafe, restaurant)

Format:
{{
  "title": "Romantic date title",
  "steps": [
    {{"time": "4:00 PM", "activity": "Visit park"}},
    {{"time": "7:00 PM", "activity": "Dinner"}}
  ],
  "food": "Food suggestion",
  "special_tip": "Romantic tip",
  "estimated_cost": "Low/Medium/High"
}}
"""

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=600
        )

        text = response.choices[0].message.content.strip()

        # 🔥 SAFE JSON PARSE
        start = text.find("{")
        end = text.rfind("}") + 1

        if start != -1 and end != -1:
            text = text[start:end]

        return json.loads(text)

    except Exception:
        # fallback (never fail)
        return {
            "title": f"{city} Romantic Date 💕",
            "steps": [
                {"time": "5 PM", "activity": "Go for a walk in a park"},
                {"time": "7 PM", "activity": "Dinner together"},
                {"time": "9 PM", "activity": "Spend quality time"}
            ],
            "food": "Local restaurant or cafe",
            "special_tip": "Stay present and enjoy each moment 💖",
            "estimated_cost": "Medium"
        }

# =========================
# UI
# =========================
def render_date_planner():
    st.markdown("""
    <div style="padding:20px 0;">
        <div style="font-size:13px; color:#FF4D6D;">✦ AI DATE PLANNER</div>
        <div class="section-title">📅 Smart Date Planner</div>
        <div style="color:#b89aa2;">Plan your perfect romantic day 💕</div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        city = st.text_input("📍 City", placeholder="Dhaka")
        mood = st.selectbox("💖 Mood", ["Romantic", "Fun", "Chill", "Adventure"])

    with col2:
        budget = st.selectbox("💰 Budget", ["Low", "Medium", "High"])

    if st.button("✨ Generate Date Plan", use_container_width=True):

        if not city:
            st.warning("Please enter a city 📍")
            return

        with st.spinner("Planning something magical... 💫"):
            result = generate_date_plan(city, mood, budget)

        # =========================
        # OUTPUT UI
        # =========================
        st.markdown(f"## 💖 {result.get('title')}")

        st.markdown("### ⏰ Timeline")
        for step in result.get("steps", []):
            st.success(f"{step['time']} — {step['activity']}")

        st.markdown("### 🍽️ Food")
        st.info(result.get("food"))

        st.markdown("### ✨ Romantic Tip")
        st.warning(result.get("special_tip"))

        st.markdown("### 💰 Estimated Cost")
        st.write(result.get("estimated_cost"))