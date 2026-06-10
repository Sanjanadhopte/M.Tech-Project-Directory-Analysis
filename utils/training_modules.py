"""
Ethical Training Modules — Structured data for Streamlit rendering.

Each module contains steps with text content, action type, and optional
quiz feedback. Converted from CLI print/input to Streamlit-compatible data.
"""

TRAINING_MODULES = {
    "Bias and Fairness in AI": {
        "icon": "⚖️",
        "description": "Learn how bias in AI can lead to unfair treatment and how to mitigate it.",
        "steps": [
            {
                "text": (
                    "**Why does fairness matter in AI?**\n\n"
                    "Bias in AI can lead to unfair treatment of individuals or groups "
                    "due to data or algorithmic issues.\n\n"
                    "**Example:** An AI hiring system favoring certain demographics unfairly."
                ),
                "action": "info",
            },
            {
                "text": "**Quiz:** Is an AI that declines applicants based on gender bias-free?",
                "action": "quiz",
                "options": ["Yes", "No"],
                "correct": "No",
                "feedback_correct": "✅ Correct! That AI exhibits bias and fairness concerns.",
                "feedback_incorrect": "❌ Incorrect. Gender-based decisions are a critical ethical issue — this AI is biased.",
            },
            {
                "text": "**Reflection:** Have you encountered or observed AI bias? How did it affect outcomes?",
                "action": "reflect",
            },
            {
                "text": "💡 **Takeaway:** Mitigating bias ensures fairness and trust in AI systems.",
                "action": "info",
            },
        ],
    },
    "Privacy and Security in AI": {
        "icon": "🔐",
        "description": "Understand why protecting personal data is crucial in AI systems.",
        "steps": [
            {
                "text": (
                    "**Why is privacy important?**\n\n"
                    "AI systems often handle personal data. If not protected, "
                    "this data can be misused or stolen.\n\n"
                    "**Example:** A chatbot storing private conversations without user consent."
                ),
                "action": "info",
            },
            {
                "text": "**Quiz:** Should AI systems collect only the data that is necessary?",
                "action": "quiz",
                "options": ["Yes", "No"],
                "correct": "Yes",
                "feedback_correct": "✅ Correct! Only necessary data should be collected to reduce privacy risks.",
                "feedback_incorrect": "❌ Incorrect. Minimizing data collection is a privacy best practice.",
            },
            {
                "text": "**Reflection:** Why do you think data privacy is especially important with AI systems?",
                "action": "reflect",
            },
            {
                "text": "💡 **Takeaway:** Privacy and security are vital for building trust in AI.",
                "action": "info",
            },
        ],
    },
    "Transparency and Explainability": {
        "icon": "🔍",
        "description": "Learn why AI decisions should be understandable to humans.",
        "steps": [
            {
                "text": (
                    "**Why does transparency matter?**\n\n"
                    "Users should know how AI makes decisions to build trust and accountability.\n\n"
                    "**Example:** A loan approval AI should explain why an application was rejected."
                ),
                "action": "info",
            },
            {
                "text": "**Quiz:** Should AI decisions always be understandable to humans?",
                "action": "quiz",
                "options": ["Yes", "No"],
                "correct": "Yes",
                "feedback_correct": "✅ Correct! Understandability is key for trust, accountability, and error detection.",
                "feedback_incorrect": "❌ Incorrect. AI decisions should be explainable for transparency.",
            },
            {
                "text": "💡 **Takeaway:** Transparency and explainability are crucial for responsible AI adoption.",
                "action": "info",
            },
        ],
    },
    "Accountability in AI": {
        "icon": "🎯",
        "description": "Understand human responsibility for AI outcomes.",
        "steps": [
            {
                "text": (
                    "**Why is accountability important?**\n\n"
                    "Humans, not machines, are responsible for the outcomes of AI decisions.\n\n"
                    "**Example:** A self-driving car accident must be investigated with human responsibility."
                ),
                "action": "info",
            },
            {
                "text": "**Quiz:** Should AI be allowed to operate without human oversight?",
                "action": "quiz",
                "options": ["Yes", "No"],
                "correct": "No",
                "feedback_correct": "✅ Correct! Human oversight is necessary for accountable and safe AI use.",
                "feedback_incorrect": "❌ Incorrect. Lack of human oversight increases risk and reduces accountability.",
            },
            {
                "text": "💡 **Takeaway:** Accountability ensures that AI serves and protects human interests.",
                "action": "info",
            },
        ],
    },
    "Misinformation and AI": {
        "icon": "📰",
        "description": "Learn about the risks of AI-generated misinformation.",
        "steps": [
            {
                "text": (
                    "**Why is misinformation a concern?**\n\n"
                    "AI can spread fake news or misleading content if not carefully managed.\n\n"
                    "**Example:** Deepfake videos used to manipulate public opinion."
                ),
                "action": "info",
            },
            {
                "text": "**Quiz:** Should we verify AI-generated content before sharing?",
                "action": "quiz",
                "options": ["Yes", "No"],
                "correct": "Yes",
                "feedback_correct": "✅ Correct! Verifying content is key to preventing misinformation.",
                "feedback_incorrect": "❌ Incorrect. Always verify before sharing to reduce risks.",
            },
            {
                "text": "💡 **Takeaway:** Vigilance against misinformation helps protect digital spaces and public trust.",
                "action": "info",
            },
        ],
    },
}
