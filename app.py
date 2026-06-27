import streamlit as st
from agent import build_agent

st.set_page_config(
    page_title="Healthcare AI Assistant",
    page_icon="🏥",
    layout="wide"
)

st.title("🏥 Healthcare AI Assistant")
st.markdown("### AI-powered Patient History, Appointment Booking & Disease Information")

@st.cache_resource
def load_agent():
    return build_agent()

agent = load_agent()

query = st.text_area(
    "Ask a healthcare question",
    placeholder="Example: Ask me something about a patient or a disease...",
)

if st.button("Submit"):
    if query.strip():
        with st.spinner("Thinking..."):
            try:
                result = agent.invoke({"input": query})
                st.success("Response")
                st.write(result["output"])
                except Exception as e:
                st.error(str(e))
