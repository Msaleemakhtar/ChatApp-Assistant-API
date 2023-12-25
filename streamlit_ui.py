# streamlit_ui.py
import streamlit as st
import openai
from app import process_website_and_files, start_chat

# setup the streamlit page with icon
st.set_page_config(page_title="ChatGpt- Like Chat App", page_icon=":speech_baloon")

# Initialize the session state variables for file IDs and chat control
if "file_id_list" not in st.session_state:
    st.session_state.file_id_list = []

if "start_chat" not in st.session_state:
    st.session_state.start_chat = False 

if "thread_id" not in st.session_state:
    st.session_state.thread_id = None
# Sidebar and UI elements
st.sidebar.header("🌈Configuration Parameters 🌈")
api_key = st.sidebar.text_input("Enter your openai_key🔑", type="password")
if api_key:
    openai.api_key = api_key

# Additional feature for scraping and file uploading
st.sidebar.header("✨Exceptional Capabilities ✨")
website_url = st.sidebar.text_input("Enter website Url to convert into Pdf🌐", key="website_url")

# Button to scrap a website, convert into pdf, and upload to openai
if st.sidebar.button("Scrap and Upload 🔄"):
    process_website_and_files(website_url, None)  # Pass None as a placeholder for the file

# Sidebar options: Upload personnel files
uploaded_file = st.sidebar.file_uploader("Upload your personnel files for Embeddings📂", key="file_uploader")
if st.sidebar.button("Upload Files 🚀"):
    if uploaded_file:
        process_website_and_files(None, uploaded_file)  # Pass None as a placeholder for the website URL

# Display the file ids
if st.session_state.file_id_list:
    st.sidebar.write("Uploaded the files IDs")
    for file_id in st.session_state.file_id_list:
        st.sidebar.write(file_id)

# Enable the button to start the chat session
if st.sidebar.button("Start Chat💬"):
    start_chat()

# Main chat interface 
st.title("🤖penAI Assistant Chat App")
st.write("🌟 Welcome to the future of chat! 🚀 Immerse yourself in this vibrant chat experience powered by OpenAI's Assistant API and Knowledge retrieval. Let the magic of technology unfold in each response! ✨💬")

# Show chat interface when chat start in the sidebar has been clicked
if st.session_state.start_chat:
    # Rest of your chat interface code

    # Initialize the session state variable for user messages
    if "user_messages" not in st.session_state:
        st.session_state.user_messages = []

    # Take input from the user and add to user_messages
    user_input = st.text_input("Enter your message💬")
    if st.button("Send"):
        st.session_state.user_messages.append({"role": "user", "content": user_input})

    # Display user messages
    for message in st.session_state.user_messages:
        with st.expander(message["role"]):
            st.write(message["content"])

    # Rest of the chat interface code
    # ...
else:
    st.write("Please upload the file and click on 'Start Chat' to begin the conversation")
