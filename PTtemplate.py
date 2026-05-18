from langchain_mistralai import ChatMistralAI
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
import streamlit as st

load_dotenv()

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="AI Interview Assistant",
    page_icon="🎯",
    layout="wide",
)

# ── CSS ────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600&family=Syne:wght@400;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Syne', sans-serif;
}

/* Dark background */
.stApp {
    background: #0a0d14;
    color: #e0e6f0;
}

/* ── Header ── */
.header-wrap {
    padding: 2.2rem 0 0.5rem;
    text-align: center;
}
.header-wrap h1 {
    font-size: 2.4rem;
    font-weight: 800;
    letter-spacing: -0.02em;
    color: #fff;
    margin: 0;
}
.header-wrap h1 span {
    background: linear-gradient(90deg, #00d4ff, #00ff88);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}
.header-wrap p {
    color: #5a6680;
    font-size: 0.92rem;
    margin-top: 0.4rem;
    font-weight: 600;
    letter-spacing: 0.06em;
    text-transform: uppercase;
}

/* ── Setup card ── */
.setup-card {
    background: #111520;
    border: 1px solid #1e2535;
    border-radius: 1.2rem;
    padding: 2rem 2.2rem;
    margin: 1.5rem auto;
    max-width: 700px;
    box-shadow: 0 8px 40px rgba(0,212,255,0.05);
}
.setup-card h3 {
    color: #00d4ff;
    font-size: 1rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    margin-bottom: 1.2rem;
}

/* ── Streamlit form inputs dark ── */
.stTextInput > div > div > input,
.stSelectbox > div > div {
    background: #0d1120 !important;
    border: 1px solid #1e2d45 !important;
    color: #c8d8f0 !important;
    border-radius: 0.6rem !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.88rem !important;
}
.stTextInput > div > div > input:focus {
    border-color: #00d4ff !important;
    box-shadow: 0 0 0 2px rgba(0,212,255,0.15) !important;
}
.stSelectbox > div > div:focus-within {
    border-color: #00d4ff !important;
}
label, .stSelectbox label, .stTextInput label {
    color: #6a7d9e !important;
    font-size: 0.78rem !important;
    font-weight: 700 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.08em !important;
}

/* ── Start button ── */
.stButton > button {
    background: linear-gradient(135deg, #00d4ff, #00ff88) !important;
    color: #000 !important;
    font-weight: 800 !important;
    border: none !important;
    border-radius: 0.7rem !important;
    padding: 0.65rem 2rem !important;
    font-size: 0.95rem !important;
    letter-spacing: 0.04em !important;
    width: 100% !important;
    margin-top: 0.5rem !important;
    transition: opacity 0.2s, transform 0.15s !important;
    font-family: 'Syne', sans-serif !important;
}
.stButton > button:hover {
    opacity: 0.88 !important;
    transform: translateY(-1px) !important;
}

/* ── Info bar ── */
.info-bar {
    display: flex;
    gap: 0.7rem;
    flex-wrap: wrap;
    margin-bottom: 1.2rem;
}
.info-chip {
    background: #111520;
    border: 1px solid #1e2535;
    border-radius: 2rem;
    padding: 0.3rem 0.9rem;
    font-size: 0.78rem;
    font-weight: 700;
    color: #6a8fb0;
    letter-spacing: 0.04em;
}
.info-chip span { color: #00d4ff; }

/* ── Chat bubbles ── */
.bubble-row {
    display: flex;
    margin-bottom: 1.3rem;
    animation: fadeUp 0.35s ease;
}
.bubble-row.user  { justify-content: flex-end; }
.bubble-row.bot   { justify-content: flex-start; }

.bubble {
    max-width: 72%;
    padding: 0.9rem 1.25rem;
    border-radius: 1.2rem;
    font-size: 0.93rem;
    line-height: 1.6;
    font-weight: 400;
    white-space: pre-wrap;
    word-wrap: break-word;
}
.bubble.user {
    background: linear-gradient(135deg, #003d55, #005a40);
    color: #c8f0e0;
    border-bottom-right-radius: 0.25rem;
    border: 1px solid #00ff8833;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.87rem;
}
.bubble.bot {
    background: #111520;
    color: #c8d8f0;
    border-bottom-left-radius: 0.25rem;
    border: 1px solid #1e2535;
}

.avatar {
    width: 34px; height: 34px;
    border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-size: 1rem;
    flex-shrink: 0;
    align-self: flex-end;
}
.avatar.bot-av  { background: #0d1e30; border: 1px solid #1e3a50; margin-right: 0.6rem; }
.avatar.user-av { background: #0d2d1e; border: 1px solid #1e4a30; margin-left:  0.6rem; }

/* ── Typing indicator ── */
.typing-wrap { display:flex; align-items:center; gap:5px; padding:0.6rem 0; }
.dot {
    width:7px; height:7px; background:#00d4ff;
    border-radius:50%; animation:pulse 1.2s infinite;
    opacity:0.6;
}
.dot:nth-child(2){ animation-delay:.2s }
.dot:nth-child(3){ animation-delay:.4s }

/* ── Chat input ── */
[data-testid="stChatInput"] textarea,
.stChatInputContainer textarea {
    background: #0d1120 !important;
    border: 1px solid #1e2d45 !important;
    color: #c8d8f0 !important;
    border-radius: 0.8rem !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.88rem !important;
}

/* ── End session button ── */
.end-btn > button {
    background: transparent !important;
    border: 1px solid #3a1e1e !important;
    color: #ff5a5a !important;
    font-size: 0.78rem !important;
    padding: 0.35rem 1rem !important;
    border-radius: 2rem !important;
    width: auto !important;
}

/* ── Sidebar ── */
section[data-testid="stSidebar"] {
    background: #080b10 !important;
    border-right: 1px solid #141a26 !important;
}
section[data-testid="stSidebar"] * { color: #8899bb !important; }
section[data-testid="stSidebar"] h2 {
    color: #fff !important;
    font-size: 1rem !important;
    letter-spacing: 0.1em !important;
    text-transform: uppercase !important;
}
.stat-box {
    background: #0d1120;
    border: 1px solid #1a2235;
    border-radius: 0.8rem;
    padding: 0.8rem 1rem;
    margin-bottom: 0.6rem;
    text-align: center;
}
.stat-box .num {
    font-size: 1.8rem;
    font-weight: 800;
    color: #00d4ff;
    display: block;
}
.stat-box .lbl {
    font-size: 0.72rem;
    color: #4a5a70;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.08em;
}

@keyframes fadeUp {
    from { opacity:0; transform:translateY(10px) }
    to   { opacity:1; transform:translateY(0) }
}
@keyframes pulse {
    0%,100%{ transform:scale(1);   opacity:0.4 }
    50%    { transform:scale(1.4); opacity:1   }
}
</style>
""", unsafe_allow_html=True)


# ── Session state ──────────────────────────────────────────────────────────────
if "interview_started" not in st.session_state:
    st.session_state.interview_started = False
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []   # {"role": "user"/"bot", "text": "..."}
if "candidate_info" not in st.session_state:
    st.session_state.candidate_info = {}
if "q_count" not in st.session_state:
    st.session_state.q_count = 0
if "model" not in st.session_state:
    st.session_state.model = ChatMistralAI(
        model_name="mistral-small-latest",
        temperature=0.5,
        max_tokens=300,
    )

TEMPLATE = ChatPromptTemplate.from_messages([
    ("system", """
You are an expert AI Interview Assistant for AI, Data Science, Machine Learning, SQL, Python, Power BI, Statistics, and Generative AI interviews.

Your responsibilities:
- Conduct realistic technical interviews
- Ask intelligent follow-up questions
- Evaluate answers honestly
- Give constructive feedback
- Explain mistakes clearly
- Adapt questions based on difficulty level
- Maintain a professional interview atmosphere

Rules:
- Ask one question at a time
- Do not immediately reveal answers
- Give hints if the candidate struggles
- Focus on practical and interview-oriented questions
- Keep responses concise and realistic
"""),
    ("human", """
Candidate Name: {name}
Role: {role}
Experience Level: {experience}
Skills: {skills}
Interview Type: {interview_type}
Difficulty Level: {difficulty}

Candidate Response:
{user_input}
""")
])


# ── Header ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="header-wrap">
  <h1>AI <span>Interview</span> Assistant</h1>
  <p>Powered by Mistral AI · Realistic Technical Interviews</p>
</div>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# SETUP SCREEN
# ══════════════════════════════════════════════════════════════════════════════
if not st.session_state.interview_started:
    st.markdown('<div class="setup-card"><h3>🎯 Candidate Setup</h3>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        name       = st.text_input("Candidate Name", placeholder="e.g. Manish Kumar")
        role       = st.text_input("Target Role", placeholder="e.g. Data Scientist")
        experience = st.selectbox("Experience Level", ["Fresher", "Junior", "Mid-Level", "Senior", "Lead"])
    with col2:
        skills        = st.text_input("Key Skills", placeholder="e.g. Python, SQL, ML, Power BI")
        interview_type = st.selectbox("Interview Type", ["Technical", "Behavioral", "Mixed"])
        difficulty    = st.selectbox("Difficulty Level", ["Easy", "Medium", "Hard"])

    st.markdown("</div>", unsafe_allow_html=True)

    if st.button("🚀 Start Interview Session"):
        if not name.strip() or not role.strip() or not skills.strip():
            st.error("Please fill in Name, Role, and Skills to continue.")
        else:
            st.session_state.candidate_info = {
                "name": name, "role": role, "experience": experience,
                "skills": skills, "interview_type": interview_type, "difficulty": difficulty
            }
            st.session_state.interview_started = True
            st.session_state.q_count = 0
            st.session_state.chat_history = []

            # Kick off first question
            with st.spinner("Preparing your first question…"):
                prompt = TEMPLATE.invoke({
                    **st.session_state.candidate_info,
                    "user_input": "Hello, I am ready to start the interview."
                })
                resp = st.session_state.model.invoke(prompt)
                st.session_state.chat_history.append({"role": "bot", "text": resp.content})
                st.session_state.q_count += 1
            st.rerun()


# ══════════════════════════════════════════════════════════════════════════════
# INTERVIEW SCREEN
# ══════════════════════════════════════════════════════════════════════════════
else:
    info = st.session_state.candidate_info

    # ── Sidebar stats ──────────────────────────────────────────────────────────
    with st.sidebar:
        st.markdown("## 📊 Session Info")
        st.markdown(f"""
        <div class="stat-box"><span class="num">{st.session_state.q_count}</span><span class="lbl">Questions Asked</span></div>
        <div class="stat-box"><span class="num">{len([m for m in st.session_state.chat_history if m['role']=='user'])}</span><span class="lbl">Answers Given</span></div>
        """, unsafe_allow_html=True)
        st.markdown("---")
        st.markdown(f"**Candidate:** {info['name']}")
        st.markdown(f"**Role:** {info['role']}")
        st.markdown(f"**Level:** {info['experience']}")
        st.markdown(f"**Type:** {info['interview_type']}")
        st.markdown(f"**Difficulty:** {info['difficulty']}")
        st.markdown("---")
        if st.button("🔁 New Session"):
            st.session_state.interview_started = False
            st.session_state.chat_history = []
            st.session_state.q_count = 0
            st.rerun()

    # ── Info bar ───────────────────────────────────────────────────────────────
    st.markdown(f"""
    <div class="info-bar">
        <div class="info-chip">👤 <span>{info['name']}</span></div>
        <div class="info-chip">💼 <span>{info['role']}</span></div>
        <div class="info-chip">📊 <span>{info['experience']}</span></div>
        <div class="info-chip">🛠 <span>{info['skills']}</span></div>
        <div class="info-chip">🎯 <span>{info['interview_type']} · {info['difficulty']}</span></div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # ── Chat history ───────────────────────────────────────────────────────────
    for msg in st.session_state.chat_history:
        if msg["role"] == "user":
            st.markdown(f"""
            <div class="bubble-row user">
                <div class="bubble user">{msg['text']}</div>
                <div class="avatar user-av">🧑‍💻</div>
            </div>""", unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="bubble-row bot">
                <div class="avatar bot-av">🤖</div>
                <div class="bubble bot">{msg['text']}</div>
            </div>""", unsafe_allow_html=True)

    # ── Chat input ─────────────────────────────────────────────────────────────
    user_input = st.chat_input(f"Your answer, {info['name']}…")

    if user_input and user_input.strip():
        st.session_state.chat_history.append({"role": "user", "text": user_input})

        # Show user bubble
        st.markdown(f"""
        <div class="bubble-row user">
            <div class="bubble user">{user_input}</div>
            <div class="avatar user-av">🧑‍💻</div>
        </div>""", unsafe_allow_html=True)

        # Typing indicator
        ph = st.empty()
        ph.markdown("""
        <div class="bubble-row bot">
            <div class="avatar bot-av">🤖</div>
            <div class="bubble bot">
                <div class="typing-wrap">
                    <div class="dot"></div><div class="dot"></div><div class="dot"></div>
                </div>
            </div>
        </div>""", unsafe_allow_html=True)

        # Build full conversation context for the model
        full_input = ""
        for m in st.session_state.chat_history:
            prefix = f"{info['name']}: " if m["role"] == "user" else "Interviewer: "
            full_input += prefix + m["text"] + "\n"

        prompt = TEMPLATE.invoke({
            **info,
            "user_input": full_input
        })
        response = st.session_state.model.invoke(prompt)
        bot_text = response.content

        st.session_state.chat_history.append({"role": "bot", "text": bot_text})
        st.session_state.q_count += 1

        ph.markdown(f"""
        <div class="bubble-row bot">
            <div class="avatar bot-av">🤖</div>
            <div class="bubble bot">{bot_text}</div>
        </div>""", unsafe_allow_html=True)