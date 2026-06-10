import streamlit as st
import pandas as pd
import numpy as np
import re
import plotly.express as px
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

from utils.helpers import load_esafety_data

st.set_page_config(page_title="EADCA E-Safety Predictor", page_icon="🔒", layout="wide")

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

st.markdown('<p class="page-title">🔒 Teen E-Safety Risk Predictor</p>', unsafe_allow_html=True)
st.markdown(
    '<p class="page-sub">Predict online safety risk categories for teen profiles using a Random Forest machine learning classifier.</p>',
    unsafe_allow_html=True,
)

# Load data
try:
    df_raw = load_esafety_data()
except Exception as e:
    st.error(f"Error loading e-safety dataset: {e}")
    st.info("Ensure that `data/teen_e_safety_dataset.csv` is present.")
    st.stop()

# Train model (cached)
@st.cache_resource
def train_esafety_model(df):
    df_clean = df.copy()
    
    # Map ordinal variables to numeric
    df_clean['Social_Media_Usage_num'] = df_clean['Social_Media_Usage'].map({'Low':0, 'Medium':1, 'High':2}).fillna(0)
    df_clean['Education_Content_Usage_num'] = df_clean['Education_Content_Usage'].map({'None':0, 'Low':1, 'High':2}).fillna(0)
    df_clean['Peer_Interactions_num'] = df_clean['Peer_Interactions'].map({'Low':0, 'Medium':1, 'High':2}).fillna(0)
    df_clean['E_Safety_Awareness_Score_num'] = df_clean['E_Safety_Awareness_Score'].map({'Low':0.33, 'Moderate':0.66, 'High':1.0}).fillna(0.5)
    
    num_features = [
        'Malware_Detection', 'Phishing_Attempts', 'Social_Media_Usage_num', 'VPN_Usage', 
        'Cyberbullying_Reports', 'Parental_Control_Alerts', 'Firewall_Logs', 'Login_Attempts',
        'Download_Risk', 'Data_Breach_Notifications', 'Online_Purchase_Risk', 'Education_Content_Usage_num',
        'Public_Network_Usage', 'Hours_Online', 'Website_Visits', 'Peer_Interactions_num',
        'Risky_Website_Visits', 'Cloud_Service_Usage', 'Unencrypted_Traffic', 'Ad_Clicks',
        'Insecure_Login_Attempts', 'E_Safety_Awareness_Score_num', 'Malware_Exposure_Risk'
    ]
    cat_features = ['Device_Type', 'Password_Strength', 'Age_Group', 'Geolocation', 'Network_Type']
    
    X = df_clean[num_features + cat_features]
    y = df_clean['Cybersecurity_Behavior_Category']
    
    le_y = LabelEncoder()
    y_encoded = le_y.fit_transform(y)
    
    preprocessor = ColumnTransformer([
        ('num', StandardScaler(), num_features),
        ('cat', OneHotEncoder(handle_unknown='ignore', sparse_output=False), cat_features)
    ])
    
    model = Pipeline([
        ('preprocessor', preprocessor),
        ('classifier', RandomForestClassifier(n_estimators=50, random_state=42))
    ])
    
    X_train, X_test, y_train, y_test = train_test_split(X, y_encoded, test_size=0.2, random_state=42)
    model.fit(X_train, y_train)
    
    accuracy = model.score(X_test, y_test)
    
    # Calculate feature importances
    cat_encoder = model.named_steps['preprocessor'].named_transformers_['cat']
    onehot_features = list(cat_encoder.get_feature_names_out(cat_features))
    all_feature_names = num_features + onehot_features
    importances = model.named_steps['classifier'].feature_importances_
    
    importance_df = pd.DataFrame({
        'Feature': all_feature_names,
        'Importance': importances
    }).sort_values(by='Importance', ascending=False)
    
    return model, le_y, accuracy, importance_df

# Train Model
with st.spinner("Training Random Forest Classifier on E-Safety dataset..."):
    try:
        model, le_y, accuracy, importance_df = train_esafety_model(df_raw)
    except Exception as e:
        st.error(f"Error training model: {e}")
        st.stop()

# Sidebar Stats
st.sidebar.markdown("### 📈 Model Evaluation")
st.sidebar.metric("Classifier Accuracy", f"{accuracy * 100:.1f}%")
st.sidebar.metric("Dataset Rows", f"{len(df_raw):,}")

