import streamlit as st  # Must be line 1
from google import genai
import PyPDF2
import time

# --- 1. CONFIGURATION & KEY ROTATION ---
def get_ai_response(full_context):
    # This matches the names you saved in your Streamlit Secrets
    all_keys = [st.secrets.get("KEY1"), st.secrets.get("KEY2"), st.secrets.get("KEY3")]
    # This ignores any keys that are empty
    valid_keys = [k for k in all_keys if k]

    for i, key in enumerate(valid_keys):
        try:
            # Using the new 2026 'google-genai' library
            client = genai.Client(api_key=key)
            response = client.models.generate_content(
                model="gemini-2.0-flash", # Most stable for 2026
                contents=full_context
            )
            return response.text, i + 1
        except Exception as e:
            if "429" in str(e):
                continue # Key is blocked/exhausted, try the next one
            else:
                return f"❌ API Error: {e}", None
    return "🛑 All 3 keys are currently exhausted. Please wait 1 hour.", None

# --- 2. PAGE SETUP ---
st.set_page_config(page_title="Manideep's Research AI", layout="wide")

# --- 3. SIDEBAR ---
with st.sidebar:
    st.header("📊 System Status")
    all_keys = [st.secrets.get("KEY1"), st.secrets.get("KEY2"), st.secrets.get("KEY3")]
    active_count = len([k for k in all_keys if k])
    st.success(f"{active_count} Keys Active")
    
    st.markdown("---")
    st.header("📂 Upload Document")
    uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")
    
    pdf_text = ""
    if uploaded_file:
        try:
            reader = PyPDF2.PdfReader(uploaded_file)
            # We take the first 50 pages to prevent the AI from getting confused
            for page in reader.pages[:50]:
                text = page.extract_text()
                if text:
                    pdf_text += text
            st.success(f"✅ {len(reader.pages)} Pages Loaded!")
        except Exception as e:
            st.error(f"Could not read PDF: {e}")

# --- 4. MAIN INTERFACE ---
st.title("Manideep's Research Assistant 🚀")

# Ensure the screen is never blank
if not uploaded_file:
    st.info("👋 Welcome! Please upload a PDF in the sidebar to start chatting.")
else:
    st.write("### Document Insight Mode")
    st.caption("The AI is now reading your uploaded file.")

# --- 5. CHAT LOGIC ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Chat input at the bottom
if prompt := st.chat_input("What would you like to know?"):
    # Add user message to history
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Get AI response
    with st.chat_message("assistant"):
        with st.spinner("🔄 AI is analyzing..."):
            # Prepare context
            full_prompt = f"Context from PDF:\n{pdf_text}\n\nUser Question: {prompt}" if pdf_text else prompt
            
            # Use rotation engine to get answer
            answer, key_index = get_ai_response(full_prompt)
            
            st.markdown(answer)
            if key_index:
                st.caption(f"Protected by Key Rotation (Used Key #{key_index})")
            
            # Save assistant response
            st.session_state.messages.append({"role": "assistant", "content": answer})
