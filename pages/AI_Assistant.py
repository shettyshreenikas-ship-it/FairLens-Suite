import streamlit as st
from gtts import gTTS
import os

# 1. Page Config
st.set_page_config(page_title="FairHire AI Assistant", page_icon="🤖", layout="centered")

# 2. Custom Styling to match your Dark/Gold Theme
st.markdown("""
<style>
    html, body, [data-testid="stAppViewContainer"] { background: #0d0d0d; color: #e2e0d8; }
    .stChatMessage { background: rgba(255,255,255,0.05); border-radius: 10px; margin-bottom: 10px; }
    .stButton > button { 
        background: transparent !important; 
        border: 1px solid #c9a84c !important; 
        color: #c9a84c !important; 
        border-radius: 20px !important;
    }
</style>
""", unsafe_allow_html=True)

st.title("🤖 FairHire Voice Assistant")
st.markdown("---")

# 3. Chat History Setup
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 4. Chat Input & Logic
if prompt := st.chat_input("Ask about AI Bias or Compliance..."):
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate Assistant Response
    with st.chat_message("assistant"):
        # The "Brain": Responding based on keywords
        p_low = prompt.lower()
        if "hiring" in p_low or "job" in p_low:
            response = "Our module checks for gendered language and age bias in resumes to ensure ATS compliance."
        elif "loan" in p_low or "bank" in p_low:
            response = "We analyze ZIP code patterns to detect 'redlining' bias in automated loan approvals."
        elif "legal" in p_low or "act" in p_low:
            response = "FairHire maps your data against the EU AI Act to ensure your company avoids massive legal fines."
        else:
            response = "I am your FairHire Assistant. I help detect hidden bias in hiring, lending, and insurance algorithms."

        st.markdown(response)

        # 5. INTEGRATED VOICE FEATURE
        # This part generates the audio for the SPECIFIC response
        try:
            tts = gTTS(text=response, lang='en', tld='co.in')
            tts.save("ai_response.mp3")
            st.audio("ai_response.mp3")
        except Exception as e:
            st.error("Audio engine busy. Please try again.")

    # Save to history
    st.session_state.messages.append({"role": "assistant", "content": response})

# Sidebar Back Button
if st.sidebar.button("⬅ Back to Dashboard"):
    st.switch_page("app.py")