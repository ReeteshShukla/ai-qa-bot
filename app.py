import os
import streamlit as st
from groq import Groq
from dotenv import load_dotenv

# Load API key

load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    st.error(" GROQ_API_KEY not found in .env file")
    st.stop()

client = Groq(api_key=GROQ_API_KEY)

st.set_page_config(page_title="AI Q&A Bot (Groq)", page_icon="⚡", layout="centered")

# Styling

st.markdown("""
    <style>
    body { background-color: #f5f7fa; }
    .stTextInput>div>div>input {
        background-color: #ffffff;
        border: 2px solid #4CAF50;
        border-radius: 8px;
        color: black;
    }
    .stTextInput>div>div>input::placeholder {
        color: #000000;
        opacity: 0.8;
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        border-radius: 8px;
        font-weight: bold;
    }
    .stButton>button:hover {
        background-color: #45a049;
        color: #fff;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1 style='color:#2c3e50;'>⚡ AI Q&A Bot (Groq)</h1>", unsafe_allow_html=True)
st.write("Ask me anything!")

with st.sidebar:
    st.markdown("<h3 style='color:#4CAF50;'>⚙️ Settings</h3>", unsafe_allow_html=True)
    model = st.selectbox("Model", options=[
        "llama-3.1-8b-instant",
        "llama3-8b-8192",
        "llama3-70b-8192",
        "gemma2-9b-it"
    ], index=0)
    temperature = st.slider("Temperature", 0.0, 1.0, 0.7)
    max_tokens = st.slider("Max tokens", 50, 500, 200)

if "history" not in st.session_state:
    st.session_state.history = []

def ask_groq(question: str) -> str:
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": question}],
            temperature=temperature,
            max_tokens=max_tokens,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        
        # If model not found, show friendly message

        if "model_not_found" in str(e).lower():
            return " That model isn’t available to your key. Try another model from the sidebar."
        return f" Error: {e}"

question = st.text_input(" Enter your question:")
if st.button("Ask"):
    if question.strip():
        with st.spinner(" Thinking..."):
            answer = ask_groq(question)
            st.session_state.history.insert(0, (question, answer))
    else:
        st.warning("Please type a question!")

if st.session_state.history:
    st.markdown("<hr>", unsafe_allow_html=True)
    st.subheader(" Conversation History")
    for q, a in st.session_state.history:
        st.markdown(f"**Q:** <span style='color:#2980b9;'>{q}</span>", unsafe_allow_html=True)
        st.markdown(f"**A:** <span style='color:#27ae60;'>{a}</span>", unsafe_allow_html=True)
        st.markdown("---")
