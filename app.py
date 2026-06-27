import streamlit as st

st.title("🧪 Minimal Test App")
st.write("Checking if Streamlit can read the OpenAI API Key...")

# Attempt to read the secret safely
try:
    api_key = st.secrets["OPENAI_API_KEY"]
    # We will only print the first 10 characters to keep it secure!
    masked_key = f"{api_key[:10]}..." 
    st.success(f"✅ Key found successfully! It starts with: {masked_key}")
except KeyError:
    st.error("🛑 Key NOT found. Streamlit Secrets is empty or misnamed.")
except Exception as e:
    st.error(f"🛑 Unexpected error: {e}")
