import streamlit as st
import google.generativeai as genai
import itertools
import time

# ------------------ PAGE CONFIG ------------------
st.set_page_config(
    page_title="Manideep AI (Gemini)",
    layout="centered",
)

st.title("🤖 Manideep AI Assistant")
st.caption("Powered by Google Gemini • Safe Mode Enabled")

# ------------------ API KEY ROTATION ------------------
API_KEYS = [
    st.secrets.get("GEMINI_KEY_1"),
    st.secrets.get("GEMINI_KEY_2"),
    st.secrets.get("GEMINI_KEY_3"),
]

API_KEYS = [k for k in API_KEYS if k]

if not API_KEYS:
    st.error("❌ No Gemini API keys found in Streamlit secrets.")
    st.stop()

key_cycle = itertools.cycle(API_KEYS)

def get_model():
    genai.configure(api_key=next(key_cycle))
    return genai.GenerativeModel("gemini-1.5-flash")

# ------------------ RATE LIMIT PROTECTION ------------------
if "last_request_time" not in st.session_state:
    st.session_state.last_request_time = 0

COOLDOWN_SECONDS = 10

# ------------------ UI ------------------
prompt = st.text_area(
    "Enter your prompt",
    placeholder="Ask anything...",
    height=150
)

generate = st.button("🚀 Generate Response")

# ------------------ LOGIC ------------------
if generate:
    now = time.time()
    elapsed = now - st.session_state.last_request_time

    if elapsed < COOLDOWN_SECONDS:
        st.warning(f"⏳ Please wait {int(COOLDOWN_SECONDS - elapsed)} seconds.")
        st.stop()

    if not prompt.strip():
        st.warning("⚠️ Please enter a prompt.")
        st.stop()

    st.session_state.last_request_time = now

    try:
        with st.spinner("Thinking..."):
            model = get_model()
            response = model.generate_content(prompt)

        if response and hasattr(response, "text"):
            st.success("✅ Response generated")
            st.write(response.text)
        else:
            st.error("❌ Emp
