import streamlit as st
import google.generativeai as genai
import PyPDF2
import time

# --- 1. THE ROTATION ENGINE ---
def get_ai_response(full_context):
    # This looks for KEY1, KEY2, and KEY3 in your secrets
    valid_keys = [st.secrets.get("KEY1"), st.secrets.get("KEY2"), st.secrets.get("KEY3")]
    # Remove any empty ones
    valid_keys = [k for k in valid_keys if k]

    for i, key in enumerate(valid_keys):
        try:
            genai.configure(api_key=key)
            model = genai.GenerativeModel("gemini-1.5-flash")
            response = model.generate_content(full_context)
            return response.text, i + 1  # Returns the answer and which key worked
        except Exception as e:
            if "429" in str(e):
                continue # Key is blocked for an hour, try the next one
            else:
                return f"❌ API Error: {e}", None
    return "🛑 ALL KEYS ARE CURRENTLY BLOCKED. Please wait 30-60 minutes.", None

# --- 2. PAGE SETUP ---
st.set_page_config(page_title="Manideep's Research AI", page_icon="🚀")
st.title("Manideep's Research Assistant 🚀")

# --- 3. SIDEBAR ---
with st.sidebar:
    st.header("Upload Document")
    uploaded_file = st.file_uploader("Choose a PDF", type="pdf")
    
    pdf_text = ""
    if uploaded_file:
        try:
            reader = PyPDF2.PdfReader(uploaded_file)
            for page in reader.pages[:50]: # Optimized for first 50 pages
                text = page.extract_text()
                if text:
                    pdf_text += text
            st.success(f"✅ Loaded {len(reader.pages)} pages!")
        except Exception as e:
            st.error(f"Error reading PDF: {e}")

# --- 4. CHAT INTERFACE ---
if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Ask about your document..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("🔄 AI is thinking (using key rotation)..."):
            context = f"Document Context:\n{pdf_text}\n\nQuestion: {prompt}" if pdf_text else prompt
            answer, key_num = get_ai_response(context)
            
            st.markdown(answer)
            if key_num:
                st.caption(f"Used Key #{key_num} to bypass limits")
            st.session_state.messages.append({"role": "assistant", "content": answer})
