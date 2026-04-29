import streamlit as st
import urllib.parse
import time
import requests
from PIL import Image
import io

def app():
    st.title("🎨 Couple Avatar Generator 💕")

    desc = st.text_input("Describe your couple 💭")

    style = st.selectbox(
        "Choose Style 🎨",
        ["Anime", "Cartoon", "Disney", "Realistic", "Romantic"]
    )

    if st.button("Generate Avatar ✨"):

        if not desc:
            st.warning("Please enter description")
            return

        prompt = f"couple, {desc}, {style} style"
        encoded = urllib.parse.quote(prompt)

        image_url = f"https://image.pollinations.ai/prompt/{encoded}?seed={int(time.time())}"

        with st.spinner("Generating... 💖"):
            try:
                response = requests.get(image_url)

                if response.status_code == 200:
                    image = Image.open(io.BytesIO(response.content))
                    st.image(image, use_container_width=True)
                else:
                    st.error("Failed to load image ❌")

            except Exception as e:
                st.error(f"Error: {e}")