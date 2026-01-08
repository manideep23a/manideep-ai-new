import streamlit as st
from google import genai
import PyPDF2

# --- 1. CONFIGURATION ---
try:
    API_KEY = st.secrets["GOOGLE_API_KEY"]
except:
    st.error("⚠️ API Key missing in Secrets!")
    st.stop()

# Initialize the new 2026 Client
client = genai.Client(api_key=API_KEY)

# --- 2. PAGE SETUP ---
st.set_page_config(page_title="My Research AI", page_icon="📚")
st.title("Manideep's Research Assistant 🚀")

# --- 3. SIDEBAR & UPLOAD ---
with st.sidebar:
    st.header("Upload Document")
    uploaded_file = st.file_uploader("Choose a PDF", type="pdf")
    pdf_text = ""
    if uploaded_file:
        try:
            reader = PyPDF2.PdfReader(uploaded_file)
            for page in reader.pages:
                text = page.extract_text()
                if text:
                    pdf_text += text
            st.success(f"✅ Loaded {len(reader.pages)} pages!")
        except Exception as e:
            st.error(f"Error reading PDF: {e}")

# --- 4. CHAT LOGIC ---
if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Ask about your PDF..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        message_placeholder.markdown("Thinking...")
        
        # Combine PDF text and user question
        full_message = f"Document Content:\n{pdf_text}\n\nQuestion: {prompt}" if pdf_text else prompt
        
        try:
            # Using the experimental 2.0 flash name which is often more stable for API calls
            response = client.models.generate_content(
                model="gemini-1.5-flash", 
                contents=full_message
            )
            message_placeholder.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            message_placeholder.error(f"⚠️ API Error: {e}")

