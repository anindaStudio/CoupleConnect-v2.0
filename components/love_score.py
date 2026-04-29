import streamlit as st
from openai import OpenAI
import json
import re

# =========================
# CLIENT (GROQ)
# =========================
def get_client():
    return OpenAI(
        base_url="https://api.groq.com/openai/v1",
        api_key=st.secrets.get("GROQ_API_KEY")
    )

# =========================
# 🧠 SAFE JSON EXTRACTOR
# =========================
def extract_json(text):
    try:
        # remove markdown ```json ```
        text = re.sub(r"```json|```", "", text).strip()

        # find JSON block
        match = re.search(r"\{.*\}", text, re.DOTALL)
        if match:
            return json.loads(match.group())
        else:
            return None
    except:
        return None

# =========================
# AI FUNCTION
# =========================
def calculate_love_score(data):
    try:
        api_key = st.secrets.get("GROQ_API_KEY")

        if not api_key:
            return {"error": "GROQ_API_KEY missing ❌"}

        client = get_client()

        prompt = f"""
Analyze this relationship and give a compatibility score.

Data:
- Duration: {data['duration']}
- Communication: {data['communication']}
- Trust: {data['trust']}
- Time Together: {data['time']}
- Conflict Handling: {data['conflict']}

Return ONLY valid JSON (no explanation):

{{
  "score": number (0-100),
  "summary": "short emotional summary",
  "strengths": ["point1","point2"],
  "improvements": ["point1","point2"],
  "advice": "practical advice"
}}
"""

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "You are a strict JSON generator."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7
        )

        text = response.choices[0].message.content.strip()

        parsed = extract_json(text)

        if not parsed:
            return {"error": "Failed to parse AI response ❌"}

        return parsed

    except Exception as e:
        return {"error": str(e)}

# =========================
# MAIN UI
# =========================
def render_love_score():

    st.markdown("""
    <div style="padding:20px 0 10px;">
        <div style="font-size:13px; color:#FFD700;">✦ AI ANALYSIS</div>
        <div style="font-size:28px; font-weight:bold;">❤️ Love Compatibility Score</div>
        <div style="color:#b89aa2;">Measure your relationship strength 💕</div>
    </div>
    """, unsafe_allow_html=True)

    # INPUT
    col1, col2 = st.columns(2)

    with col1:
        duration = st.selectbox("Relationship Duration", [
            "Less than 3 months",
            "3-6 months",
            "6-12 months",
            "1-3 years",
            "3+ years"
        ])
        communication = st.slider("Communication Level", 1, 10, 7)
        trust = st.slider("Trust Level", 1, 10, 7)

    with col2:
        time = st.slider("Time Spent Together", 1, 10, 6)
        conflict = st.slider("Conflict Handling", 1, 10, 6)

    # BUTTON
    if st.button("💖 Calculate Love Score", use_container_width=True):

        data = {
            "duration": duration,
            "communication": communication,
            "trust": trust,
            "time": time,
            "conflict": conflict
        }

        with st.spinner("Analyzing your relationship... 💫"):
            result = calculate_love_score(data)

        if "error" in result:
            st.error(result["error"])
            return

        score = result.get("score", 70)

        # 🎯 SCORE DISPLAY
        st.markdown(f"## ❤️ {score}% Compatibility")

        # 💬 SUMMARY
        st.markdown("### 💬 Summary")
        st.write(result.get("summary", ""))

        # 💚 STRENGTHS
        st.markdown("### 💚 Strengths")
        for s in result.get("strengths", []):
            st.success(s)

        # ⚠️ IMPROVEMENTS
        st.markdown("### ⚠️ Improvements")
        for i in result.get("improvements", []):
            st.warning(i)

        # 💡 ADVICE
        st.markdown("### 💡 Advice")
        st.info(result.get("advice", "Keep loving each other 💕"))