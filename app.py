import streamlit as st
import google.generativeai as genai
import PyPDF2

# --- CONFIGURATION ---
try:
    API_KEY = st.secrets["GOOGLE_API_KEY"]
except:
    st.error("⚠️ API Key missing in Secrets!")
    st.stop()

genai.configure(api_key=API_KEY)

# --- SETUP MODEL ---
model_name = "gemini-1.5-flash" 
try:
    model = genai.GenerativeModel(model_name)
except Exception as e:
    st.error(f"❌ Connection Error: {e}")

# --- PAGE SETUP ---
st.set_page_config(page_title="My Research AI", page_icon="📚")
st.title("Manideep's Research Assistant 🚀")

# --- UPLOAD ---
with st.sidebar:
    st.header("Upload Document")
    uploaded_file = st.file_uploader("Choose a PDF", type="pdf")

    pdf_text = ""
    if uploaded_file is not None:
        try:
            reader = PyPDF2.PdfReader(uploaded_file)
            for page in reader.pages:
                pdf_text += page.extract_text()
            st.success(f"✅ Loaded {len(reader.pages)} pages!")
        except Exception as e:
            st.error(f"Error reading PDF: {e}")

# --- CHAT ---
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ask about your PDF..."):
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    full_prompt = prompt
    if pdf_text:
        full_prompt = f"Here is the document context: {pdf_text}\n\nUser Question: {prompt}"

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        message_placeholder.markdown("Thinking...")
        try:
            response = model.generate_content(full_prompt)
            message_placeholder.markdown(response.text)
            st.session_state.messages.append({"role": "model", "content": response.text})
        except Exception as e:

            message_placeholder.error(f"⚠️ Error: {e}")
