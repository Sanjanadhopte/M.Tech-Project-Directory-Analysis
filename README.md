 An Ethical Framework and Assessment Model for Bridging AI Adoption, Cyber security and Digital Literacy Gaps

A unified, interactive, and deployment-ready Streamlit application that consolidates the scattered tools, models, and analytical components of the M.Tech research project by **Sanjana Manoj Dhopte** (PRN: 202403040004), under the guidance of **Mrs. Ranjana Badre** at **MIT Academy of Engineering, Pune**.

---

## 📂 Project Structure

```
eadca-app/
├── 📄 app.py                      ← Main landing page and global config
├── 📄 requirements.txt            ← Pinned dependencies
├── 📄 README.md                   ← Setup and deployment guide (This file)
├── 📄 .gitignore                  ← Git exclusions
├── 📄 .streamlit/
│   └── config.toml                ← Dark-blue styling configuration
│
├── 📁 pages/                      ← Application Pages
│   ├── 1_🧠_Assessment.py         ← EADCA Competency Quiz
│   ├── 2_🤖_AI_Ethics_Assistant.py ← FAQ Chatbot + Stepwise training modules
│   ├── 3_📊_Survey_Analytics.py   ← Sentiment, topic, and factor analysis dashboard
│   ├── 4_🛡️_Threat_Intelligence.py ← Open-MalSec threat intelligence search & quiz
│   └── 5_🔒_ESafety_Predictor.py  ← Teen online safety risk prediction
│
├── 📁 data/                       ← Migrated survey & machine learning datasets
│   ├── survey_responses.xlsx      ← Survey response data (128 samples)
│   ├── teen_e_safety_dataset.csv  ← Teen safety dataset (8.8 MB)
│   └── threats/                   ← Open-MalSec threat intelligence JSON files (11 files)
│
└── 📁 utils/                      ← Shared Python helper utilities
    ├── __init__.py
    ├── faq_knowledge_base.py      ← 40+ entry FAQ dictionary
    ├── training_modules.py        ← Structured training module step definitions
    └── helpers.py                 ← Data loaders & path helpers
```

---

## ⚡ Key Features

1. **🧠 Competency Assessment Quiz**: 24-question test spanning Digital Literacy, Cybersecurity, and AI Ethics. Features instant feedback, interactive Plotly radar charts, and PDF/CSV score report downloads.
2. **🤖 AI Ethics Assistant**: Chat interface powered by semantic search (`SentenceTransformers`) using a 40+ entry FAQ knowledge base. Integrates 5 interactive, step-by-step training modules with quizzes and reflection inputs.
3. **📊 Survey Analytics**: Exploratory NLP pipeline showcasing TextBlob sentiment polarity, NMF topic modeling, rule-based topic labeling, Likert correlation heatmaps, and a 3-factor exploratory factor analysis dashboard.
4. **🛡️ Cybersecurity Threat Intelligence**: Searches real-world threats and mitigations from Open-MalSec using semantic similarity. Includes a scenario-based quiz with full session-state tracking.
5. **🔒 Teen E-Safety Predictor**: Predicts risk status (Safe, Neutral, Risky) of teen profiles using a Random Forest Classifier. Supports both interactive sliders/forms and natural language parsing.

---

## 💻 Local Setup & Execution

Follow these steps to run the application locally on your Windows machine:

### 1. Clone or Navigate to Project Directory
Open PowerShell and navigate to the project directory:
```powershell
cd "d:\project mtech\eadca-app"
```

### 2. Set Up a Virtual Environment (Recommended)
Creating a virtual environment on the `D:` drive avoids filling up your primary `C:` system drive:
```powershell
# Create the virtual environment
python -m venv .venv

# Activate the virtual environment
.venv\Scripts\Activate.ps1
```

### 3. Install Dependencies
Install all required libraries using the pinned requirements file:
```powershell
pip install --no-cache-dir -r requirements.txt
```

### 4. Run the Streamlit Application
Start the server and launch the app in your browser:
```powershell
streamlit run app.py
```

---

## ☁️ Deploying to Streamlit Community Cloud

The application is fully configured for free deployment to **Streamlit Community Cloud**:

1. **Push to GitHub**: Create a repository and push the contents of `d:\project mtech\eadca-app\` to your repo.
2. **Link Streamlit Cloud**: Go to [share.streamlit.io](https://share.streamlit.io/) and log in with your GitHub account.
3. **Deploy**:
   - Select your Repository, Branch, and set the Main file path to `app.py`.
   - Click **Deploy**.
4. **Access Link**: Your application will compile and become publicly accessible at a URL resembling `https://<your-repo-name>.streamlit.app`.

---

## 🎓 Academic Attribution

- **Researcher**: Sanjana Manoj Dhopte (PRN: 202403040004)
- **Project Title**: Ethical AI & Digital Competency Assessment Platform
- **Guide**: Mrs. Ranjana Badre
- **Institution**: MIT Academy of Engineering, Alandi (D), Pune
- **Year**: 2025 - 2026
