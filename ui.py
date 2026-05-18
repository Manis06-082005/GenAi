from langchain_mistralai import ChatMistralAI
from dotenv import load_dotenv
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
import streamlit as st

load_dotenv()

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Manish's Happy Space 🌟",
    page_icon="🌻",
    layout="centered",
)

# ── Custom CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;700;800&family=Pacifico&display=swap');

/* ── Base ── */
html, body, [class*="css"] {
    font-family: 'Nunito', sans-serif;
}

/* ── Background ── */
.stApp {
    background: linear-gradient(135deg, #fef9f0 0%, #fff0f6 50%, #f0f4ff 100%);
    min-height: 100vh;
}

/* ── Header ── */
.chat-header {
    text-align: center;
    padding: 2rem 0 1rem;
}
.chat-header h1 {
    font-family: 'Pacifico', cursive;
    font-size: 2.4rem;
    background: linear-gradient(135deg, #ff6b9d, #ffa551, #7b61ff);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin: 0;
    line-height: 1.2;
}
.chat-header p {
    color: #888;
    font-size: 0.95rem;
    margin-top: 0.4rem;
    font-weight: 600;
    letter-spacing: 0.03em;
}

/* ── Chat container ── */
.chat-wrap {
    max-width: 680px;
    margin: 0 auto;
    padding: 0 1rem 6rem;
}

/* ── Bubbles ── */
.bubble-row {
    display: flex;
    margin-bottom: 1.2rem;
    animation: popIn 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
}
.bubble-row.user  { justify-content: flex-end; }
.bubble-row.bot   { justify-content: flex-start; }

.bubble {
    max-width: 75%;
    padding: 0.85rem 1.2rem;
    border-radius: 1.5rem;
    font-size: 0.97rem;
    line-height: 1.55;
    font-weight: 600;
    position: relative;
    word-wrap: break-word;
}
.bubble.user {
    background: linear-gradient(135deg, #7b61ff, #ff6b9d);
    color: #fff;
    border-bottom-right-radius: 0.3rem;
    box-shadow: 0 4px 18px rgba(123,97,255,0.3);
}
.bubble.bot {
    background: #fff;
    color: #333;
    border-bottom-left-radius: 0.3rem;
    box-shadow: 0 4px 18px rgba(0,0,0,0.08);
}

/* avatar */
.avatar {
    width: 36px;
    height: 36px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.1rem;
    flex-shrink: 0;
}
.avatar.bot-av  { background: linear-gradient(135deg,#ffd6eb,#c6baff); margin-right: 0.6rem; align-self:flex-end; }
.avatar.user-av { background: linear-gradient(135deg,#7b61ff,#ff6b9d); margin-left: 0.6rem;  align-self:flex-end; }

/* ── Welcome card ── */
.welcome-card {
    background: #fff;
    border-radius: 1.4rem;
    padding: 1.6rem 1.8rem;
    text-align: center;
    box-shadow: 0 6px 28px rgba(0,0,0,0.07);
    margin: 1.5rem auto 2rem;
    max-width: 460px;
}
.welcome-card .emoji { font-size: 3rem; }
.welcome-card h3 {
    margin: 0.5rem 0 0.3rem;
    font-size: 1.25rem;
    color: #333;
}
.welcome-card p {
    color: #888;
    font-size: 0.9rem;
    margin: 0;
}

/* ── Input bar ── */
.stChatInputContainer, [data-testid="stChatInput"] {
    border-radius: 2rem !important;
    border: 2px solid #e0d4ff !important;
    background: #fff !important;
    box-shadow: 0 4px 20px rgba(123,97,255,0.12) !important;
}
.stChatInputContainer:focus-within {
    border-color: #7b61ff !important;
    box-shadow: 0 4px 24px rgba(123,97,255,0.25) !important;
}

/* ── Sidebar ── */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #1a1030 0%, #2a1850 100%) !important;
}
section[data-testid="stSidebar"] * { color: #ddd !important; }
section[data-testid="stSidebar"] h2 { color: #fff !important; font-family: 'Pacifico', cursive; }
section[data-testid="stSidebar"] .stButton > button {
    background: linear-gradient(135deg,#7b61ff,#ff6b9d);
    color: #fff !important;
    border: none;
    border-radius: 2rem;
    font-weight: 700;
    width: 100%;
    padding: 0.6rem 0;
    margin-top: 0.5rem;
    cursor: pointer;
    transition: opacity 0.2s;
}
section[data-testid="stSidebar"] .stButton > button:hover { opacity: 0.85; }

/* ── Divider ── */
hr { border-color: #f0e8ff !important; }

/* ── Typing indicator ── */
.typing-dot {
    display: inline-block;
    width: 8px; height: 8px;
    background: #bbb;
    border-radius: 50%;
    animation: bounce 1.2s infinite;
    margin: 0 2px;
}
.typing-dot:nth-child(2){ animation-delay:.2s }
.typing-dot:nth-child(3){ animation-delay:.4s }

@keyframes bounce {
    0%,80%,100%{ transform:translateY(0) }
    40%{ transform:translateY(-7px) }
}
@keyframes popIn {
    from{ opacity:0; transform:scale(0.92) translateY(8px) }
    to  { opacity:1; transform:scale(1)    translateY(0)   }
}
</style>
""", unsafe_allow_html=True)


# ── Session state ──────────────────────────────────────────────────────────────
SYSTEM_PROMPT = """You are a warm, upbeat, and caring assistant helping a user named Manish 
who tends to overthink even the smallest things. Your mission:
- Gently reassure and calm any worries, big or small.
- Always add a sprinkle of positivity and encouragement.
- Keep answers clear, friendly, and never overwhelming.
- Use a warm, conversational tone—like a supportive best friend.
- End replies with a motivating thought or a light-hearted emoji when fitting."""

if "messages" not in st.session_state:
    st.session_state.messages = [SystemMessage(content=SYSTEM_PROMPT)]

if "display_messages" not in st.session_state:
    st.session_state.display_messages = []  # list of {"role": "user"/"bot", "text": "..."}

if "model" not in st.session_state:
    st.session_state.model = ChatMistralAI(
        model_name="mistral-small-latest",
        temperature=0.7,
        max_tokens=300,
    )


# ── Sidebar ────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("##  Happy Space")
    st.markdown("---")
    st.markdown("**How it works**")
    st.markdown("Just type anything on your mind — big worries, tiny doubts, or random thoughts. I'm here for all of it! ")
    st.markdown("---")
    st.markdown("**Tips**")
    st.markdown("• Be honest — no judgment here  \n• Ask anything, anytime  \n• I remember our whole chat!")
    st.markdown("---")
    if st.button(" Clear Chat"):
        st.session_state.messages = [SystemMessage(content=SYSTEM_PROMPT)]
        st.session_state.display_messages = []
        st.rerun()
    st.markdown("<br><small style='opacity:0.4'>Powered by Mistral AI ✨</small>", unsafe_allow_html=True)


# ── Header ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="chat-header">
  <h1>Manish's Happy Space 🌻</h1>
  <p>Your personal overthinking antidote — available 24/7</p>
</div>
""", unsafe_allow_html=True)


# ── Welcome card (shown only at start) ────────────────────────────────────────
if not st.session_state.display_messages:
    st.markdown("""
    <div class="welcome-card">
      <div class="emoji">🤗</div>
      <h3>Hey Manish, I'm glad you're here!</h3>
      <p>Whatever's on your mind — big or small — let's talk it through together. You've got this! 💪</p>
    </div>
    """, unsafe_allow_html=True)


# ── Render chat history ────────────────────────────────────────────────────────
for msg in st.session_state.display_messages:
    if msg["role"] == "user":
        st.markdown(f"""
        <div class="bubble-row user">
            <div class="bubble user">{msg["text"]}</div>
            <div class="avatar user-av">😊</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="bubble-row bot">
            <div class="avatar bot-av">🌻</div>
            <div class="bubble bot">{msg["text"]}</div>
        </div>
        """, unsafe_allow_html=True)


# ── Chat input ─────────────────────────────────────────────────────────────────
user_input = st.chat_input("Share what's on your mind, Manish… 💬")

if user_input and user_input.strip():
    # Add user message
    st.session_state.display_messages.append({"role": "user", "text": user_input})
    st.session_state.messages.append(HumanMessage(content=user_input))

    # Show user bubble immediately
    st.markdown(f"""
    <div class="bubble-row user">
        <div class="bubble user">{user_input}</div>
        <div class="avatar user-av">😊</div>
    </div>
    """, unsafe_allow_html=True)

    # Typing indicator
    typing_placeholder = st.empty()
    typing_placeholder.markdown("""
    <div class="bubble-row bot">
        <div class="avatar bot-av">🌻</div>
        <div class="bubble bot" style="padding:1rem 1.4rem;">
            <span class="typing-dot"></span>
            <span class="typing-dot"></span>
            <span class="typing-dot"></span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Call model
    response = st.session_state.model.invoke(st.session_state.messages)
    bot_text = response.content

    # Store AI message
    st.session_state.messages.append(AIMessage(content=bot_text))
    st.session_state.display_messages.append({"role": "bot", "text": bot_text})

    # Replace typing indicator with real response
    typing_placeholder.markdown(f"""
    <div class="bubble-row bot">
        <div class="avatar bot-av">🌻</div>
        <div class="bubble bot">{bot_text}</div>
    </div>
    """, unsafe_allow_html=True)