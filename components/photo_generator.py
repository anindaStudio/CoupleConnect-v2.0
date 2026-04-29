import streamlit as st
import urllib.parse
import time

def app():
    st.title("📸 Couple Photo Generator 💕")

    prompt = st.text_input("Describe your couple image 💭")

    # 🔒 prevent multiple clicks
    if "loading" not in st.session_state:
        st.session_state.loading = False

    if st.button("Generate Image ✨") and not st.session_state.loading:

        if not prompt:
            st.warning("Please enter a prompt")
            return

        if "couple" not in prompt.lower():
            st.warning("Please include 'couple' ❤️")
            return

        st.session_state.loading = True

        with st.spinner("Generating your romantic image... 💖"):
            try:
                # 🔥 short + clean prompt
                full_prompt = f"romantic couple {prompt}"
                encoded_prompt = urllib.parse.quote(full_prompt)

                # ✅ random seed (avoid cache + queue clash)
                image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?seed={int(time.time())}"

                time.sleep(2)  # small delay (queue avoid)

                st.markdown("### ✨ Your Generated Image")
                st.image(image_url, use_container_width=True)

                st.markdown(f"[📥 Download Image]({image_url})")

            except Exception as e:
                st.error(f"❌ Error: {str(e)}")

        st.session_state.loading = False