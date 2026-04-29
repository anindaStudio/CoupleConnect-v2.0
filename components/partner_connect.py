import streamlit as st
from components.auth_db import send_invite, get_invites, accept_invite, get_partner
from components.email_service import send_email_invite  # 🔥 EMAIL ADD

def render_partner_connect():

    st.markdown("""
    <div style="padding:20px 0 10px;">
        <div style="font-size:13px; color:#FF4D6D; letter-spacing:3px;">✦ CONNECTION</div>
        <div class="section-title">💞 Partner Connect</div>
        <div style="color:#b89aa2;">Connect with your partner and unlock couple features 💕</div>
    </div>
    """, unsafe_allow_html=True)

    user = st.session_state.get("user")

    if not user:
        st.error("User not logged in ❌")
        return

    # =========================
    # CHECK EXISTING PARTNER
    # =========================
    partner = get_partner(user)

    if partner:
        st.markdown(f"""
        <div class="love-card" style="text-align:center;">
            <div style="font-size:20px;">💖 You are connected with</div>
            <div style="font-size:18px; margin-top:8px; color:#FF85A1;">
                {partner}
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.success("Couple features unlocked 💕")
        return

    # =========================
    # SEND INVITE
    # =========================
    st.markdown("### 📩 Invite Your Partner")

    st.markdown('<div class="love-card">', unsafe_allow_html=True)

    partner_email = st.text_input(
        "Partner Email",
        placeholder="Enter your partner's email"
    )

    if st.button("💌 Send Invite", use_container_width=True):

        if not partner_email:
            st.warning("Please enter email 💕")

        elif partner_email == user:
            st.error("You can't invite yourself 😅")

        else:
            success = send_invite(user, partner_email)

            if success:
                # 🔥 EMAIL SEND
                email_sent = send_email_invite(partner_email, user)

                if email_sent:
                    st.success("Invite sent + Email delivered 💌")
                else:
                    st.warning("Invite saved but email failed ⚠️")

            else:
                st.warning("Already invited or something went wrong ⚠️")

    st.markdown('</div>', unsafe_allow_html=True)

    # =========================
    # INCOMING REQUESTS
    # =========================
    st.markdown("### 📬 Incoming Requests")

    invites = get_invites(user)

    if invites:
        for i, inv in enumerate(invites):   # 🔥 FIXED (INDEX ADD)
            sender = inv[0]

            st.markdown('<div class="love-card">', unsafe_allow_html=True)

            col1, col2 = st.columns([3, 1])

            with col1:
                st.markdown(f"💖 **{sender}** wants to connect")

            with col2:
                # 🔥 UNIQUE KEY FIX
                if st.button("Accept", key=f"accept_{sender}_{i}"):
                    accept_invite(sender, user)
                    st.success("Connected successfully 💕")
                    st.rerun()

            st.markdown('</div>', unsafe_allow_html=True)

    else:
        st.info("No pending requests 💭")