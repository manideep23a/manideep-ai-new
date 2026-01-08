import streamlit as st
from google import genai
import PyPDF2

# --- 1. SECURE KEY LOADING ---
# Try to get keys from Secrets first
KEY1 = st.secrets.get("KEY1")
KEY2 = st.secrets.get("KEY2")
KEY3 = st.secrets.get("KEY3")

# IF SECRETS STILL FAIL: Use this backup (Paste your main key here too)
BACKUP_KEY = "AIza..." # <--- PASTE YOUR ACTUAL KEY HERE AS A LAST RESORT

# Combine them into a list
all_keys = [KEY1, KEY2, KEY3, BACKUP_KEY]
valid_keys = [k for k in all_keys if k and k != "AIza..."]

# --- 2. DEBUG SIDEBAR ---
with st.sidebar:
    st.title("System Status")
    if not valid_keys:
        st.error("❌ NO KEYS FOUND ANYWHERE")
        st.stop()
    else:
        st.success(f"✅ {len(valid_keys)} Keys Active")
