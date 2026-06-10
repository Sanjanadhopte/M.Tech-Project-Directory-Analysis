import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="EADCA Competency Quiz", page_icon="🧠", layout="wide")

st.markdown(
    """
    <style>
    .page-title {
        background: linear-gradient(135deg, #38bdf8, #818cf8);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 2.5rem;
        font-weight: 800;
        margin-bottom: 0.5rem;
    }
    .page-sub {
        color: #94a3b8;
        font-size: 1.1rem;
        margin-bottom: 2rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown('<p class="page-title">🧠 Competency Assessment Quiz</p>', unsafe_allow_html=True)
st.markdown(
    '<p class="page-sub">Evaluate your real-world skills in Digital Literacy, Cybersecurity Awareness, and AI Ethics & Adoption.</p>',
    unsafe_allow_html=True,
)

questions = {
    "Digital Literacy": [
        {
            "q": "You find two conflicting online articles about the same topic. What should you do?",
            "options": {
                "a": "Pick the first article that looks detailed",
                "b": "Check the author, date, and credibility of both sources",
                "c": "Ask your friend which one is correct"
            },
            "answer": "b"
        },
        {
            "q": "A file download looks suspicious but claims to be a course update. What will you do?",
            "options": {
                "a": "Scan it or verify the sender before opening",
                "b": "Open it immediately to check what's inside",
                "c": "Forward it to others to confirm"
            },
            "answer": "a"
        },
        {
            "q": "Cloud files remain private even without setting permissions. (T/F)",
            "options": {"a": "True", "b": "False"},
            "answer": "b"
        },
        {
            "q": "You are working on a group document and notice conflicting edits. What is the most professional way to resolve it?",
            "options": {
                "a": "Delete others’ edits and keep yours",
                "b": "Use version history and discuss changes with your team",
                "c": "Save multiple copies and ignore differences"
            },
            "answer": "b"
        },
        {
            "q": "Which of the following represents a safe website?",
            "options": {"a": "http://example.com", "b": "https://example.com", "c": "example.txt"},
            "answer": "b"
        },
        {
            "q": "Which of the following is a productivity tool?",
            "options": {"a": "Google Docs", "b": "YouTube", "c": "Instagram"},
            "answer": "a"
        },
        {
            "q": "While sharing files online, which format is best for maintaining document structure?",
            "options": {"a": ".pdf", "b": ".txt", "c": ".doc"},
            "answer": "a"
        },
        {
            "q": "You see a trending post that looks fake but has thousands of shares. What should you do?",
            "options": {
                "a": "Share it since everyone else did",
                "b": "Report or verify it through trusted sources",
                "c": "Ignore it completely"
            },
            "answer": "b"
        }
    ],

    "Cybersecurity Awareness": [
        {
            "q": "You receive an email asking to update your account password through a link. What should you do?",
            "options": {
                "a": "Click the link immediately",
                "b": "Ignore it and verify directly from the official site",
                "c": "Forward it to friends to check"
            },
            "answer": "b"
        },
        {
            "q": "Which password is most secure?",
            "options": {"a": "Sanjana123", "b": "San@2025", "c": "!T9x#R1p$"},
            "answer": "c"
        },
        {
            "q": "You are using public Wi-Fi at a café. Which action is most secure?",
            "options": {
                "a": "Accessing your online banking account",
                "b": "Connecting via VPN before logging in anywhere",
                "c": "Turning off firewall for faster internet"
            },
            "answer": "b"
        },
        {
            "q": "Define phishing in one sentence (type your answer):",
            "type": "text",
            "keywords": ["fraud", "fake", "trick", "steal", "information", "data"]
        },
        {
            "q": "A friend’s account got hacked due to a weak password. What should they do first?",
            "options": {
                "a": "Reset password and enable 2FA",
                "b": "Create a new account",
                "c": "Ignore it"
            },
            "answer": "a"
        },
        {
            "q": "Cybersecurity mainly focuses on protecting what?",
            "options": {
                "a": "Data, systems, and networks",
                "b": "Only people",
                "c": "Mobile phones"
            },
            "answer": "a"
        },
        {
            "q": "Ransomware does which of the following?",
            "options": {
                "a": "Deletes files permanently",
                "b": "Encrypts files and demands payment",
                "c": "Improves system security"
            },
            "answer": "b"
        },
        {
            "q": "Multi-factor authentication adds which layer of protection?",
            "options": {
                "a": "Additional verification like OTP or fingerprint",
                "b": "Automatic login to save time",
                "c": "Password sharing with others"
            },
            "answer": "a"
        }
    ],

    "AI Ethics & Adoption": [
        {
            "q": "An AI tool ranks students unfairly. Which ethical principle is violated?",
            "options": {"a": "Fairness", "b": "Transparency", "c": "Privacy"},
            "answer": "a"
        },
        {
            "q": "An AI algorithm predicts job candidates’ success but shows bias against certain groups. What is the ethical response?",
            "options": {
                "a": "Continue using it since accuracy is high",
                "b": "Audit and retrain the model to reduce bias",
                "c": "Hide results to avoid complaints"
            },
            "answer": "b"
        },
        {
            "q": "Which is an example of responsible AI use?",
            "options": {
                "a": "Using AI results without checking bias",
                "b": "Evaluating bias before using AI output",
                "c": "Letting AI decide everything"
            },
            "answer": "b"
        },
        {
            "q": "AI models never make mistakes if data is large enough. (T/F)",
            "options": {"a": "True", "b": "False"},
            "answer": "b"
        },
        {
            "q": "Mention one ethical risk of using ChatGPT for assignments (type your answer):",
            "type": "text",
            "keywords": ["plagiarism", "bias", "misinformation", "privacy"]
        },
        {
            "q": "When creating an AI chatbot collecting user data, what must be ensured?",
            "options": {
                "a": "User consent and secure data handling",
                "b": "Collect any data freely",
                "c": "Ignore privacy"
            },
            "answer": "a"
        },
        {
            "q": "Which organization provides global AI ethics guidance (e.g., UNESCO or EU)?",
            "options": {
                "a": "UNESCO and European Union",
                "b": "Only private companies",
                "c": "No one regulates AI"
            },
            "answer": "a"
        },
        {
            "q": "What is 'algorithmic bias'?",
            "options": {
                "a": "Errors due to random system bugs",
                "b": "Bias arising from unbalanced data or design flaws",
                "c": "User input mistakes"
            },
            "answer": "b"
        }
    ]
}

def evaluate_text(answer, keywords):
    answer = answer.lower()
    return 3 if any(k in answer for k in keywords) else 1

with st.form("assessment_form"):
    st.markdown("### 📋 Complete the quiz below:")
    total_score = 0
    domain_scores = {}
    answers_given = {}

    for domain, qs in questions.items():
        st.subheader(f"🔹 {domain}")
        score = 0
        answers_given[domain] = []
        for idx, q in enumerate(qs):
            # Clean layout
            st.markdown(f"**Q{idx+1}:** {q['q']}")
            if "type" in q and q["type"] == "text":
                ans = st.text_input("", key=f"{domain}_q{idx}", placeholder="Type your answer here...")
                answers_given[domain].append(ans)
                if ans:
                    score += evaluate_text(ans, q["keywords"])
                else:
                    score += 1 # Unanswered or empty gets 1 point
            else:
                ans = st.radio("", list(q["options"].values()), key=f"{domain}_q{idx}")
                answers_given[domain].append(ans)
                if ans:
                    chosen = [k for k, v in q["options"].items() if v == ans][0]
                    score += 3 if chosen == q["answer"] else 1
        domain_scores[domain] = score
        total_score += score
        st.divider()

    submitted = st.form_submit_button("Submit Assessment", use_container_width=True)

if submitted:
    st.success("🎉 Assessment Completed Successfully!")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("### 📊 Score Summary")
        for domain, score in domain_scores.items():
            st.metric(label=domain, value=f"{score} / 24")
        
        st.divider()
        st.metric(label="Total Score", value=f"{total_score} / 72")
        
        if total_score >= 54:
            level = "High Competence"
            color = "green"
            msg = "Excellent! You possess strong knowledge in digital tools, safety practices, and AI ethics."
        elif total_score >= 37:
            level = "Moderate Competence"
            color = "orange"
            msg = "Good. You have solid foundations but could improve in specific security or ethical areas."
        else:
            level = "Needs Improvement"
            color = "red"
            msg = "Recommended to review core digital safety principles and AI ethics guidelines."
            
        st.markdown(f"**Competency Level:** :{color}[{level}]")
        st.info(msg)
        
        # Download Results
        st.markdown("#### 📥 Export Results")
        
        # Create CSV text
        report_data = []
        for domain, score in domain_scores.items():
            report_data.append({"Category": domain, "Score": score, "Max Score": 24})
        report_df = pd.DataFrame(report_data)
        csv_data = report_df.to_csv(index=False)
        
        st.download_button(
            label="Download Score CSV",
            data=csv_data,
            file_name="eadca_competency_scores.csv",
            mime="text/csv",
            use_container_width=True
        )
        
        # Create TXT text
        txt_report = f"""==================================================
EADCA COMPETENCY ASSESSMENT REPORT
==================================================
Competency Level: {level}
Total Score: {total_score} / 72
--------------------------------------------------
Domain-wise Breakdown:
"""
        for domain, score in domain_scores.items():
            txt_report += f"- {domain}: {score} / 24\n"
        txt_report += "==================================================\n"
        
        st.download_button(
            label="Download Detailed Text Report",
            data=txt_report,
            file_name="eadca_assessment_report.txt",
            mime="text/plain",
            use_container_width=True
        )

    with col2:
        st.markdown("### 🕸️ Competency Radar Chart")
        
        categories = list(domain_scores.keys())
        values = list(domain_scores.values())
        categories_radar = categories + [categories[0]]
        values_radar = values + [values[0]]
        
        fig = go.Figure()
        fig.add_trace(go.Scatterpolar(
            r=values_radar,
            theta=categories_radar,
            fill='toself',
            name='Competency Score',
            line_color='#38bdf8',
            fillcolor='rgba(56, 189, 248, 0.3)'
        ))
        
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 24],
                    gridcolor="#475569",
                    linecolor="#475569"
                ),
                angularaxis=dict(
                    gridcolor="#475569",
                    linecolor="#475569"
                ),
                bgcolor="rgba(0,0,0,0)"
            ),
            showlegend=False,
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            margin=dict(t=30, b=30, l=30, r=30)
        )
        
        st.plotly_chart(fig, use_container_width=True)
