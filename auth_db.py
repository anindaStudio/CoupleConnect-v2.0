import streamlit as st
import sqlite3
import hashlib

# =========================
# DB SETUP
# =========================
conn = sqlite3.connect("users.db", check_same_thread=False)
c = conn.cursor()

# USERS
c.execute("""
CREATE TABLE IF NOT EXISTS users (
    email TEXT PRIMARY KEY,
    password TEXT
)
""")

# CONNECTIONS
c.execute("""
CREATE TABLE IF NOT EXISTS connections (
    user_email TEXT,
    partner_email TEXT,
    status TEXT
)
""")

# INVITES
c.execute("""
CREATE TABLE IF NOT EXISTS invites (
    sender TEXT,
    receiver TEXT,
    status TEXT
)
""")

# CHAT
c.execute("""
CREATE TABLE IF NOT EXISTS messages (
    sender TEXT,
    receiver TEXT,
    message TEXT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
)
""")

# QUIZ
c.execute("""
CREATE TABLE IF NOT EXISTS quiz_answers (
    user TEXT,
    question TEXT,
    answer TEXT
)
""")

conn.commit()

# =========================
# HASH
# =========================
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# =========================
# USER
# =========================
def create_user(email, password):
    try:
        c.execute("INSERT INTO users VALUES (?, ?)",
                  (email, hash_password(password)))
        conn.commit()
        return True
    except:
        return False


def login_user(email, password):
    c.execute("SELECT * FROM users WHERE email=? AND password=?",
              (email, hash_password(password)))
    return c.fetchone()

# =========================
# PARTNER (FIXED 🔥)
# =========================
def send_invite(sender, receiver):

    if sender == receiver:
        return False

    # 🔥 duplicate check
    c.execute("""
    SELECT * FROM invites 
    WHERE sender=? AND receiver=? AND status='pending'
    """, (sender, receiver))

    if c.fetchone():
        return False

    try:
        c.execute("INSERT INTO invites VALUES (?, ?, ?)",
                  (sender, receiver, "pending"))
        conn.commit()
        return True
    except:
        return False


def get_invites(email):
    c.execute("SELECT sender FROM invites WHERE receiver=? AND status='pending'", (email,))
    return c.fetchall()


def accept_invite(sender, receiver):

    # update invite
    c.execute("UPDATE invites SET status='accepted' WHERE sender=? AND receiver=?",
              (sender, receiver))

    # 🔥 prevent duplicate connection
    c.execute("""
    SELECT * FROM connections 
    WHERE user_email=? AND partner_email=?
    """, (sender, receiver))

    if not c.fetchone():
        c.execute("INSERT INTO connections VALUES (?, ?, ?)", (sender, receiver, "connected"))
        c.execute("INSERT INTO connections VALUES (?, ?, ?)", (receiver, sender, "connected"))

    conn.commit()


def get_partner(email):
    c.execute("SELECT partner_email FROM connections WHERE user_email=? AND status='connected'", (email,))
    res = c.fetchone()
    return res[0] if res else None

# =========================
# CHAT
# =========================
def send_message(sender, receiver, message):
    c.execute("INSERT INTO messages (sender, receiver, message) VALUES (?, ?, ?)",
              (sender, receiver, message))
    conn.commit()


def get_messages(user, partner):
    c.execute("""
    SELECT sender, message FROM messages
    WHERE (sender=? AND receiver=?) OR (sender=? AND receiver=?)
    ORDER BY timestamp ASC
    """, (user, partner, partner, user))
    return c.fetchall()

# =========================
# QUIZ
# =========================
def save_answer(user, question, answer):
    c.execute("INSERT INTO quiz_answers VALUES (?, ?, ?)",
              (user, question, answer))
    conn.commit()


def get_partner_answer(partner, question):
    c.execute("SELECT answer FROM quiz_answers WHERE user=? AND question=?",
              (partner, question))
    res = c.fetchone()
    return res[0] if res else None

# =========================
# AUTH UI
# =========================
def render_auth():

    st.markdown("""
    <div style="text-align:center; padding:40px 0 20px;">
        <div style="font-size:50px;">💕</div>
        <div style="font-size:28px; font-weight:700; color:#FF4D6D;">
            CoupleConnect
        </div>
        <div style="color:#b89aa2; font-size:13px;">
            Your Love Journey Starts Here
        </div>
    </div>
    """, unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["🔐 Login", "✨ Signup"])

    with tab1:
        email = st.text_input("Email", key="login_email")
        password = st.text_input("Password", type="password", key="login_pass")

        if st.button("Login"):
            user = login_user(email, password)
            if user:
                st.session_state.logged_in = True
                st.session_state.user = email
                st.rerun()
            else:
                st.error("Invalid credentials")

    with tab2:
        email = st.text_input("New Email", key="signup_email")
        password = st.text_input("New Password", type="password", key="signup_pass")

        if st.button("Create Account"):
            if create_user(email, password):
                st.success("Account created!")
            else:
                st.warning("User already exists")