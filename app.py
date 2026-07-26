import streamlit as st
import requests
import os

st.title("🤖 OpenShift AI Chat Assistant")

# Pull variables from OpenShift environment fields
API_URL = os.getenv("LLM_API_URL", "https://redhataimeta-llama-31-8b-instr-kvn-ai.apps.openshift-ai.aws.kavinchauhan.in")
#API_KEY = os.getenv("LLM_API_KEY", "YOUR_DEFAULT_KEY")
MODEL_NAME = os.getenv("LLM_MODEL_NAME", "redhataimeta-llama-31-8b-instr")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

if prompt := st.chat_input("What is on your mind?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)
 #   headers = {"Content-Type": "application/json", "Authorization": f"Bearer {API_KEY}"}
    headers = {"Content-Type": "application/json"}
    payload = {"model": MODEL_NAME, "messages": st.session_state.messages}

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                response = requests.post(API_URL, json=payload, headers=headers)
                ai_response = response.json()["choices"]["message"]["content"]
                st.write(ai_response)
                st.session_state.messages.append({"role": "assistant", "content": ai_response})
            except Exception as e:
                st.error(f"Error connecting to LLM: {e}")
