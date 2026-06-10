"""
Shared helper utilities for the EADCA platform.

Provides data loading functions, path resolution, and shared constants.
"""

import os
import json
import pandas as pd
import streamlit as st

# ---------------------------------------------------------------------------
# Path helpers
# ---------------------------------------------------------------------------

def get_base_path():
    """Return the base directory of the app (where app.py lives)."""
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def get_data_path(*parts):
    """Return an absolute path under the data/ directory."""
    return os.path.join(get_base_path(), "data", *parts)


# ---------------------------------------------------------------------------
# Data loaders (cached)
# ---------------------------------------------------------------------------

@st.cache_data
def load_survey_data():
    """Load the primary survey responses Excel file."""
    path = get_data_path("survey_responses.xlsx")
    df = pd.read_excel(path, sheet_name=0)
    return df


@st.cache_data
def load_threat_datasets():
    """Load all Open-MalSec JSON threat files from data/threats/."""
    threats_dir = get_data_path("threats")
    threat_data = {}
    all_samples = []

    if not os.path.isdir(threats_dir):
        return threat_data, all_samples

    for filename in sorted(os.listdir(threats_dir)):
        if not filename.endswith(".json"):
            continue
        filepath = os.path.join(threats_dir, filename)
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                data = json.load(f)
            if isinstance(data, list):
                threat_data[filename] = data
                all_samples.extend(data)
            elif isinstance(data, dict):
                threat_data[filename] = [data]
                all_samples.append(data)
        except Exception:
            continue

    return threat_data, all_samples


@st.cache_data
def load_esafety_data():
    """Load the teen e-safety dataset."""
    path = get_data_path("teen_e_safety_dataset.csv")
    return pd.read_csv(path)


# ---------------------------------------------------------------------------
# Topic keyword definitions (shared across analytics & assistant)
# ---------------------------------------------------------------------------

TOPIC_KEYWORDS = {
    "AI Ethics": [
        "ethics", "bias", "fairness", "privacy", "responsible ai", "ethical risks",
    ],
    "Cybersecurity Awareness": [
        "phishing", "password", "two-factor authentication", "scam", "security",
        "cybersecurity",
    ],
    "Digital Skills & Literacy": [
        "digital skills", "critical thinking", "information evaluation",
        "digital literacy",
    ],
    "Misinformation & Fact-Checking": [
        "fake news", "misinformation", "fact-check", "verify", "credible", "accuracy",
    ],
    "AI Adoption & Usage": [
        "chatgpt", "ai tools", "ai adoption", "machine learning", "automation",
        "ai-generated",
    ],
    "Privacy & Data Protection": [
        "data privacy", "personal data", "data protection", "privacy concerns",
    ],
}


def assign_topic(text: str) -> str:
    """Assign a topic label to a text string based on keyword matching."""
    text_lower = str(text).lower()
    for topic, keywords in TOPIC_KEYWORDS.items():
        if any(kw in text_lower for kw in keywords):
            return topic
    return "Other"
