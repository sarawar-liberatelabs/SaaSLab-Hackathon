import streamlit as st
import requests

API_URL = "http://localhost:8000"

def send_message(message):
    url = f"{API_URL}/chat/chat"
    data = {"message": message}
    try:
        response = requests.post(url, json=data)
        if response.status_code == 200:
            return response.json()["response"], None
        else:
            return None, response.json().get("detail", "Failed to send message.")
    except Exception as e:
        return None, str(e)

def fetch_chat_history():
    url = f"{API_URL}/chat/chat/history"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.json().get("chat_history", []), None
        else:
            return [], response.json().get("detail", "Failed to fetch history.")
    except Exception as e:
        return [], str(e)

def show_chat():
    st.title("AI Chatbot")
    chat_history, error = fetch_chat_history()
    if error:
        st.error(error)
    else:
        for entry in chat_history:
            st.markdown(f"**You:** {entry['message']}")
            if entry['message_type'] == 'HumanMessage':
                continue
            st.markdown(f"**AI:** {entry['message']}")
    st.markdown("---")
    message = st.text_input("Your message:")
    if st.button("Send") and message:
        response, error = send_message(message)
        if response:
            st.success("AI: " + response)
            st.experimental_rerun()
        else:
            st.error(error)

def main():
    show_chat()

if __name__ == "__main__":
    main()
