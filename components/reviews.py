import streamlit as st
import datetime

def app():
    st.title("⭐ CoupleConnect Reviews")

    # session storage (simple version)
    if "reviews" not in st.session_state:
        st.session_state.reviews = []

    st.subheader("Write a Review 💬")

    rating = st.slider("Rating ⭐", 1, 5, 4)
    comment = st.text_area("Your feedback")

    if st.button("Submit Review ✨"):

        if not comment:
            st.warning("Please write something")
            return

        review = {
            "rating": rating,
            "comment": comment,
            "date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        }

        st.session_state.reviews.append(review)
        st.success("Review submitted ❤️")

    st.markdown("---")

    st.subheader("🌟 User Reviews")

    if not st.session_state.reviews:
        st.info("No reviews yet")
        return

    # average rating
    avg = sum(r["rating"] for r in st.session_state.reviews) / len(st.session_state.reviews)
    st.markdown(f"### ⭐ Average Rating: {avg:.1f}/5")

    # show reviews
    for r in reversed(st.session_state.reviews):
        st.markdown(f"""
        ⭐ {r['rating']}/5  
        💬 {r['comment']}  
        🕒 {r['date']}
        """)
        st.markdown("---")