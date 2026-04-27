import streamlit as st
from components.auth_db import get_partner, send_message, get_messages

def render_couple_chat():

    st.markdown("""
    <div style="padding:20px 0 10px;">
        <div class="section-title">💬 Couple Chat</div>
        <div style="color:#b89aa2;">Private chat with your partner 💕</div>
    </div>
    """, unsafe_allow_html=True)

    user = st.session_state.get("user")

    if not user:
        st.error("User not logged in ❌")
        return

    partner = get_partner(user)

    # ❌ no partner
    if not partner:
        st.warning("Connect with a partner first 💞")
        return

    st.success(f"Chatting with 💕 {partner}")

    # ================= CHAT DISPLAY =================
    chat_container = st.container()

    with chat_container:
        messages = get_messages(user, partner)

        if not messages:
            st.info("Start your conversation 💕")

        for sender, msg in messages:

            if sender == user:
                # USER MESSAGE
                st.markdown(f"""
                <div style="text-align:right; margin:6px;">
                    <span style="
                        background:#FF4D6D;
                        color:white;
                        padding:10px 14px;
                        border-radius:15px;
                        display:inline-block;
                        max-width:70%;
                    ">
                        {msg}
                    </span>
                </div>
                """, unsafe_allow_html=True)

            else:
                # PARTNER MESSAGE
                st.markdown(f"""
                <div style="text-align:left; margin:6px;">
                    <span style="
                        background:#2d1420;
                        color:white;
                        padding:10px 14px;
                        border-radius:15px;
                        display:inline-block;
                        max-width:70%;
                    ">
                        {msg}
                    </span>
                </div>
                """, unsafe_allow_html=True)

    st.markdown("---")

    # ================= INPUT =================
    user_input = st.text_input("Type a message 💕", key="chat_input")

    col1, col2, col3 = st.columns([3,1,1])

    with col1:
        if st.button("Send 💬", use_container_width=True):

            if not user_input:
                st.warning("Type something first 💭")
                return

            send_message(user, partner, user_input)

            # clear input
            st.session_state.chat_input = ""

            st.rerun()

    with col2:
        if st.button("Refresh 🔄", use_container_width=True):
            st.rerun()

    with col3:
        if st.button("Clear 🗑️", use_container_width=True):
            # optional (if you later add clear function)
            st.info("Clear feature coming soon 😄")