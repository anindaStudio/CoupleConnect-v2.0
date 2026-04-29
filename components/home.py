import streamlit as st

def render_home():
    # Floating hearts
    st.markdown("""
    <div style="position:fixed; top:0; left:0; width:100%; height:100%; pointer-events:none; z-index:0; overflow:hidden;">
        <span class="floating-heart" style="left:10%; animation-duration:8s; animation-delay:0s;">💕</span>
        <span class="floating-heart" style="left:30%; animation-duration:12s; animation-delay:3s;">❤️</span>
        <span class="floating-heart" style="left:60%; animation-duration:9s; animation-delay:1s;">💖</span>
        <span class="floating-heart" style="left:80%; animation-duration:11s; animation-delay:5s;">💗</span>
    </div>
    """, unsafe_allow_html=True)

    # Hero section
    col1, col2 = st.columns([1.2, 1])
    with col1:
        st.markdown("""
        <div style="padding: 40px 0 20px;">
            <div style="font-size:13px; color:#FF4D6D; font-weight:600; letter-spacing:3px; 
                        text-transform:uppercase; margin-bottom:16px;">✦ Welcome to</div>
            <div class="hero-title">Couple<br>Connect</div>
            <div class="hero-sub">Where love meets intelligence.<br>
                AI-powered tools for every relationship stage.</div>
        </div>
        """, unsafe_allow_html=True)

        col_a, col_b = st.columns(2)
        with col_a:
            if st.button("💑 I'm in a Relationship", use_container_width=True):
                st.session_state.relationship_status = "coupled"
                st.success("Welcome, lovebirds! 💕")
        with col_b:
            if st.button("💫 I'm Single", use_container_width=True):
                st.session_state.relationship_status = "single"
                st.session_state.page = "single_ai"
                st.rerun()

    with col2:
        st.markdown("""
        <div style="display:flex; justify-content:center; align-items:center; 
                    height:300px; font-size:140px; text-align:center;
                    filter:drop-shadow(0 0 40px rgba(255,77,109,0.4));">
            💑
        </div>
        """, unsafe_allow_html=True)

    st.markdown('<div class="heart-divider">♥ ♥ ♥</div>', unsafe_allow_html=True)

    # Stats row
    st.markdown("""
    <div style="display:grid; grid-template-columns:repeat(4,1fr); gap:16px; margin-bottom:40px;">
        <div style="background:rgba(255,77,109,0.08); border:1px solid rgba(255,77,109,0.2); 
                    border-radius:16px; padding:20px; text-align:center;">
            <div style="font-size:32px; font-family:'Playfair Display',serif; color:#FF4D6D; font-weight:700;">8+</div>
            <div style="font-size:12px; color:#b89aa2; margin-top:4px;">AI Features</div>
        </div>
        <div style="background:rgba(199,125,255,0.08); border:1px solid rgba(199,125,255,0.2); 
                    border-radius:16px; padding:20px; text-align:center;">
            <div style="font-size:32px; font-family:'Playfair Display',serif; color:#C77DFF; font-weight:700;">∞</div>
            <div style="font-size:12px; color:#b89aa2; margin-top:4px;">Love Letters</div>
        </div>
        <div style="background:rgba(0,180,216,0.08); border:1px solid rgba(0,180,216,0.2); 
                    border-radius:16px; padding:20px; text-align:center;">
            <div style="font-size:32px; font-family:'Playfair Display',serif; color:#00B4D8; font-weight:700;">50+</div>
            <div style="font-size:12px; color:#b89aa2; margin-top:4px;">Date Spots</div>
        </div>
        <div style="background:rgba(255,215,0,0.08); border:1px solid rgba(255,215,0,0.2); 
                    border-radius:16px; padding:20px; text-align:center;">
            <div style="font-size:32px; font-family:'Playfair Display',serif; color:#FFD700; font-weight:700;">💯</div>
            <div style="font-size:12px; color:#b89aa2; margin-top:4px;">Love Score</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Features grid
    st.markdown('<div class="section-title">✨ Explore Features</div>', unsafe_allow_html=True)
    st.markdown('<div style="color:#b89aa2; font-size:14px; margin-bottom:24px;">Everything you need for a magical relationship</div>', unsafe_allow_html=True)

    features = [
        ("🤖", "AI Love Advisor", "Get personalized relationship advice & tips", "ai_advisor"),
        ("📍", "Dating Locations", "Find perfect romantic spots near you", "dating_locations"),
        ("🎮", "Love Games & Quiz", "Fun games to strengthen your bond", "games"),
        ("💌", "Love Letter Gen", "AI-crafted letters for every moment", "love_letter"),
        ("📅", "Date Night Planner", "Plan unforgettable date experiences", "date_planner"),
        ("❤️‍🔥", "Love Score", "Measure your relationship compatibility", "love_score"),
        ("🌟", "AI Partner", "For singles — your AI companion", "single_ai"),
        ("💝", "Match Finder", "Let AI find your perfect match", "single_ai"),
    ]

    cols = st.columns(4)
    for i, (icon, title, desc, page_key) in enumerate(features):
        with cols[i % 4]:
            if st.button(f"{icon}\n{title}", key=f"feature_{page_key}_{i}", use_container_width=True, help=desc):
                st.session_state.page = page_key
                st.rerun()
            st.markdown(f'<div style="text-align:center; font-size:11px; color:#b89aa2; margin-top:-8px; margin-bottom:16px;">{desc}</div>', unsafe_allow_html=True)