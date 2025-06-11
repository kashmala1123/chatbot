import google.generativeai as genai
import streamlit as st

# API Configuration
GOOGLE_API_KEY = "AIzaSyA263PFo-EEA9qs_-93Cy5v79nhVoUxQLc"
genai.configure(api_key=GOOGLE_API_KEY)

# Model Initialization
model = genai.GenerativeModel('gemini-1.5-flash')

# Function to get response from the model
def getResponseFromModel(user_input):
    if not isinstance(user_input, str) or not user_input.strip():
        raise ValueError("Prompt must be a non-empty string.")
    try:
        response = model.generate_content(user_input)
        return response.text
    except Exception as e:
        st.error("❌ Failed to get response from Gemini API.")
        st.error(f"Details: {e}")
        return "Sorry, something went wrong. Please try again later."

# Page config
st.set_page_config(page_title="AI Chat with Gemini", page_icon="🤖")
st.title("🤖 AI Chatbot")
st.subheader("Welcome, Kashmala")
st.write("This chatbot is powered by Gemini API")

# Sidebar: Select mode
interview_type = st.sidebar.radio("🧠 Choose Mode:", ["General Chat", "Coding Interview", "System Design"])

# Chat history
if "history" not in st.session_state:
    st.session_state["history"] = []

# Custom CSS for chat bubbles
st.markdown("""
    <style>
    .user-bubble, .bot-bubble {
        padding: 12px 16px;
        border-radius: 20px;
        margin-bottom: 10px;
        max-width: 80%;
        backdrop-filter: blur(12px);
        background: rgba(255, 255, 255, 0.1);
        border: 1px solid rgba(255, 255, 255, 0.3);
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
        font-family: 'Segoe UI', sans-serif;
    }
    .user-bubble {
        margin-left: 0;
        color: #000;
        background: rgba(220, 248, 198, 0.6);
    }
    .bot-bubble {
        margin-left: auto;
        color: #fff;
        background: rgba(59, 59, 59, 0.7);
    }
    </style>
""", unsafe_allow_html=True)

# Show buttons for mock questions
if interview_type == "Coding Interview":
    if st.button("🎯 Get a Coding Question"):
        question = getResponseFromModel("Give me a challenging coding interview question.")
        st.session_state["history"].append(("Give me a coding interview question", question))
        st.rerun()

if interview_type == "System Design":
    if st.button("🛠️ Get a System Design Prompt"):
        prompt = getResponseFromModel("Give me a realistic system design interview question.")
        st.session_state["history"].append(("Give me a system design interview question", prompt))
        st.rerun()

# Input form
with st.form(key="chat_form", clear_on_submit=True):
    user_input = st.text_area("Your Message / Answer", max_chars=3000, placeholder="Type your response here...", height=150)
    submit_button = st.form_submit_button("Send")

    if submit_button:
        if user_input.strip():
            if interview_type == "General Chat":
                response = getResponseFromModel(user_input)
            elif interview_type == "Coding Interview":
                prompt = f"You are a coding interviewer. Here's the candidate's answer:\n\n'{user_input}'\n\nPlease evaluate this and provide detailed feedback on correctness, time/space complexity, and improvement tips."
                response = getResponseFromModel(prompt)
            elif interview_type == "System Design":
                prompt = f"You are a system design interviewer. Here's the candidate's design idea:\n\n'{user_input}'\n\nEvaluate it and give detailed feedback including architecture, scalability, and trade-offs."
                response = getResponseFromModel(prompt)

            st.session_state["history"].append((user_input, response))
            st.rerun()
        else:
            st.warning("⚠️ Please enter a valid message.")

# Clear chat
if st.session_state["history"]:
    if st.button("🧹 Clear Chat"):
        st.session_state["history"] = []
        st.rerun()

# Display history
if st.session_state["history"]:
    for user_message, bot_response in st.session_state["history"]:
        st.markdown(f'<div class="user-bubble"><strong>You:</strong> {user_message}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="bot-bubble"><strong>Bot:</strong> {bot_response}</div>', unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
