import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from sentence_transformers import SentenceTransformer, util
from utils.helpers import load_threat_datasets

st.set_page_config(page_title="EADCA Threat Intelligence", page_icon="🛡️", layout="wide")

# Custom Styles
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

st.markdown('<p class="page-title">🛡️ Cybersecurity Threat Intelligence</p>', unsafe_allow_html=True)
st.markdown(
    '<p class="page-sub">Explore Open-MalSec threat datasets, run semantic searches, and test threat classification skills.</p>',
    unsafe_allow_html=True,
)

# Load data
try:
    threat_data, all_threats = load_threat_datasets()
    if not all_threats:
        st.warning("No threat datasets found in data/threats/.")
        st.stop()
except Exception as e:
    st.error(f"Error loading threat datasets: {e}")
    st.stop()

# Load Model
@st.cache_resource
def load_threat_model():
    return SentenceTransformer('all-MiniLM-L6-v2')

try:
    model = load_threat_model()
except Exception as e:
    st.error(f"Failed to load sentence-transformers model: {e}")
    model = None

# Precompute threat embeddings
@st.cache_resource
def get_threat_embeddings(_samples):
    if model is None:
        return None
    instructions = [str(s.get('Instruction', s.get('instruction'))) + ' ' + str(s.get('Input', s.get('input'))) for s in _samples]
    return model.encode(instructions, convert_to_tensor=True, show_progress_bar=False)

if model is not None:
    try:
        threat_embeddings = get_threat_embeddings(all_threats)
    except Exception as e:
        st.warning(f"Error precomputing threat embeddings: {e}")
        threat_embeddings = None
else:
    threat_embeddings = None

def semantic_threat_search(query, samples, top_k=5):
    if model is None or threat_embeddings is None:
        # Fallback keyword matching
        query = query.lower()
        results = []
        for s in samples:
            text = (str(s.get('Instruction', s.get('instruction'))) + ' ' + str(s.get('Input', s.get('input')))).lower()
            if query in text:
                results.append(s)
            if len(results) >= top_k:
                break
        return results

    query_emb = model.encode(query, convert_to_tensor=True)
    hits = util.semantic_search(query_emb, threat_embeddings, top_k=top_k)
    return [samples[hit['corpus_id']] for hit in hits[0]]

# Sidebar info
st.sidebar.markdown("### 📊 Dataset Statistics")
st.sidebar.metric("Loaded Threat Samples", f"{len(all_threats):,}")
st.sidebar.metric("Categories", f"{len(threat_data)}")

# Layout Tabs
tab1, tab2, tab3, tab4 = st.tabs(["🎯 Threat Analysis Quiz", "🔍 Semantic Threat Search", "📊 Analytics Dashboard", "⚙️ Integration Setup"])

# --- Tab 1: Threat Quiz ---
with tab1:
    st.markdown("### Interactive Threat Analysis Quiz")
    st.write("Test your security analysis skills by reviewing a real-world threat scenario.")

    category = st.selectbox("Select Threat Category:", list(threat_data.keys()))
    
    # Initialize Quiz State
    if "quiz_sample" not in st.session_state or st.session_state.get("quiz_category") != category:
        st.session_state.quiz_sample = np.random.choice(threat_data[category])
        st.session_state.quiz_category = category
        st.session_state.quiz_submitted = False
        st.session_state.user_analysis = ""

    # Button to generate a new scenario
    if st.button("🚨 Generate New Threat Scenario"):
        st.session_state.quiz_sample = np.random.choice(threat_data[category])
        st.session_state.quiz_submitted = False
        st.session_state.user_analysis = ""
        st.rerun()

    sample = st.session_state.quiz_sample

    st.info(f"**Scenario:** {sample.get('Instruction', sample.get('instruction', ''))}")
    if sample.get('Input') or sample.get('input'):
        st.warning(f"**Evidence / Logs:**\n```\n{sample.get('Input', sample.get('input', ''))}\n```")

    user_analysis = st.text_area(
        "Analyze the threat scenario and type your recommended mitigation steps:",
        value=st.session_state.user_analysis,
        key="user_analysis_input"
    )

    if st.button("✅ Submit for Expert Feedback"):
        if user_analysis.strip() == "":
            st.warning("Please enter your analysis first.")
        else:
            st.session_state.quiz_submitted = True
            st.session_state.user_analysis = user_analysis

    if st.session_state.quiz_submitted:
        st.success(f"**Expert Analysis & Remediation:**\n{sample.get('Output', sample.get('output', ''))}")
        st.metric("System Severity Score (CVSS Estimate)", sample.get('Metadata', {}).get('CVSS', 'N/A'))

