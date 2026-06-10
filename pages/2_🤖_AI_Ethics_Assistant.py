import streamlit as st
import pandas as pd
import numpy as np
import os
import csv
from datetime import datetime
from utils.faq_knowledge_base import FAQ
from utils.training_modules import TRAINING_MODULES

st.set_page_config(page_title="EADCA AI Ethics Assistant", page_icon="🤖", layout="wide")

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
    .chat-container {
        border: 1px solid #334155;
        border-radius: 12px;
        background-color: #1e293b;
        padding: 1.5rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown('<p class="page-title">🤖 AI Ethics Assistant</p>', unsafe_allow_html=True)
st.markdown(
    '<p class="page-sub">Semantic Chatbot & Interactive Ethical Training Modules.</p>',
    unsafe_allow_html=True,
)

# Initialize Session Logs Setup
log_dir = "interaction_logs"
os.makedirs(log_dir, exist_ok=True)
csv_file = os.path.join(log_dir, "user_interactions.csv")

if "session_id" not in st.session_state:
    st.session_state.session_id = datetime.now().strftime("%Y%m%d_%H%M%S")

if "logs" not in st.session_state:
    st.session_state.logs = []

def log_interaction(event_type, module="", user_input="", ai_response="", quiz_correct=None, reflection=""):
    ts = datetime.now().isoformat()
    row = [ts, st.session_state.session_id, event_type, module, user_input, ai_response, quiz_correct, reflection]
    
    # Write to local CSV safely
    try:
        file_exists = os.path.exists(csv_file)
        with open(csv_file, "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            if not file_exists:
                writer.writerow(["timestamp", "session_id", "event_type", "module", "user_input", "ai_response", "quiz_correct", "reflection"])
            writer.writerow(row)
    except Exception:
        pass # Ignore permission errors or file system locks in cloud

    # Write to session state
    st.session_state.logs.append({
        "timestamp": ts,
        "event_type": event_type,
        "module": module,
        "user_input": user_input,
        "ai_response": ai_response,
        "quiz_correct": quiz_correct,
        "reflection": reflection
    })

# Load embedding model and precompute FAQ embeddings
@st.cache_resource
def load_nlp_model():
    from sentence_transformers import SentenceTransformer
    return SentenceTransformer("all-MiniLM-L6-v2")

@st.cache_resource
def precompute_embeddings():
    model = load_nlp_model()
    faq_questions = list(FAQ.keys())
    embeddings = model.encode(faq_questions, convert_to_tensor=True)
    return faq_questions, embeddings

try:
    faq_questions, faq_embeddings = precompute_embeddings()
except Exception as e:
    st.error(f"Failed to load sentence-transformers model. Detail: {e}")
    # Fallback to keyword matching if SentenceTransformers fails to load
    faq_questions, faq_embeddings = None, None

def search_faq(query, threshold=0.6):
    if faq_embeddings is None:
        # Fallback keyword matching
        query = query.lower()
        best_match = None
        best_score = 0
        for k in FAQ:
            # simple Jaccard similarity fallback
            q_set = set(query.split())
            k_set = set(k.split())
            if not q_set or not k_set:
                continue
            score = len(q_set.intersection(k_set)) / len(q_set.union(k_set))
            if score > best_score:
                best_score = score
                best_match = k
        if best_score >= 0.2:
            return FAQ[best_match]
        return None

    # SentenceTransformers semantic search
    from sentence_transformers import util
    model = load_nlp_model()
    user_emb = model.encode(query, convert_to_tensor=True)
    scores = util.cos_sim(user_emb, faq_embeddings)[0]
    best_idx = np.argmax(scores.cpu().numpy())
    best_score = scores[best_idx].item()
    if best_score >= threshold:
        return FAQ[faq_questions[best_idx]]
    return None

# Tabs
tab1, tab2 = st.tabs(["💬 Chat Assistant", "🎓 Ethical Training Modules"])

# Tab 1: Chat Assistant
with tab1:
    st.markdown("### Ask any AI Ethics or Digital Literacy Question:")
    
    # Initialize message list
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "Hello! I am your AI Ethics Assistant. Ask me anything about AI ethics, cybersecurity, or digital footprint."}
        ]

    # Render previous messages
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Chat Input
    if prompt := st.chat_input("Ask a question (e.g., What is algorithmic bias?)"):
        # Display user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Generate response
        with st.chat_message("assistant"):
            with st.spinner("Analyzing query..."):
                response = search_faq(prompt)
                if not response:
                    response = "Sorry, I couldn't find a matching response in my knowledge base. Please try rephrasing or asking something like: 'What is responsible AI?'"
                st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})
                
                # Log interaction
                log_interaction(
                    event_type="chat",
                    module="AI Assistant",
                    user_input=prompt,
                    ai_response=response
                )

# Tab 2: Ethical Training Modules
with tab2:
    st.markdown("### Interactive Ethical Training Modules")
    st.write("Complete the structured training modules to learn key AI Ethics concepts.")

    module_name = st.selectbox("Select Training Module:", list(TRAINING_MODULES.keys()))
    module_data = TRAINING_MODULES[module_name]

    # Initialize state for this module
    step_key = f"step_{module_name.replace(' ', '_')}"
    if step_key not in st.session_state:
        st.session_state[step_key] = 0
        
    current_step = st.session_state[step_key]
    steps = module_data["steps"]

    if current_step < len(steps):
        step_data = steps[current_step]
        st.info(f"Step {current_step + 1} of {len(steps)}")
        
        # Display step content
        st.markdown(step_data["text"])
        
        # Action handler
        if step_data["action"] == "info":
            if st.button("Continue"):
                st.session_state[step_key] += 1
                st.rerun()
                
        elif step_data["action"] == "quiz":
            ans_key = f"quiz_ans_{module_name.replace(' ', '_')}_{current_step}"
            user_choice = st.radio("Choose your answer:", step_data["options"], key=ans_key)
            
            if st.button("Submit Answer"):
                is_correct = user_choice == step_data["correct"]
                feedback = step_data["feedback_correct"] if is_correct else step_data["feedback_incorrect"]
                st.markdown(feedback)
                log_interaction(
                    event_type="quiz",
                    module=module_name,
                    user_input=user_choice,
                    ai_response=feedback,
                    quiz_correct="correct" if is_correct else "incorrect"
                )
                st.session_state[step_key] += 1
                st.button("Next Step")
                
        elif step_data["action"] == "reflect":
            ref_key = f"reflect_{module_name.replace(' ', '_')}_{current_step}"
            reflection_text = st.text_area("Share your thoughts/reflection:", key=ref_key)
            
            if st.button("Submit Reflection"):
                if reflection_text.strip():
                    log_interaction(
                        event_type="reflection",
                        module=module_name,
                        reflection=reflection_text
                    )
                    st.success("Reflection recorded!")
                    st.session_state[step_key] += 1
                    st.rerun()
                else:
                    st.warning("Please type a reflection before submitting.")
    else:
        st.success(f"🎉 Congratulations! You have successfully completed the '{module_name}' module!")
        if st.button("Restart Module"):
            st.session_state[step_key] = 0
            st.rerun()

# Display Session Interaction Logs
st.divider()
with st.expander("📊 Session Interaction Log"):
    if st.session_state.logs:
        log_df = pd.DataFrame(st.session_state.logs)
        st.dataframe(log_df, use_container_width=True)
    else:
        st.caption("No interactions logged in this session yet.")
