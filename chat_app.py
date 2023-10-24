import openai
import streamlit as st
import requests
import json


if "messages" not in st.session_state:
    st.session_state.messages = []
st.set_page_config(layout="wide", page_title="chat", page_icon=":computer:")
st.title("ChatGPT-like clone")
#st.markdown(f"**Upload a PDF file and chat with our assistant to inquire about the contents!**")
# Sidebar content
st.sidebar.subheader("About the app")
st.sidebar.info("This app uses OpenAI or HuggingFace.")
st.sidebar.write("\n\n")
option = st.sidebar.selectbox(
    'What model do you like to use?',
    ('OpenAI', 'HuggingFace'))
st.session_state["model_1"] = option
API_KEY = st.sidebar.text_input("Enter your HuggingFace API key",  type="password")
st.sidebar.markdown("**Get a free API key from HuggingFace:**")
# HuggingFace API KEY input
st.sidebar.markdown("* Create a [access token from huggingface](https://huggingface.co/join) or a  [payed OpenAi key](https://platform.openai.com/login?launch) ")
# st.sidebar.markdown("* Go to **Settings** and then **Access Tokens**")
# st.sidebar.markdown("* Create a new Token (select 'read' role)")
st.sidebar.markdown("* Paste your API key in the text box")
def query(payload):
    data = json.dumps(payload)
    response = requests.request("POST", API_URL, headers=headers, data=data)
    print(response.json())
    return json.loads(response.content.decode("utf-8"))
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
    if st.session_state["model_1"]== "OpenAI":
        openai.api_key = API_KEY
        if "openai_model" not in st.session_state:
            st.session_state["openai_model"] = "gpt-3.5-turbo"
        responses = openai.ChatCompletion.create( model=st.session_state["openai_model"],
                                                     messages=[{"role": m["role"], "content": m["content"]}for m in st.session_state.messages],
                                                     stream=True,)
        for response in responses:
            full_response += response.choices[0].delta.get("content", "")
            message_placeholder.markdown(full_response + " ")
        message_placeholder.markdown(full_response)
        st.session_state.messages.append({"role": "assistant", "content": full_response})
    if st.session_state["model_1"]== "HuggingFace":
        #API_URL = "https://api-inference.huggingface.co/models/HuggingFaceH4/zephyr-7b-alpha"
        API_URL = "https://api-inference.huggingface.co/models/microsoft/DialoGPT-large"
        headers = {"Authorization": f"Bearer {API_KEY}"}
        full_response = ""
        user_input = []
        assist_input = []
        for m in st.session_state.messages:
            content = m["content"]
            if m["role"]== "user" and not content == prompt  :
                user_input.append(content)
            elif m["role"]== "assistant":
                assist_input.append(content)
        data = query({"inputs": {
                         "past_user_inputs": user_input,
                         "generated_responses": assist_input,
                         "text": prompt,},})
        #data.pop("warnings")
        #message = {"inputs":[{"role": m["role"], "content": m["content"]}for m in st.session_state.messages]}
        #print(message)
        #data = query(message)        
        #print(data)
        full_response = data["generated_text"]
        message_placeholder.markdown(full_response + " ")
        #for response in responses:
        #    full_response += response.choices[0].delta.get("content", "")
        #    message_placeholder.markdown(full_response + " ")
        #message_placeholder.markdown(full_response)
        st.session_state.messages.append({"role": "assistant", "content": full_response})