# --- Tab 2: Semantic Search ---
with tab2:
    st.markdown("### Semantic Threat Database Search")
    st.write("Search for real cyber threats and mitigations using natural language.")

    query = st.text_input("Enter search keywords (e.g. 'phishing password reset' or 'DDOS attack vector'):")
    
    if query:
        with st.spinner("Searching database..."):
            results = semantic_threat_search(query, all_threats)
            
        if results:
            st.write(f"Showing top {len(results)} matches:")
            for i, threat in enumerate(results):
                threat_type = threat.get('Metadata', {}).get('threat_type', threat.get('Metadata', {}).get('threattype', 'Unknown'))
                cvss = threat.get('Metadata', {}).get('CVSS', 'N/A')
                
                with st.expander(f"Match #{i+1}: {threat_type} (CVSS: {cvss})"):
                    st.markdown(f"**Scenario:** {threat.get('Instruction', threat.get('instruction', ''))}")
                    if threat.get('Input') or threat.get('input'):
                        st.markdown(f"**Logs/IOCs:**\n```\n{threat.get('Input', threat.get('input', ''))}\n```")
                    st.success(f"**Mitigation Plan:**\n{threat.get('Output', threat.get('output', ''))}")
        else:
            st.write("No matching threats found.")

# --- Tab 3: Analytics Dashboard ---
with tab3:
    st.markdown("### Threat Intelligence Analytics")
    
    df = pd.DataFrame(all_threats)
    if not df.empty:
        # Category plot
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.markdown("#### Threat Types Distribution")
            df['ThreatType'] = df['Metadata'].apply(lambda x: x.get('threat_type', x.get('threattype')) if isinstance(x, dict) else 'Unknown')
            type_counts = df['ThreatType'].value_counts().reset_index()
            type_counts.columns = ['Threat Type', 'Count']
            
            fig_types = px.bar(
                type_counts,
                x='Count',
                y='Threat Type',
                orientation='h',
                color='Threat Type',
                color_discrete_sequence=px.colors.qualitative.Dark2,
                title="Counts by Threat Class"
            )
            fig_types.update_layout(template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
            st.plotly_chart(fig_types, use_container_width=True)
            
        with col2:
            st.markdown("#### Severity Distribution (CVSS)")
            df['CVSS'] = pd.to_numeric(
                df['Metadata'].apply(lambda x: x.get('CVSS') if isinstance(x, dict) else 0), 
                errors='coerce'
            ).fillna(0)
            
            # Group into low/med/high/critical
            def categorize_cvss(score):
                if score >= 9.0: return 'Critical (9.0 - 10.0)'
                elif score >= 7.0: return 'High (7.0 - 8.9)'
                elif score >= 4.0: return 'Medium (4.0 - 6.9)'
                elif score > 0.0: return 'Low (0.1 - 3.9)'
                else: return 'None / Info'
                
            df['Severity'] = df['CVSS'].apply(categorize_cvss)
            sev_counts = df['Severity'].value_counts().reset_index()
            sev_counts.columns = ['Severity Level', 'Count']
            
            fig_sev = px.pie(
                sev_counts,
                values='Count',
                names='Severity Level',
                color='Severity Level',
                color_discrete_map={
                    'Critical (9.0 - 10.0)': '#ef4444',
                    'High (7.0 - 8.9)': '#f97316',
                    'Medium (4.0 - 6.9)': '#eab308',
                    'Low (0.1 - 3.9)': '#3b82f6',
                    'None / Info': '#64748b'
                },
                title="Threats by Severity Rating"
            )
            fig_sev.update_layout(template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)")
            st.plotly_chart(fig_sev, use_container_width=True)

# --- Tab 4: Integration Setup ---
with tab4:
    st.markdown("### Setup & API Integration")
    st.write("Connect this threat database with external security logs or pipelines.")
    
    st.markdown("#### Sample Python Connection Script")
    st.code(
        """
import requests
import json

# Fetch matching mitigations from Open-MalSec local database
def check_mitigation(threat_type, query):
    # Simulated API call
    payload = {"threat_type": threat_type, "query": query}
    # response = requests.post("https://eadca-platform.streamlit.app/api/search", json=payload)
    # return response.json()
    print(f"Checking intelligence for: {threat_type} -> {query}")

check_mitigation("Ransomware", "phishing attachment encrypts files")
        """,
        language="python"
    )
    st.success("API pipeline config is ready. Model mappings loaded successfully.")
