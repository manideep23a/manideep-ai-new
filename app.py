import streamlit as st
from google import genai
import PyPDF2
import time

# --- 1. ROTATION ENGINE ---
def get_ai_response(full_context):
    all_keys = [st.secrets.get("KEY1"), st.secrets.get("KEY2"), st.secrets.get("KEY3")]
    valid_keys = [k for k in all_keys if k]
    for i, key in enumerate(valid_keys):
        try:
            client = genai.Client(api_key=key)
            response = client.models.generate_content(model="gemini-2.0-flash", contents=full_context)
            return response.text, i + 1
        except Exception as e:
            if "429" in str(e): continue
            else: return f"❌ Error: {e}", None
    return "🛑 Keys exhausted.", None

# --- 2. UI SETUP ---
st.set_page_config(page_title="Research AI", layout="wide")
st.title("Manideep's Research Assistant 🚀")

with st.sidebar:
    st.success(f"{len([k for k in [st.secrets.get('KEY1'), st.secrets.get('KEY2'), st.secrets.get('KEY3')] if k])} Keys Active")
    uploaded_file = st.file_uploader("Upload PDF", type="pdf")
    pdf_text = ""
    if uploaded_file:
        reader = PyPDF2.PdfReader(uploaded_file)
        for page in reader.pages[:50]:
            pdf_text += page.extract_text()
        st.success("✅ PDF Loaded")

# --- 3. CHAT ---
if "messages" not in st.session_state: st.session_state.messages = []
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]): st.markdown(msg["content"])

if prompt := st.chat_input("Ask about your PDF..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"): st.markdown(prompt)
    with st.chat_message("assistant"):
        context = f"PDF Context: {pdf_text}\n\nQuestion: {prompt}" if pdf_text else prompt
        answer, key_num = get_ai_response(context)
        st.markdown(answer)
        st.session_state.messages.append({"role": "assistant", "content": answer})
