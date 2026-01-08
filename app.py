import streamlit as st

# --- DEBUGGING BLOCK ---
st.title("Debug Mode 🔍")
if not st.secrets:
    st.error("The entire Secrets box is EMPTY. Please go to Settings > Secrets and paste your keys.")
    st.stop()

found_keys = list(st.secrets.keys())
st.write(f"I found these names in your Secrets: {found_keys}")

if "KEY1" not in st.secrets:
    st.warning("I found secrets, but none of them are named 'KEY1'. Check your spelling!")
    st.stop()
else:
    st.success("KEY1 found! Proceeding to the app...")
# --- END DEBUGGING ---
