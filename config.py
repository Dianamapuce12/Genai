def get_api_key():
  try:
    openai_api_key = st.secrets["openai_api_key"]
    
    # Validate the API key format
    if not openai_api_key.startswith("sk-"):
        st.error("Invalid OpenAI API key format. The key should start with 'sk-'")
        st.stop()
except KeyError:
    st.error("OpenAI API key not found in secrets. Please add 'openai_api_key' to your Streamlit secrets.")

def 
