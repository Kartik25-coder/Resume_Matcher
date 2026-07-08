

import streamlit as st
from extractor import extract_text
from matcher import get_match_score, get_skill_match_score, get_missing_keywords
from skills_list import SKILLS

st.set_page_config(page_title="Resume Matcher",
                   page_icon="📄", layout="centered")


INK = "#14171A"
INK_SOFT = "#5B6266"
PAPER = "#F2F0EA"
LINE = "#E4E2DC"
CARD = "#FFFFFF"
FIELD = "#F6F5F1"     # input backgrounds — off-white, sits quietly inside the card
GOOD = "#1C7C54"     # matched / high score
GOOD_BG = "#EAF5EF"
BAD = "#B23A48"      # missing / low score
BAD_BG = "#FBEAEC"
MID = "#B8860B"      # mid-tier score
MID_BG = "#FAF3E0"

st.markdown(
    f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,500;9..144,600&family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@500;700&display=swap');

    html, body, [class*="css"] {{
        font-family: 'Inter', -apple-system, sans-serif;
        color: {INK};
    }}

    .stApp {{
        background: {PAPER};
    }}

    /* Hide default chrome for a calmer canvas */
    #MainMenu, footer, header {{ visibility: hidden; }}

    .block-container {{
        max-width: 700px;
        margin-top: 3rem;
        margin-bottom: 3rem;
        padding: 3rem 3.2rem 3.2rem 3.2rem;
        background: {CARD};
        border-radius: 16px;
        border: 1px solid {LINE};
        box-shadow: 0 1px 2px rgba(20, 23, 26, 0.03), 0 8px 24px rgba(20, 23, 26, 0.05);
    }}

    /* ---------- Header ---------- */
    .app-eyebrow {{
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.75rem;
        letter-spacing: 0.12em;
        text-transform: uppercase;
        color: {INK_SOFT};
        margin-bottom: 0.4rem;
    }}

    .app-title {{
        font-family: 'Fraunces', serif;
        font-weight: 600;
        font-size: 2.4rem;
        line-height: 1.15;
        color: {INK};
        margin-bottom: 0.35rem;
    }}

    .app-sub {{
        font-size: 0.98rem;
        color: {INK_SOFT};
        margin-bottom: 2.2rem;
        max-width: 46ch;
    }}

    /* ---------- Inputs ---------- */
    section[data-testid="stFileUploaderDropzone"] {{
        background: {FIELD};
        border: 1.5px dashed {LINE};
        border-radius: 10px;
    }}

    .stTextArea textarea {{
        background: {FIELD};
        border: 1px solid {LINE};
        border-radius: 10px;
        font-size: 0.92rem;
        color: {INK};
    }}

    .stTextArea textarea:focus {{
        border-color: #B7B2A6;
        box-shadow: 0 0 0 3px rgba(20, 23, 26, 0.05);
    }}

    section[data-testid="stFileUploaderDropzone"] button {{
        background: {CARD};
        color: {INK};
        border: 1px solid {LINE};
        border-radius: 6px;
    }}

    section[data-testid="stFileUploaderDropzone"] button:hover {{
        border-color: {INK_SOFT};
        color: {INK};
    }}

    section[data-testid="stFileUploaderDropzone"] button p {{
        color: {INK} !important;
    }}

    /* Uploaded file row (name + size) */
    [data-testid="stFileUploaderFile"] {{
        background: {FIELD};
        border: 1px solid {LINE};
        border-radius: 8px;
        padding: 0.3rem 0.6rem;
    }}

    [data-testid="stFileUploaderFile"] * {{
        color: {INK} !important;
    }}

    [data-testid="stFileUploaderFileName"] {{
        color: {INK} !important;
    }}

    label, .stTextArea label, .stFileUploader label {{
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.72rem;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        color: {INK_SOFT} !important;
        font-weight: 500;
    }}

    /* ---------- Button ---------- */
    .stButton > button {{
        background: {INK} !important;
        color: {PAPER} !important;
        border: none !important;
        border-radius: 8px;
        padding: 0.6rem 1.6rem;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.82rem;
        letter-spacing: 0.06em;
        text-transform: uppercase;
        font-weight: 500;
        transition: opacity 0.15s ease;
        margin-top: 0.5rem;
    }}

    .stButton > button p {{
        color: {PAPER} !important;
    }}

    .stButton > button:hover,
    .stButton > button:focus,
    .stButton > button:active {{
        opacity: 0.82;
        background: {INK} !important;
        color: {PAPER} !important;
        border: none !important;
    }}

    .stButton > button:hover p,
    .stButton > button:focus p,
    .stButton > button:active p {{
        color: {PAPER} !important;
    }}

    /* ---------- Divider ---------- */
    .hr {{
        border: none;
        border-top: 1px solid {LINE};
        margin: 2.4rem 0 2rem 0;
    }}

    /* ---------- Score readout ---------- */
    .score-wrap {{
        display: flex;
        align-items: baseline;
        gap: 1.1rem;
        margin-bottom: 0.4rem;
    }}

    .score-num {{
        font-family: 'JetBrains Mono', monospace;
        font-weight: 700;
        font-size: 3.4rem;
        line-height: 1;
    }}

    .score-label {{
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.78rem;
        letter-spacing: 0.1em;
        text-transform: uppercase;
        color: {INK_SOFT};
    }}

    .score-bar-track {{
        width: 100%;
        height: 6px;
        border-radius: 3px;
        background: {LINE};
        overflow: hidden;
        margin-top: 0.9rem;
    }}

    .score-bar-fill {{
        height: 100%;
        border-radius: 3px;
    }}

    .score-sub {{
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.8rem;
        color: {INK_SOFT};
        margin-top: 0.8rem;
    }}

    .score-sub b {{
        color: {INK};
    }}

    /* ---------- Skill columns ---------- */
    .col-heading {{
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.75rem;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        color: {INK_SOFT};
        margin-bottom: 0.9rem;
    }}

    .chip {{
        display: inline-block;
        font-size: 0.86rem;
        padding: 0.32rem 0.7rem;
        border-radius: 6px;
        margin: 0 0.4rem 0.4rem 0;
        font-weight: 500;
    }}

    .chip-good {{ background: {GOOD_BG}; color: {GOOD}; }}
    .chip-bad {{ background: {BAD_BG}; color: {BAD}; }}

    .empty-note {{
        color: {INK_SOFT};
        font-size: 0.88rem;
        font-style: italic;
    }}
    </style>
    """,
    unsafe_allow_html=True,
)

# ----------------------------------------------------------------------------
# Header
# ----------------------------------------------------------------------------
st.markdown('<div class="app-eyebrow">Resume · Job Description</div>',
            unsafe_allow_html=True)
st.markdown('<div class="app-title">Match Report</div>',
            unsafe_allow_html=True)
st.markdown(
    '<div class="app-sub">Upload your resume and paste a job description. '
    'We\'ll score the overlap and show exactly which skills are covered and which are missing.</div>',
    unsafe_allow_html=True,
)

resume_file = st.file_uploader("Resume (PDF)", type="pdf")
jd_text = st.text_area("Job description", height=220,
                       placeholder="Paste the full job description here…")

analyze = st.button("Analyze match")

# ----------------------------------------------------------------------------
# Result
# ----------------------------------------------------------------------------
if analyze:
    if resume_file is None:
        st.warning("Please upload a resume PDF.")
    elif not jd_text.strip():
        st.warning("Please paste a job description.")
    else:
        with st.spinner("Analyzing…"):
            resume_text = extract_text(resume_file)

            if not resume_text.strip():
                st.error(
                    "Couldn't extract text from that PDF. Try a different file.")
            else:
                skill_score = get_skill_match_score(
                    resume_text, jd_text, SKILLS)
                overall_score = get_match_score(resume_text, jd_text)
                keywords = get_missing_keywords(resume_text, jd_text, SKILLS)

                if skill_score >= 75:
                    tone, tone_bg = GOOD, GOOD_BG
                elif skill_score >= 50:
                    tone, tone_bg = MID, MID_BG
                else:
                    tone, tone_bg = BAD, BAD_BG

                st.markdown('<hr class="hr">', unsafe_allow_html=True)

                st.markdown(
                    f"""
                    <div class="score-wrap">
                        <div class="score-num" style="color:{tone};">{skill_score}%</div>
                        <div class="score-label">Skill match</div>
                    </div>
                    <div class="score-bar-track">
                        <div class="score-bar-fill" style="width:{skill_score}%; background:{tone};"></div>
                    </div>
                    <div class="score-sub">Overall text similarity: <b>{overall_score}%</b> — reflects full-document phrasing and context, not just skill overlap.</div>
                    """,
                    unsafe_allow_html=True,
                )

                st.markdown('<hr class="hr">', unsafe_allow_html=True)

                col1, col2 = st.columns(2)

                with col1:
                    st.markdown(
                        '<div class="col-heading">Matched skills</div>', unsafe_allow_html=True)
                    if keywords["matched"]:
                        chips = "".join(
                            f'<span class="chip chip-good">{s}</span>' for s in keywords["matched"]
                        )
                        st.markdown(chips, unsafe_allow_html=True)
                    else:
                        st.markdown(
                            '<div class="empty-note">None found</div>', unsafe_allow_html=True)

                with col2:
                    st.markdown(
                        '<div class="col-heading">Missing skills</div>', unsafe_allow_html=True)
                    if keywords["missing"]:
                        chips = "".join(
                            f'<span class="chip chip-bad">{s}</span>' for s in keywords["missing"]
                        )
                        st.markdown(chips, unsafe_allow_html=True)
                    else:
                        st.markdown(
                            '<div class="empty-note">None — great match!</div>', unsafe_allow_html=True)
