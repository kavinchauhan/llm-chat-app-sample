import streamlit as st
import requests
import os

# 1. Page Configuration
st.set_page_config(page_title="OpenShift AI Chat", page_icon="🤖", layout="centered")
st.title("🤖 OpenShift AI Chat Assistant")

# 2. Fetch Configurations from OpenShift Environment Variables
# These fallback to defaults if not set by 'oc set env'
API_URL = os.getenv("LLM_API_URL", "https://openai.com")
API_KEY = os.getenv("LLM_API_KEY", "none")
MODEL_NAME = os.getenv("LLM_MODEL_NAME", "gpt-4o")

# 3. Initialize Chat Session State
if "messages" not in st.session_state:
    st.session_state.messages = []

# 4. Display Existing Chat History
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# 5. Capture and Process User Input
if prompt := st.chat_input("What is on your mind?"):
    # Append and display user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    # 6. Dynamically Build Request Headers
    headers = {
        "Content-Type": "application/json"
    }
    
    # Only append Authorization header if a valid key is provided
    if API_KEY and API_KEY.strip().lower() != "none":
        headers["Authorization"] = f"Bearer {API_KEY}"

    # 7. Construct OpenAI/vLLM Compatible JSON Payload
    payload = {
        "model": MODEL_NAME,
        "messages": st.session_state.messages
    }

    # 8. Send Request to the LLM Model Endpoint
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
            #    response = requests.post(API_URL, json=payload, headers=headers)
                response = requests.post(API_URL, json=payload, headers=headers, verify=False)
                
                # Check for standard HTTP errors (404, 500, etc.)
                response.raise_for_status()
                
                # Parse JSON response
                response_data = response.json()
                ai_response = response_data["choices"][0]["message"]["content"]
                
                # Render response and save to history
                st.write(ai_response)
                st.session_state.messages.append({"role": "assistant", "content": ai_response})
                
            except requests.exceptions.RequestException as req_err:
                st.error(f"Network error connecting to LLM: {req_err}")
            except KeyError:
                st.error("Received unexpected response format from the model server.")
                if 'response_data' in locals():
                    st.json(response_data) # Prints the raw structure to debug easily
            except Exception as e:
                st.error(f"An unexpected error occurred: {e}")
