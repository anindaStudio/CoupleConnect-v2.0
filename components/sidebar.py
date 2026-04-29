import streamlit as st

def render_sidebar():
    with st.sidebar:

        # 🔥 Header
        st.markdown("""
        <div style="text-align:center; padding: 20px 0 30px;">
            <div style="font-size:48px;">👩‍❤️‍👨</div>
            <div style="font-family:'Playfair Display',serif; font-size:24px; 
                        background:linear-gradient(135deg,#FF4D6D,#FF85A1); 
                        -webkit-background-clip:text; -webkit-text-fill-color:transparent;
                        font-weight:700;">CoupleConnect</div>
            <div style="font-size:11px; color:#b89aa2;">
                Your Love Journey Starts Here
            </div>
        </div>
        """, unsafe_allow_html=True)

        # 👤 User Info (safe check)
        if "user" in st.session_state and st.session_state.user:
            st.markdown(f"""
            <div style="background:rgba(255,77,109,0.1); padding:10px; border-radius:10px;
                        text-align:center; margin-bottom:10px;">
                👤 <b>{st.session_state.user}</b>
            </div>
            """, unsafe_allow_html=True)

        # 🔗 Navigation
        nav_items = [
            ("🏠 Home", "home"),
            ("🤖 AI Love Advisor", "ai_advisor"),
            ("📍 Dating Locations", "dating_locations"),
            ("🎮 Love Games", "games"),
            ("💌 Love Letter", "love_letter"),
            ("📅 Date Planner", "date_planner"),
            ("❤️‍🔥 Love Score", "love_score"),
            ("🌟 Single AI Partner", "single_ai"),
            ("💞 Partner Connect", "partner_connect"),
            ("💬 Couple Chat", "couple_chat"),

            # 🆕 AI + CREATIVE
            ("📸 Photo Generator", "photo_generator"),
            ("📷 Photo Pose Advisor", "photo_pose"),
            ("🎨 Avatar Generator", "avatar"),
            ("🎁 Surprise Generator", "surprise_generator"),

            # 🆕 MEMORY + ACTIVITY
            ("🖼️ Memory Wall", "memory_wall"),
            ("❤️ Daily Activity", "daily_activity"),

            # 🆕 FEEDBACK
            ("⭐ Reviews", "reviews"),
        ]

        # 🔘 Navigation Buttons
        for label, page_key in nav_items:
            is_active = st.session_state.get("page", "home") == page_key

            if st.button(
                label,
                key=f"nav_{page_key}",
                use_container_width=True,
                type="primary" if is_active else "secondary"
            ):
                st.session_state.page = page_key
                st.rerun()

        # 🔻 Divider
        st.markdown("---")

        # 🚪 Logout
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.user = None
            st.session_state.page = "home"   # 🔥 reset page
            st.rerun()

        # 🔻 Footer
        st.markdown("""
        <div style="text-align:center; font-size:11px; color:#b89aa2; padding:10px;">
            ✨ Built by <b>Aninda</b><br>
            <span style="color:#FF4D6D;">CoupleConnect v2.0</span>
        </div>
        """, unsafe_allow_html=True)