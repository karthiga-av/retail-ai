import streamlit as st
import requests
import uuid

st.set_page_config(page_title="AI Financial Advisor", layout="wide")

st.title("💰 AI Financial Advisor")

# 🧠 Initialize sessions
if "sessions" not in st.session_state:
    st.session_state.sessions = {}

if "current_session" not in st.session_state:
    session_id = str(uuid.uuid4())
    st.session_state.current_session = session_id
    st.session_state.sessions[session_id] = []

# 🔹 Sidebar
st.sidebar.title("💬 Chats")

# New Chat button
if st.sidebar.button("➕ New Chat"):
    session_id = str(uuid.uuid4())
    st.session_state.current_session = session_id
    st.session_state.sessions[session_id] = []

# List chat history
for session_id in st.session_state.sessions:
    if st.sidebar.button(f"Chat {list(st.session_state.sessions).index(session_id)+1}", key=session_id):
        st.session_state.current_session = session_id

# Current messages
messages = st.session_state.sessions[st.session_state.current_session]

# 📤 Upload file
uploaded_file = st.file_uploader("Upload PDF/TXT")

if uploaded_file:
    files = {"file": (uploaded_file.name, uploaded_file.getvalue())}
    requests.post("http://localhost:8000/api/v1/upload", files=files)
    st.success("File uploaded successfully!")

# 💬 Display chat
for msg in messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# 🧾 Input
if prompt := st.chat_input("Ask your question"):

    # Save user message
    messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    # API call
    response = requests.post(
        "http://localhost:8000/api/v1/query",
        json={"query": prompt}
    )

    answer = response.json()["response"]

    # Save assistant response
    messages.append({"role": "assistant", "content": answer})

    with st.chat_message("assistant"):
        st.markdown(answer)