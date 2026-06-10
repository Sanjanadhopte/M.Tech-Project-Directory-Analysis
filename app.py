"""
EADCA — Ethical AI & Digital Competency Assessment Platform

A unified multi-page Streamlit application integrating:
  1. Competency Assessment Quiz
  2. AI Ethics Chatbot & Training Modules
  3. Survey Analytics Dashboard
  4. Cybersecurity Threat Intelligence
  5. Teen E-Safety Risk Predictor

Author : Sanjana Manoj Dhopte (PRN: 202403040004)
Guide  : Mrs. Ranjana Badre
Institute: MIT Academy of Engineering, Pune
"""

import streamlit as st

st.set_page_config(
    page_title="EADCA Platform",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Sidebar ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.image(
        "https://img.icons8.com/fluency/96/artificial-intelligence.png",
        width=64,
    )
    st.markdown("### EADCA Platform")
    st.caption("Ethical AI & Digital Competency Assessment")
    st.divider()
    st.markdown(
        """
        **Navigate using the pages above ☝️**

        | Page | Description |
        |------|-------------|
        | 🧠 Assessment | Take the competency quiz |
        | 🤖 AI Assistant | Chat & learn about AI ethics |
        | 📊 Analytics | Survey data insights |
        | 🛡️ Threats | Cybersecurity threat intel |
        | 🔒 E-Safety | Teen online safety predictor |
        """
    )
    st.divider()
    st.caption("MIT Academy of Engineering, Pune")

# ── Main Landing Page ────────────────────────────────────────────────────────
st.markdown(
    """
    <style>
    .hero-title {
        background: linear-gradient(135deg, #38bdf8, #818cf8, #c084fc);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3rem;
        font-weight: 800;
        line-height: 1.2;
        margin-bottom: 0.5rem;
    }
    .hero-sub {
        color: #94a3b8;
        font-size: 1.15rem;
        margin-bottom: 2rem;
    }
    .card {
        background: #1e293b;
        border: 1px solid #334155;
        border-radius: 12px;
        padding: 1.5rem;
        height: 100%;
        transition: transform 0.2s, border-color 0.2s;
    }
    .card:hover {
        transform: translateY(-4px);
        border-color: #38bdf8;
    }
    .card-icon { font-size: 2rem; margin-bottom: 0.5rem; }
    .card-title { font-size: 1.1rem; font-weight: 700; color: #f1f5f9; margin-bottom: 0.3rem; }
    .card-desc { font-size: 0.9rem; color: #94a3b8; }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown('<p class="hero-title">Ethical AI & Digital Competency<br>Assessment Platform</p>', unsafe_allow_html=True)
st.markdown(
    '<p class="hero-sub">Bridging AI Adoption, Cybersecurity Awareness, and Digital Literacy Gaps</p>',
    unsafe_allow_html=True,
)

# ── Feature Cards ────────────────────────────────────────────────────────────
cols = st.columns(5)

cards = [
    ("🧠", "Assessment", "Test your skills across Digital Literacy, Cybersecurity, and AI Ethics"),
    ("🤖", "AI Assistant", "Chat with an ethics-aware AI and take interactive training modules"),
    ("📊", "Analytics", "Explore sentiment, topics, and factor analysis on survey data"),
    ("🛡️", "Threat Intel", "Search real-world cybersecurity threats from Open-MalSec"),
    ("🔒", "E-Safety", "Predict online safety risk levels for teen user profiles"),
]

for col, (icon, title, desc) in zip(cols, cards):
    with col:
        st.markdown(
            f"""
            <div class="card">
                <div class="card-icon">{icon}</div>
                <div class="card-title">{title}</div>
                <div class="card-desc">{desc}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

st.markdown("---")

# ── About Section ────────────────────────────────────────────────────────────
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("### 📌 About This Project")
    st.markdown(
        """
        This platform is part of an M.Tech research project that investigates the
        relationship between **digital literacy**, **cybersecurity awareness**, and
        **AI ethics adoption** among students and young professionals.

        **Key Research Findings:**
        - Digital literacy strongly predicts AI confidence (r = 0.64)
        - AI usage is weakly linked to security awareness (r = 0.35)
        - 88% of variance in AI confidence is explained by the regression model
        - Factor analysis reveals 3 latent constructs: AI skills, security practices, ethical awareness
        """
    )

with col2:
    st.markdown("### 🏗️ Tech Stack")
    st.markdown(
        """
        - **Frontend:** Streamlit
        - **NLP:** SentenceTransformers, TextBlob
        - **ML:** Scikit-learn (RandomForest, Logistic Regression, KMeans, NMF)
        - **Visualization:** Plotly, Matplotlib, Seaborn
        - **Data:** Pandas, NumPy
        """
    )

st.markdown("---")
st.caption(
    "Sanjana Manoj Dhopte · PRN: 202403040004 · "
    "Guided by Mrs. Ranjana Badre · "
    "MIT Academy of Engineering, Pune · 2025"
)
