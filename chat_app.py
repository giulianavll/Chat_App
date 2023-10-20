import openai
import streamlit as st
import requests


st.set_page_config(layout="wide", page_title="chat", page_icon=":computer:")
st.title("ChatGPT-like clone")
st.markdown(f"**Upload a PDF file and chat with our assistant to inquire about the contents!**")

# Sidebar content
st.sidebar.subheader("About the app")
st.sidebar.info("This app uses OpenAI or HuggingFace.")
st.sidebar.write("\n\n")
option = st.sidebar.selectbox(
    'What model do you like to use?',
    ('GPT', 'Hugging face'))
API_KEY = st.sidebar.text_input("Enter your HuggingFace API key",  type="password")
st.sidebar.markdown("**Get a free API key from HuggingFace:**")
# HuggingFace API KEY input
st.sidebar.markdown("* Create a [free account](https://huggingface.co/join) or [login](https://huggingface.co/login)")
# st.sidebar.markdown("* Go to **Settings** and then **Access Tokens**")
# st.sidebar.markdown("* Create a new Token (select 'read' role)")
st.sidebar.markdown("* Paste your API key in the text box")
st.sidebar.divider()
st.sidebar.write("Please ensure that your file has .pdf extension.")
if "messages" not in st.session_state:
    st.session_state.messages = []

if option== "OpenAI":
    openai.api_key = st.secrets["OPENAI_API_KEY"]
    if "openai_model" not in st.session_state:
        st.session_state["openai_model"] = "gpt-3.5-turbo"
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    if prompt := st.chat_input("What is up?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""
            responses = openai.ChatCompletion.create( model=st.session_state["openai_model"],
                                                     messages=[{"role": m["role"], "content": m["content"]}for m in st.session_state.messages],
                                                     stream=True,)
            for response in responses:
                full_response += response.choices[0].delta.get("content", "")
                message_placeholder.markdown(full_response + " ")
            message_placeholder.markdown(full_response)
        st.session_state.messages.append({"role": "assistant", "content": full_response})
def query(payload):
	response = requests.post(API_URL, headers=headers, json=payload)
	return response.json()
if option== "HuggingFace":
    API_URL =  "https://api-inference.huggingface.co/models/google/vit-base-patch16-224"
    headers = {"Authorization": f"Bearer {API_KEY}"}
    API_URL = "https://api-inference.huggingface.co/models/HuggingFaceH4/zephyr-7b-alpha"
    headers = {"Authorization": "Bearer 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"}


    
    output = query({
    	"inputs": "Can you please let us know more details about your ",
    })



