import streamlit as st
import requests
import json

# Page config
st.set_page_config(page_title="SaaSLab", layout="centered")
st.title("💬 SaaSLab")

# Initialize session state
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'show_chat' not in st.session_state:
    st.session_state.show_chat = False
if 'history_loaded' not in st.session_state:
    st.session_state.history_loaded = False

# Sidebar: toggle chat interface
with st.sidebar:
    st.header("Controls")
    if st.button("Acquisition Strategy Agent"):
        st.session_state.show_chat = True

# Show chat only when activated
if st.session_state.show_chat:
    # Load previous chat history once
    if not st.session_state.history_loaded:
        try:
            url = 'http://127.0.0.1:8000/chat/chat/history'
            payload = {'thread_id': 0, 'skip': 0, 'limit': 10}
            headers = {'accept': 'application/json', 'Content-Type': 'application/json'}
            resp = requests.get(url, headers=headers, json=payload, timeout=15)
            resp.raise_for_status()
            data = resp.json().get('chat_history', [])
            for entry in data:
                role = 'user' if entry.get('message_type') == 'HumanMessage' else 'assistant'
                st.session_state.chat_history.append({'role': role, 'content': entry.get('message')})
        except Exception as e:
            st.session_state.chat_history.append({'role': 'assistant', 'content': f"❌ Failed to load history: {e}"})
        finally:
            st.session_state.history_loaded = True

    # Display conversation history
    for msg in st.session_state.chat_history:
        st.chat_message(msg['role']).write(msg['content'])

    # User input
    user_message = st.chat_input("Type a message...")
    if user_message:
        # Record user message
        st.session_state.chat_history.append({'role': 'user', 'content': user_message})

        # Send user message to Acquisition API
        post_url = 'http://127.0.0.1:8000/Acquisition'
        payload = {'thread_id': '0', 'message': user_message}
        headers = {'accept': 'application/json', 'Content-Type': 'application/json'}
        try:
            resp = requests.post(post_url, headers=headers, json=payload, timeout=15)
            status = resp.status_code
            try:
                resp_data = resp.json()
            except ValueError:
                resp_data = {'response_text': resp.text}
            formatted = json.dumps(resp_data, indent=2)
            reply = f"**Status:** {status}\n```json\n{formatted}\n```"
        except Exception as e:
            reply = f"❌ Request failed: {e}"  

        # Record assistant reply
        st.session_state.chat_history.append({'role': 'assistant', 'content': reply})
