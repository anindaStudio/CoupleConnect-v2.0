import streamlit as st
import os
import json
from datetime import datetime

DATA_FILE = "memories.json"
UPLOAD_FOLDER = "memory_images"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def load_data():
    if os.path.exists(DATA_FILE):
        return json.load(open(DATA_FILE))
    return []

def save_data(data):
    json.dump(data, open(DATA_FILE, "w"))

def app():
    st.title("🖼️ Memory Wall")

    image = st.file_uploader("Upload Memory Photo 📸", type=["jpg", "png", "jpeg"])
    text = st.text_area("Write your memory ❤️")

    if st.button("Save Memory"):
        if image and text:
            filename = f"{datetime.now().timestamp()}.png"
            filepath = os.path.join(UPLOAD_FOLDER, filename)

            with open(filepath, "wb") as f:
                f.write(image.read())

            data = load_data()
            data.append({
                "image": filepath,
                "text": text,
                "time": str(datetime.now())
            })
            save_data(data)

            st.success("Memory Saved ❤️")

    st.subheader("Your Memories 💕")

    data = load_data()

    for i, mem in enumerate(data):
        st.image(mem["image"], width=300)
        st.write(mem["text"])
        st.caption(mem["time"])

        if st.button("❌ Delete", key=i):
            os.remove(mem["image"])
            data.pop(i)
            save_data(data)
            st.rerun()