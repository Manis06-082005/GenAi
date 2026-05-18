import streamlit as st
from dotenv import load_dotenv
from langchain_mistralai import ChatMistralAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel
from typing import List, Optional

load_dotenv()

# ── Schema ────────────────────────────────────────────────────────────────────
class CvScanner(BaseModel):
    name: str
    Job_title: str
    experience: Optional[str]
    skills: List[str]
    projects: Optional[List[str]]
    email: Optional[str]
    linkedin: Optional[str]
    github: Optional[str]
    summary: Optional[str]
    match_score: Optional[int]

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="CV Scanner AI",
    page_icon="📋",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Mono:wght@300;400;500&display=swap');

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body, [data-testid="stAppViewContainer"] {
    background: #0d0d0f !important;
    color: #e8e6e1 !important;
    font-family: 'DM Mono', monospace;
}
[data-testid="stAppViewContainer"] {
    background:
        radial-gradient(ellipse 80% 50% at 50% -10%, rgba(255,180,0,0.07) 0%, transparent 60%),
        #0d0d0f !important;
}
[data-testid="stHeader"] { background: transparent !important; }

/* ── Hero ── */
.hero { text-align: center; padding: 3rem 1rem 1.5rem; }
.hero-badge {
    display: inline-block;
    background: rgba(255,180,0,0.12);
    border: 1px solid rgba(255,180,0,0.35);
    color: #ffb400;
    font-family: 'DM Mono', monospace;
    font-size: 0.68rem;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    padding: 0.3rem 1rem;
    border-radius: 2rem;
    margin-bottom: 1.2rem;
}
.hero h1 {
    font-family: 'Syne', sans-serif;
    font-weight: 800;
    font-size: clamp(2.2rem, 5vw, 3.6rem);
    line-height: 1.05;
    letter-spacing: -0.02em;
    color: #f0ece4;
    margin-bottom: 0.7rem;
}
.hero h1 span { color: #ffb400; }
.hero p { color: #6a6860; font-size: 0.88rem; max-width: 500px; margin: 0 auto; line-height: 1.7; }

/* ── Divider ── */
.divider { border: none; border-top: 1px solid rgba(255,255,255,0.06); margin: 1.8rem 0; }

/* ── Column labels ── */
.col-label {
    font-family: 'Syne', sans-serif;
    font-size: 0.72rem;
    font-weight: 700;
    letter-spacing: 0.16em;
    text-transform: uppercase;
    color: #ffb400;
    margin-bottom: 0.5rem;
}

/* ── Textareas ── */
[data-testid="stTextArea"] textarea {
    background: rgba(255,255,255,0.03) !important;
    border: 1px solid rgba(255,255,255,0.09) !important;
    border-radius: 12px !important;
    color: #e8e6e1 !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 0.83rem !important;
    line-height: 1.7 !important;
    padding: 1rem !important;
    transition: border-color 0.2s, box-shadow 0.2s;
    resize: vertical;
}
[data-testid="stTextArea"] textarea:focus {
    border-color: rgba(255,180,0,0.45) !important;
    box-shadow: 0 0 0 3px rgba(255,180,0,0.07) !important;
    outline: none !important;
}

/* ── Button ── */
[data-testid="stButton"] button {
    background: #ffb400 !important;
    color: #0d0d0f !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
    font-size: 0.88rem !important;
    letter-spacing: 0.04em !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 0.65rem 2rem !important;
    width: 100% !important;
    transition: background 0.2s, transform 0.1s !important;
}
[data-testid="stButton"] button:hover { background: #ffc733 !important; transform: translateY(-1px) !important; }
[data-testid="stButton"] button:active { transform: translateY(0) !important; }

/* ── Score ring ── */
.score-wrapper {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 1.6rem 1rem;
    background: rgba(255,255,255,0.025);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 16px;
    height: 100%;
    min-height: 180px;
}
.score-ring { position: relative; width: 110px; height: 110px; }
.score-ring svg { transform: rotate(-90deg); }
.score-ring .bg-circle { fill: none; stroke: rgba(255,255,255,0.07); stroke-width: 8; }
.score-ring .fg-circle { fill: none; stroke-width: 8; stroke-linecap: round; }
.score-center {
    position: absolute; inset: 0;
    display: flex; flex-direction: column;
    align-items: center; justify-content: center;
}
.score-number { font-family: 'Syne', sans-serif; font-size: 1.9rem; font-weight: 800; line-height: 1; }
.score-denom { font-family: 'DM Mono', monospace; font-size: 0.62rem; color: #5a5852; margin-top: 0.1rem; }
.score-label {
    font-family: 'Syne', sans-serif; font-size: 0.7rem; font-weight: 700;
    letter-spacing: 0.16em; text-transform: uppercase; color: #ffb400; margin-top: 0.9rem;
}
.score-verdict { font-family: 'DM Mono', monospace; font-size: 0.75rem; color: #6a6860; margin-top: 0.3rem; text-align: center; }

/* ── Cards ── */
.result-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 0.9rem; margin-top: 1rem; }
.card {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 14px;
    padding: 1.2rem 1.4rem;
    transition: border-color 0.2s;
}
.card:hover { border-color: rgba(255,180,0,0.22); }
.card-label {
    font-family: 'Syne', sans-serif; font-size: 0.66rem; font-weight: 700;
    letter-spacing: 0.18em; text-transform: uppercase; color: #ffb400; margin-bottom: 0.5rem;
}
.card-value { font-family: 'DM Mono', monospace; font-size: 0.88rem; color: #e8e6e1; line-height: 1.55; }
.card-wide { grid-column: 1 / -1; }

/* ── Tags ── */
.tags { display: flex; flex-wrap: wrap; gap: 0.4rem; margin-top: 0.3rem; }
.tag {
    background: rgba(255,180,0,0.1); border: 1px solid rgba(255,180,0,0.25);
    color: #ffb400; font-family: 'DM Mono', monospace; font-size: 0.72rem;
    padding: 0.22rem 0.7rem; border-radius: 2rem;
}

/* ── Links ── */
.link-row { display: flex; flex-direction: column; gap: 0.4rem; margin-top: 0.3rem; }
.link-chip { display: inline-flex; align-items: center; gap: 0.35rem; color: #7dd3fc; font-size: 0.8rem; text-decoration: none; word-break: break-all; }
.link-chip:hover { color: #bae6fd; }

/* ── Projects ── */
.project-item { display: flex; gap: 0.6rem; align-items: flex-start; padding: 0.45rem 0; border-bottom: 1px solid rgba(255,255,255,0.05); }
.project-item:last-child { border-bottom: none; }
.project-bullet { color: #ffb400; font-size: 0.68rem; margin-top: 0.28rem; flex-shrink: 0; }

/* ── Section title ── */
.section-title { font-family: 'Syne', sans-serif; font-size: 1.1rem; font-weight: 700; color: #f0ece4; margin-bottom: 0.2rem; }
.section-sub { color: #5a5852; font-size: 0.75rem; }

[data-testid="stSpinner"] { color: #ffb400 !important; }
[data-testid="stAlert"] {
    background: rgba(255,180,0,0.06) !important;
    border: 1px solid rgba(255,180,0,0.2) !important;
    border-radius: 10px !important;
    color: #e8e6e1 !important;
}
#MainMenu, footer, [data-testid="stToolbar"] { visibility: hidden; }
</style>
""", unsafe_allow_html=True)


# ── Helpers ───────────────────────────────────────────────────────────────────
def score_color(score: int) -> str:
    if score >= 8:   return "#22c55e"
    elif score >= 5: return "#ffb400"
    else:            return "#f87171"

def score_verdict(score: int) -> str:
    if score >= 9:   return "Excellent match"
    elif score >= 7: return "Strong match"
    elif score >= 5: return "Moderate match"
    elif score >= 3: return "Weak match"
    else:            return "Poor match"

def score_ring_html(score: int) -> str:
    s = max(0, min(10, score))
    r = 46
    circumference = 2 * 3.14159 * r
    offset = circumference * (1 - s / 10)
    color = score_color(s)
    return f"""
    <div class="score-wrapper">
      <div class="score-ring">
        <svg width="110" height="110" viewBox="0 0 110 110">
          <circle class="bg-circle" cx="55" cy="55" r="{r}"/>
          <circle class="fg-circle" cx="55" cy="55" r="{r}"
            stroke="{color}"
            stroke-dasharray="{circumference:.1f}"
            stroke-dashoffset="{offset:.1f}"/>
        </svg>
        <div class="score-center">
          <span class="score-number" style="color:{color}">{s}</span>
          <span class="score-denom">/ 10</span>
        </div>
      </div>
      <div class="score-label">Match Score</div>
      <div class="score-verdict">{score_verdict(s)}</div>
    </div>"""


# ── Hero ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div class="hero-badge">✦ Powered by Mistral AI</div>
    <h1>CV <span>Scanner</span> AI</h1>
    <p>Paste a CV and a job description — get instant structured extraction plus a match score out of 10.</p>
</div>
<hr class="divider"/>
""", unsafe_allow_html=True)

# ── Inputs ────────────────────────────────────────────────────────────────────
_, center, _ = st.columns([0.5, 6, 0.5])

with center:
    col_cv, col_jd = st.columns(2, gap="large")

    with col_cv:
        st.markdown('<div class="col-label">📄 CV Content</div>', unsafe_allow_html=True)
        cv_content = st.text_area(
            label="CV",
            placeholder="Paste the full CV text here — work experience, education, skills, contact details…",
            height=260,
            label_visibility="collapsed",
            key="cv_input",
        )

    with col_jd:
        st.markdown('<div class="col-label">💼 Job Description</div>', unsafe_allow_html=True)
        job_description = st.text_area(
            label="Job Description",
            placeholder="Paste the job description here — role, requirements, responsibilities, preferred skills…",
            height=260,
            label_visibility="collapsed",
            key="jd_input",
        )

    st.markdown("<div style='height:0.8rem'></div>", unsafe_allow_html=True)
    scan_btn = st.button("⚡  Scan & Match CV", use_container_width=True)

# ── Processing ────────────────────────────────────────────────────────────────
if scan_btn:
    if not cv_content.strip():
        st.warning("Please paste CV content before scanning.")
    elif not job_description.strip():
        st.warning("Please paste a job description before scanning.")
    else:
        with st.spinner("Analysing CV and matching against job description…"):
            try:
                parser = PydanticOutputParser(pydantic_object=CvScanner)
                model = ChatMistralAI(model_name="mistral-small-latest")

                prompt_template = ChatPromptTemplate.from_messages([
                    ("system", """
You are a CV Scanner AI designed to extract structured information from unstructured CV text.

Your task is to analyze the provided CV content and extract:
- candidate name
- job title
- experience
- skills
- projects
- contact information (email, LinkedIn, GitHub)
- brief summary
- match_score: an integer from 0 to 10 rating how well the CV matches the job description

{format_instructions}
"""),
                    ("human", "CV:\n{CV_content}\n\nJob Description:\n{job_description}"),
                ])

                formatted_prompt = prompt_template.invoke({
                    "CV_content": cv_content,
                    "job_description": job_description,
                    "format_instructions": parser.get_format_instructions(),
                })

                response = model.invoke(formatted_prompt)
                result: CvScanner = parser.parse(response.content)

                # ── Results ───────────────────────────────────────────────────
                st.markdown('<hr class="divider"/>', unsafe_allow_html=True)
                _, res_center, _ = st.columns([0.5, 6, 0.5])

                with res_center:
                    hdr_col, score_col = st.columns([3, 1], gap="large")

                    with hdr_col:
                        st.markdown(
                            f'<div class="section-title">✦ {result.name}</div>'
                            f'<div class="section-sub">{result.Job_title}</div>',
                            unsafe_allow_html=True,
                        )
                        if result.summary:
                            st.markdown(f"""
                            <div class="result-grid">
                              <div class="card card-wide">
                                <div class="card-label">Summary</div>
                                <div class="card-value">{result.summary}</div>
                              </div>
                            </div>""", unsafe_allow_html=True)

                    with score_col:
                        score_val = result.match_score if result.match_score is not None else 0
                        st.markdown(score_ring_html(score_val), unsafe_allow_html=True)

                    # Experience + Contact
                    contact_html = ""
                    if result.email:
                        contact_html += f'<a class="link-chip" href="mailto:{result.email}">✉ {result.email}</a>'
                    if result.linkedin:
                        contact_html += f'<a class="link-chip" href="{result.linkedin}" target="_blank">🔗 LinkedIn</a>'
                    if result.github:
                        contact_html += f'<a class="link-chip" href="{result.github}" target="_blank">🐙 GitHub</a>'

                    exp_html = result.experience or "<span style='color:#5a5852'>Not specified</span>"

                    st.markdown(f"""
                    <div class="result-grid">
                      <div class="card">
                        <div class="card-label">Experience</div>
                        <div class="card-value">{exp_html}</div>
                      </div>
                      <div class="card">
                        <div class="card-label">Contact</div>
                        <div class="link-row">{contact_html or '<span style="color:#5a5852">None found</span>'}</div>
                      </div>
                    </div>""", unsafe_allow_html=True)

                    # Skills
                    if result.skills:
                        tags_html = "".join(f'<span class="tag">{s}</span>' for s in result.skills)
                        st.markdown(f"""
                        <div class="result-grid">
                          <div class="card card-wide">
                            <div class="card-label">Skills</div>
                            <div class="tags">{tags_html}</div>
                          </div>
                        </div>""", unsafe_allow_html=True)

                    # Projects
                    if result.projects:
                        projects_html = "".join(
                            f'<div class="project-item"><span class="project-bullet">▸</span>'
                            f'<span class="card-value">{p}</span></div>'
                            for p in result.projects
                        )
                        st.markdown(f"""
                        <div class="result-grid">
                          <div class="card card-wide">
                            <div class="card-label">Projects</div>
                            {projects_html}
                          </div>
                        </div>""", unsafe_allow_html=True)

                    # Raw JSON
                    with st.expander("🔍 View raw JSON output"):
                        st.code(result.model_dump_json(indent=2), language="json")

            except Exception as e:
                st.error(f"Something went wrong: {e}")
                