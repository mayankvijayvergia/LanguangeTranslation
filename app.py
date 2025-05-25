import streamlit as st
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set page config
st.set_page_config(
    page_title="AI Language Translator 🌍",
    page_icon="🌐",
    layout="centered"
)

# Load Groq API Key
groq_api_key = os.getenv("GROQ_API_KEY")
if not groq_api_key:
    st.error("GROQ_API_KEY not found. Please set it in Streamlit secrets.")
    st.stop()

# Initialize LLM
model = ChatGroq(model="Gemma2-9b-It", groq_api_key=groq_api_key)

# Define prompt template
generic_template = "Translate the following into {language}:"
prompt = ChatPromptTemplate.from_messages([
    ("system", generic_template),
    ("user", "{text}")
])

# Output parser and chain
parser = StrOutputParser()
chain = prompt | model | parser

# --- UI ---
st.title("🌐 AI Language Translator")
st.caption("Built with Groq + LangChain + Streamlit")

# Styling divider
st.markdown("---")

# Translation form
with st.form("translation_form"):
    st.subheader("📥 Enter Text to Translate")
    text = st.text_area("Your text in English", height=150)
    language = st.selectbox("Select target language", ["French", "Spanish", "German", "Hindi", "Arabic"])
    submitted = st.form_submit_button("🔄 Translate")

    if submitted:
        if not text.strip():
            st.warning("⚠️ Please enter some text to translate.")
        else:
            with st.spinner("Translating using Groq..."):
                output = chain.invoke({"language": language, "text": text})

            # Display result in two columns
            st.markdown("### 📄 Translation Result")
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("**Original Text**")
                st.write(text)
            with col2:
                st.markdown(f"**Translated to {language}**")
                st.success(output)

# Footer
st.markdown("---")
st.markdown("🚀 Built by 🔗[Mayank Vijay](https://www.linkedin.com/in/mayank-vijay/)")