# Layout Tabs
tab1, tab2, tab3 = st.tabs(["📋 Form-based Assessment", "💬 Chat-based Assessment", "📊 Feature Importance"])

# --- Tab 1: Form-based Assessment ---
with tab1:
    st.markdown("### Quick Profile Assessment")
    st.write("Fill in the profile details below to predict the online safety risk level.")
    
    with st.form("esafety_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("##### 👤 Demographics")
            age = st.slider("Age:", min_value=12, max_value=20, value=15)
            device_type = st.selectbox("Device Type:", ["Mobile", "Laptop", "Desktop", "Tablet"])
            network_type = st.selectbox("Network Type:", ["WiFi", "Cellular", "Ethernet"])
            geolocation = st.selectbox("Geolocation Country Code:", ["US", "IN", "UK", "CA", "AU"])
            
            st.markdown("##### ⚙️ Technical Controls")
            vpn_usage = st.selectbox("VPN Usage (0=No, 1=Yes):", [0, 1])
            password_strength = st.selectbox("Password Strength:", ["Weak", "Medium", "Strong"])
            public_network = st.selectbox("Public Network Usage (0=No, 1=Yes):", [0, 1])
            
        with col2:
            st.markdown("##### 🌐 Activity Details")
            hours_online = st.slider("Hours Online Daily:", min_value=0.0, max_value=24.0, value=3.0, step=0.5)
            social_media = st.selectbox("Social Media Usage Level:", ["Low", "Medium", "High"])
            edu_content = st.selectbox("Educational Content Usage Level:", ["None", "Low", "High"])
            peer_interactions = st.selectbox("Peer Interactions Level:", ["Low", "Medium", "High"])
            
            st.markdown("##### 🚨 Risks & Alerts")
            malware_det = st.slider("Malware Detections (Last 30 Days):", min_value=0, max_value=10, value=0)
            phishing_att = st.slider("Phishing Attempts Encountered:", min_value=0, max_value=20, value=0)
            parental_alerts = st.slider("Parental Control Alerts:", min_value=0, max_value=10, value=0)
            esafety_score = st.slider("E-Safety Awareness Score (0 to 1):", min_value=0.0, max_value=1.0, value=0.8, step=0.05)
            
        submitted = st.form_submit_button("Predict Safety Category", use_container_width=True)

    if submitted:
        # Construct prediction DataFrame
        age_group = '13-16' if age <= 16 else '17-19'
        pred_data = {
            'Device_Type': device_type, 'Password_Strength': password_strength, 'Age_Group': age_group,
            'Geolocation': geolocation, 'Network_Type': network_type,
            'Malware_Detection': malware_det, 'Phishing_Attempts': phishing_att, 'Social_Media_Usage': social_media,
            'VPN_Usage': vpn_usage, 'Cyberbullying_Reports': phishing_att // 2, 'Parental_Control_Alerts': parental_alerts,
            'Firewall_Logs': 2, 'Login_Attempts': 2, 'Download_Risk': malware_det * 2,
            'Data_Breach_Notifications': malware_det, 'Online_Purchase_Risk': 0, 'Education_Content_Usage': edu_content,
            'Public_Network_Usage': public_network, 'Hours_Online': hours_online,
            'Website_Visits': 5, 'Peer_Interactions': peer_interactions, 'Risky_Website_Visits': (phishing_att * 2) + (malware_det * 2),
            'Cloud_Service_Usage': 0, 'Unencrypted_Traffic': 1 if public_network else 0, 'Ad_Clicks': 0,
            'Insecure_Login_Attempts': phishing_att, 'E_Safety_Awareness_Score': esafety_score, 'Malware_Exposure_Risk': malware_det * 3
        }
        
        pred_df = pd.DataFrame([pred_data])
        pred_df['Social_Media_Usage_num'] = pred_df['Social_Media_Usage'].map({'Low':0, 'Medium':1, 'High':2}).fillna(0)
        pred_df['Education_Content_Usage_num'] = pred_df['Education_Content_Usage'].map({'None':0, 'Low':1, 'High':2}).fillna(0)
        pred_df['Peer_Interactions_num'] = pred_df['Peer_Interactions'].map({'Low':0, 'Medium':1, 'High':2}).fillna(0)
        pred_df['E_Safety_Awareness_Score_num'] = pred_df['E_Safety_Awareness_Score']
        
        # Select features
        num_features = [
            'Malware_Detection', 'Phishing_Attempts', 'Social_Media_Usage_num', 'VPN_Usage', 
            'Cyberbullying_Reports', 'Parental_Control_Alerts', 'Firewall_Logs', 'Login_Attempts',
            'Download_Risk', 'Data_Breach_Notifications', 'Online_Purchase_Risk', 'Education_Content_Usage_num',
            'Public_Network_Usage', 'Hours_Online', 'Website_Visits', 'Peer_Interactions_num',
            'Risky_Website_Visits', 'Cloud_Service_Usage', 'Unencrypted_Traffic', 'Ad_Clicks',
            'Insecure_Login_Attempts', 'E_Safety_Awareness_Score_num', 'Malware_Exposure_Risk'
        ]
        cat_features = ['Device_Type', 'Password_Strength', 'Age_Group', 'Geolocation', 'Network_Type']
        
        X_pred = pred_df[num_features + cat_features]
        
        prediction = model.predict(X_pred)[0]
        prob = model.predict_proba(X_pred)[0]
        category = le_y.inverse_transform([prediction])[0]
        
        risk_emoji = "🟢 Safe" if category == "Safe" else "🟡 Neutral" if category == "Neutral" else "🔴 Risky"
        color = "green" if category == "Safe" else "orange" if category == "Neutral" else "red"
        
        st.markdown("### 📊 Prediction Result")
        st.markdown(f"**Predicted Category:** :{color}[{risk_emoji}]")
        st.markdown(f"**Confidence:** {max(prob)*100:.0f}%")
        
        # Advice
        if category == 'Safe':
            st.success("✅ Student exhibits safe cybersecurity habits! Keep up the good work.")
        elif category == 'Neutral':
            st.info("⚠️ Moderate safety risk. Recommended actions: Enable VPN on public networks and run regular antivirus scans.")
        else:
            st.error("🚨 High safety risk detected! Immediate actions required: Install a firewall/antivirus, enforce strong passwords, and reduce exposure to risky sites.")

# --- Tab 2: Chat-based Assessment ---
with tab2:
    st.markdown("### Natural Language Assistant")
    st.write("Type a profile description in natural language and press Enter. (e.g. `risk for 16yo mobile WiFi 6hrs`)")
    
    # Initialize message list
    if "esafety_chat_messages" not in st.session_state:
        st.session_state.esafety_chat_messages = [
            {"role": "assistant", "content": "Hello! I can evaluate online safety risk. Provide a prompt containing age, device (mobile/laptop/desktop/tablet), network type (WiFi/cellular/ethernet), and hours online. I'll predict the risk status."}
        ]

    # Render previous messages
    for msg in st.session_state.esafety_chat_messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Chat Input
    if chat_prompt := st.chat_input("Enter profile details...", key="esafety_chat_input"):
        st.session_state.esafety_chat_messages.append({"role": "user", "content": chat_prompt})
        with st.chat_message("user"):
            st.markdown(chat_prompt)

        with st.chat_message("assistant"):
            # Parsing numbers (first is age, second is hours)
            numbers = re.findall(r'\d+(?:\.\d+)?', chat_prompt)
            age = 15
            hours = 3.0
            if len(numbers) >= 1:
                try:
                    age = int(float(numbers[0]))
                except ValueError:
                    pass
            if len(numbers) >= 2:
                try:
                    hours = float(numbers[1])
                except ValueError:
                    pass
                    
            age_group = '13-16' if age <= 16 else '17-19'
            
            # Device type parsing
            device_match = re.search(r'(mobile|phone|tablet|laptop|desktop)', chat_prompt.lower())
            device_type = device_match.group(1).capitalize() if device_match else 'Mobile'
            
            # Network type parsing
            network_match = re.search(r'(wifi|cellular|data|ethernet)', chat_prompt.lower())
            network_type = network_match.group(1).capitalize() if network_match else 'WiFi'
            
            # Threat parsing
            malware_match = re.search(r'malware.*?(\d+)', chat_prompt.lower())
            malware_det = int(malware_match.group(1)) if malware_match else 0
            phishing_match = re.search(r'phishing.*?(\d+)', chat_prompt.lower())
            phishing_att = int(phishing_match.group(1)) if phishing_match else 0
            
            # Prediction
            pred_data = {
                'Device_Type': device_type, 'Password_Strength': 'Weak', 'Age_Group': age_group,
                'Geolocation': 'US', 'Network_Type': network_type,
                'Malware_Detection': malware_det, 'Phishing_Attempts': phishing_att, 'Social_Media_Usage': 'Low',
                'VPN_Usage': 0, 'Cyberbullying_Reports': phishing_att // 2, 'Parental_Control_Alerts': 0,
                'Firewall_Logs': 2, 'Login_Attempts': 2, 'Download_Risk': malware_det * 2,
                'Data_Breach_Notifications': malware_det, 'Online_Purchase_Risk': 0, 'Education_Content_Usage': 'None',
                'Public_Network_Usage': 1 if 'public' in chat_prompt.lower() else 0, 'Hours_Online': hours,
                'Website_Visits': 5, 'Peer_Interactions': 'Low', 'Risky_Website_Visits': (phishing_att * 2) + (malware_det * 2),
                'Cloud_Service_Usage': 0, 'Unencrypted_Traffic': 1 if 'public' in chat_prompt.lower() else 0, 'Ad_Clicks': 0,
                'Insecure_Login_Attempts': phishing_att, 'E_Safety_Awareness_Score': 0.4 if malware_det > 0 else 0.7, 'Malware_Exposure_Risk': malware_det * 3
            }
            
            pred_df = pd.DataFrame([pred_data])
            pred_df['Social_Media_Usage_num'] = pred_df['Social_Media_Usage'].map({'Low':0, 'Medium':1, 'High':2}).fillna(0)
            pred_df['Education_Content_Usage_num'] = pred_df['Education_Content_Usage'].map({'None':0, 'Low':1, 'High':2}).fillna(0)
            pred_df['Peer_Interactions_num'] = pred_df['Peer_Interactions'].map({'Low':0, 'Medium':1, 'High':2}).fillna(0)
            pred_df['E_Safety_Awareness_Score_num'] = pred_df['E_Safety_Awareness_Score']
            
            num_features = [
                'Malware_Detection', 'Phishing_Attempts', 'Social_Media_Usage_num', 'VPN_Usage', 
                'Cyberbullying_Reports', 'Parental_Control_Alerts', 'Firewall_Logs', 'Login_Attempts',
                'Download_Risk', 'Data_Breach_Notifications', 'Online_Purchase_Risk', 'Education_Content_Usage_num',
                'Public_Network_Usage', 'Hours_Online', 'Website_Visits', 'Peer_Interactions_num',
                'Risky_Website_Visits', 'Cloud_Service_Usage', 'Unencrypted_Traffic', 'Ad_Clicks',
                'Insecure_Login_Attempts', 'E_Safety_Awareness_Score_num', 'Malware_Exposure_Risk'
            ]
            cat_features = ['Device_Type', 'Password_Strength', 'Age_Group', 'Geolocation', 'Network_Type']
            
            X_pred = pred_df[num_features + cat_features]
            prediction = model.predict(X_pred)[0]
            prob = model.predict_proba(X_pred)[0]
            category = le_y.inverse_transform([prediction])[0]
            
            risk_emoji = "🟢 Safe" if category == "Safe" else "🟡 Neutral" if category == "Neutral" else "🔴 Risky"
            color = "green" if category == "Safe" else "orange" if category == "Neutral" else "red"
            
            response = f"""
            **Risk Prediction:** :{color}[{risk_emoji}] ({max(prob)*100:.0f}% confidence)
            
            **Extracted Profile Parameters:**
            - **Age**: {age} ({age_group} group)
            - **Device**: {device_type}
            - **Network**: {network_type}
            - **Hours Online**: {hours:.1f}
            
            **Mitigation Advice:**
            {'✅ Keep practicing safe security habits!' if category == 'Safe' else '⚠️ Recommended to enable VPN and change passwords regularly.' if category == 'Neutral' else '🚨 Critical safety warning! Install parental controls, block risky sites, and run antivirus scans.'}
            """
            st.markdown(response)
            st.session_state.esafety_chat_messages.append({"role": "assistant", "content": response})

# --- Tab 3: Feature Importance ---
with tab3:
    st.markdown("### Random Forest Feature Importance")
    st.write("Variables sorted by their predictive contribution in determining a teen's online safety risk category:")
    
    fig_importance = px.bar(
        importance_df.head(15),
        x='Importance',
        y='Feature',
        orientation='h',
        title="Top 15 Most Important Features",
        color='Importance',
        color_continuous_scale="Viridis"
    )
    fig_importance.update_layout(
        template="plotly_dark", 
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        yaxis=dict(autorange="reversed")
    )
    st.plotly_chart(fig_importance, use_container_width=True)
