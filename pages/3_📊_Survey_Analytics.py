import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import NMF
from sklearn.preprocessing import LabelEncoder
from sklearn.decomposition import FactorAnalysis
from textblob import TextBlob

from utils.helpers import load_survey_data, assign_topic

st.set_page_config(page_title="EADCA Survey Analytics", page_icon="📊", layout="wide")

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

st.markdown('<p class="page-title">📊 Survey Analytics Dashboard</p>', unsafe_allow_html=True)
st.markdown(
    '<p class="page-sub">Explore sentiment distribution, topic modeling, and factor analysis on primary survey responses.</p>',
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------------------
# Data Preprocessing Functions (cached)
# ---------------------------------------------------------------------------

@st.cache_data
def preprocess_nlp_data(df):
    # Combine text columns
    text_cols = [
        "In your opinion, how can AI improve digital literacy? ",
        "What kind of digital skills or knowledge do you think students need most in today's AI-driven world? "
    ]
    # Verify columns exist
    existing_cols = [c for c in text_cols if c in df.columns]
    if not existing_cols:
        return df, "No combined text available"
        
    df = df.copy()
    df['Combined_Text'] = df[existing_cols].fillna("").astype(str).apply(lambda x: " ".join(x), axis=1)
    
    # Filter empty responses
    df['Combined_Text'] = df['Combined_Text'].apply(lambda x: x if x.strip() != "" else "No response")
    df_filtered = df[df['Combined_Text'] != "No response"].copy()
    
    # Sentiment Analysis
    df_filtered['Sentiment_Polarity'] = df_filtered['Combined_Text'].apply(lambda x: TextBlob(str(x)).sentiment.polarity)
    df_filtered['Sentiment_Label'] = df_filtered['Sentiment_Polarity'].apply(
        lambda x: 'Positive' if x > 0 else ('Negative' if x < 0 else 'Neutral')
    )
    
    # Topic Labeling (Rule-based)
    df_filtered['Topic_Label'] = df_filtered['Combined_Text'].apply(assign_topic)
    
    return df_filtered

@st.cache_data
def perform_nmf_topics(texts, n_topics=5):
    vectorizer = TfidfVectorizer(max_features=500, stop_words='english')
    tfidf = vectorizer.fit_transform(texts)
    
    nmf = NMF(n_components=n_topics, random_state=42, max_iter=1000)
    nmf.fit(tfidf)
    
    feature_names = vectorizer.get_feature_names_out()
    topics = {}
    for topic_idx, topic in enumerate(nmf.components_):
        top_words = [feature_names[i] for i in topic.argsort()[:-11:-1]]
        topics[f"Topic {topic_idx + 1}"] = top_words
    return topics

@st.cache_data
def perform_factor_analysis(df):
    cols_cyber = [
        'I always verify the authenticity of emails or links before clicking on them [Row 1]',
        'I use two-factor authentication for my accounts whenever possible.',
        'How confident are you in identifying phishing or scam content? [Row 1]'
    ]
    cols_digital_lit = [
        'I can easily find and evaluate reliable information on the internet. [Row 1]',
        "What kind of digital skills or knowledge do you think students need most in today's AI-driven world? "
    ]
    cols_ethics = [
        'I understand the ethical risks of over-relying on AI-generated content. [Row 1]'
    ]
    
    all_cols = cols_cyber + cols_digital_lit + cols_ethics
    existing_cols = [c for c in all_cols if c in df.columns]
    
    if len(existing_cols) < 2:
        return None, None
        
    df_encoded = df.copy()
    le = LabelEncoder()
    for col in existing_cols:
        df_encoded[col] = le.fit_transform(df_encoded[col].astype(str))
        
    corr_matrix = df_encoded[existing_cols].corr()
    
    # Factor Analysis
    n_components = min(3, len(existing_cols))
    fa = FactorAnalysis(n_components=n_components, random_state=42)
    fa.fit(df_encoded[existing_cols])
    
    # Loadings
    loadings = pd.DataFrame(
        fa.components_.T, 
        index=existing_cols, 
        columns=[f'Factor {i+1}' for i in range(n_components)]
    )
    
    # Simplify row labels for readability
    short_labels = {
        'I always verify the authenticity of emails or links before clicking on them [Row 1]': 'Verify Links/Emails',
        'I use two-factor authentication for my accounts whenever possible.': 'Use 2FA',
        'How confident are you in identifying phishing or scam content? [Row 1]': 'Phishing Confidence',
        'I can easily find and evaluate reliable information on the internet. [Row 1]': 'Find Info Online',
        "What kind of digital skills or knowledge do you think students need most in today's AI-driven world? ": 'Skills Needed in AI Era',
        'I understand the ethical risks of over-relying on AI-generated content. [Row 1]': 'AI Ethical Risks Awareness'
    }
    
    loadings.index = [short_labels.get(idx, idx) for idx in loadings.index]
    corr_matrix.index = [short_labels.get(idx, idx) for idx in corr_matrix.index]
    corr_matrix.columns = [short_labels.get(col, col) for col in corr_matrix.columns]
    
    return corr_matrix, loadings

# Load Data
try:
    df_raw = load_survey_data()
    df_nlp = preprocess_nlp_data(df_raw)
except Exception as e:
    st.error(f"Error loading survey responses: {e}")
    st.info("Please verify that `data/survey_responses.xlsx` is present.")
    st.stop()

# Layout Tabs
tab1, tab2, tab3 = st.tabs(["📋 Data Overview", "💬 Text & Sentiment NLP", "📈 Factor & Correlation Analysis"])

# --- Tab 1: Data Overview ---
with tab1:
    st.markdown("### Survey Data Overview")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Survey Responses", len(df_raw))
    with col2:
        st.metric("Total Variables Analyzed", len(df_raw.columns))
    with col3:
        st.metric("NLP Filtered Responses", len(df_nlp))
        
    st.subheader("Dataset Preview (First 5 Rows)")
    st.dataframe(df_raw.head(5), use_container_width=True)

# --- Tab 2: NLP & Sentiment ---
with tab2:
    col_left, col_right = st.columns([1, 1])
    
    with col_left:
        st.markdown("### Sentiment Distribution")
        sentiment_counts = df_nlp['Sentiment_Label'].value_counts().reset_index()
        sentiment_counts.columns = ['Sentiment', 'Count']
        
        fig_sent = px.bar(
            sentiment_counts,
            x='Sentiment',
            y='Count',
            color='Sentiment',
            color_discrete_map={'Positive': '#22c55e', 'Neutral': '#64748b', 'Negative': '#ef4444'},
            title="Survey Text Polarity Counts"
        )
        fig_sent.update_layout(template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig_sent, use_container_width=True)
        
    with col_right:
        st.markdown("### Topic Classification (Keyword-Based)")
        topic_counts = df_nlp['Topic_Label'].value_counts().reset_index()
        topic_counts.columns = ['Topic', 'Count']
        
        fig_topic = px.pie(
            topic_counts,
            values='Count',
            names='Topic',
            color_discrete_sequence=px.colors.qualitative.Pastel,
            title="Classification of Responses"
        )
        fig_topic.update_layout(template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig_topic, use_container_width=True)
        
    st.divider()
    
    # Topic Modeling (NMF)
    st.markdown("### Unsupervised Topic Modeling (NMF)")
    st.write("Below are the top 10 keywords representing the 5 topics extracted from the survey comments using Non-negative Matrix Factorization:")
    
    topics = perform_nmf_topics(df_nlp['Combined_Text'])
    
    cols = st.columns(5)
    for idx, (topic_name, keywords) in enumerate(topics.items()):
        with cols[idx]:
            st.markdown(f"#### 🏷️ {topic_name}")
            for kw in keywords:
                st.markdown(f"- {kw}")
                
    st.divider()
    st.markdown("### Browse Responses by Sentiment")
    selected_sent = st.radio("Select Sentiment Filter:", ["Positive", "Neutral", "Negative"], horizontal=True)
    filtered_responses = df_nlp[df_nlp['Sentiment_Label'] == selected_sent]['Combined_Text'].tolist()
    
    if filtered_responses:
        st.write(f"Showing up to 10 sample responses for **{selected_sent}** sentiment:")
        for idx, resp in enumerate(filtered_responses[:10]):
            st.info(f"**Response {idx+1}:** {resp}")
    else:
        st.write("No responses found for this sentiment.")

# --- Tab 3: Factor & Correlation Analysis ---
with tab3:
    st.markdown("### Correlation & Factor Loadings")
    
    corr_matrix, loadings = perform_factor_analysis(df_raw)
    
    if corr_matrix is not None and loadings is not None:
        col_c, col_l = st.columns([1.1, 0.9])
        
        with col_c:
            st.markdown("#### Correlation Heatmap")
            fig_heatmap = px.imshow(
                corr_matrix,
                text_auto=True,
                color_continuous_scale="RdBu_r",
                zmin=-1,
                zmax=1,
                title="Pairwise Correlation Matrix of Likert Variables"
            )
            fig_heatmap.update_layout(
                template="plotly_dark", 
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)"
            )
            st.plotly_chart(fig_heatmap, use_container_width=True)
            
        with col_l:
            st.markdown("#### Factor Loadings")
            fig_loadings = px.bar(
                loadings.reset_index(),
                x="index",
                y=list(loadings.columns),
                barmode="group",
                labels={"index": "Variable", "value": "Loading Value"},
                title="Factor Loadings (3-Factor Model)",
                color_discrete_sequence=px.colors.qualitative.Safe
            )
            fig_loadings.update_layout(
                template="plotly_dark", 
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                xaxis_tickangle=-45
            )
            st.plotly_chart(fig_loadings, use_container_width=True)
            
        st.info(
            "💡 **Interpretation Guide:**\n"
            "- **Factor 1 (AI Skills & Risks)** generally aligns with AI capability and ethical awareness.\n"
            "- **Factor 2 (Cybersecurity Practices)** groups 2FA and phishing identification competence.\n"
            "- **Factor 3 (Digital Competence)** is related to searching and evaluating online information."
        )
    else:
        st.warning("Could not perform factor analysis due to missing survey variables in the loaded file.")
