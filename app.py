import streamlit as st
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv

# Load .env variables
load_dotenv()

# Groq API Key
groq_api_key = os.getenv("GROQ_API_KEY")


# Initialize model
model = ChatGroq(model="Gemma2-9b-It", groq_api_key=groq_api_key)

# Prompt Template
generic_template = "Translate the following into {language}:"
prompt = ChatPromptTemplate.from_messages([
    ("system", generic_template),
    ("user", "{text}")
])

# Output parser
parser = StrOutputParser()

# Final chain
chain = prompt | model | parser

# --- Streamlit UI ---
st.title("🌍 Language Translator with Groq + LangChain")

text = st.text_area("Enter text to translate:")
language = st.selectbox("Translate to:", ["French", "Spanish", "German", "Hindi", "Arabic"])

if st.button("Translate"):
    if text.strip() == "":
        st.warning("Please enter some text.")
    else:
        with st.spinner("Translating..."):
            output = chain.invoke({"language": language, "text": text})
            st.success("Translation complete:")
            st.write(output)