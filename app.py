from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate
import streamlit as st
import os
from dotenv import load_dotenv

load_dotenv()


groq_api_api = os.getenv('GROQ_API_KEY')


llm = ChatGroq(model_name="llama-3.1-8b-instant",groq_api_key=groq_api_api)

prompt_template = """
You are an AI Code Reviewer. Review the following {language} code

{code}

Provide:

1. Readability feedback
2. Bug or error detection
3. Performance improvements
4. Security concerns
5. Best practice suggestions

"""

prompt = PromptTemplate(
    input_variables=['code', 'language'],
    template=prompt_template
)


st.set_page_config(page_title="AI Code Review",layout="wide")
st.title("🤖 Intelligent Code Reviewer with LLMs (LangChain + Groq API)")



input_option =st.radio("How would you like to provide code?",("paste code", "upload file"))


user_code = ""

if input_option == "paste code":
    user_code = st.text_area("Paste your code here")
elif input_option == "upload file":
    file_loader = st.file_uploader("Upload your file", type=["py","js","sql"])
    if file_loader is not None:
        user_code = file_loader.read().decode('utf-8')
        

language = st.selectbox("Select Programming language", options=["Python","Java","SQL"])


if st.button("Review Code") and user_code.strip():
    
    formatted_prompt = prompt.format(code=user_code,language=language)
    
    response = llm.invoke(formatted_prompt)
    
    st.subheader("📝 AI Code Review Result")
    st.text_area("Review Output",value=response.content,height=700)
    
else:
    st.write("Please provide some code to review")
    
    