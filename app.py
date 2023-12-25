
import time
import pdfkit
import requests
from bs4 import BeautifulSoup
import openai
from openai.types.beta import Assistant
import streamlit as st

# Initialize the client to set the API key from the user in the sidebar within the app
client = openai

# Initialize the Assistant
assistant: Assistant = client.beta.assistants.create(
    name="Assistant",
    instructions="Utilize your knowledge base and the uploaded file to provide optimal responses to user queries as a knowledgeable AI assistant.",
    model="gpt-3.5-turbo-1106",
    tools=[{"type": "retrieval"}],
)

# Define the function for scraping, converting text to pdf, uploading pdf
def scrape_website(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    return soup.get_text()

def text_to_pdf(text, filename):
    path_wkhtmltopdf = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'
    config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)
    pdfkit.from_string(text, filename, configuration=config)
    return filename

def upload_to_openai(filepath):
    with open(filepath, "rb") as file:
        response = client.files.create(file=file.read(), purpose="assistants")
    return response.id

# Process message with citations
def process_message_citations(message):
    # Extract the message content
    message_content = message.content[0].text
    annotations = message_content.annotations
    citations = []

    # Iterate over the annotations and add footnotes
    for index, annotation in enumerate(annotations):
        # Replace the text with a footnote
        message_content.value = message_content.value.replace(annotation.text, f' [{index}]')

        # Gather citations based on annotation attributes
        if (file_citation := getattr(annotation, 'file_citation', None)):
            cited_file = client.files.retrieve(file_citation.file_id)
            citations.append(f'[{index}] {file_citation.quote} from {cited_file.filename}')
        elif (file_path := getattr(annotation, 'file_path', None)):
            cited_file = client.files.retrieve(file_path.file_id)
            citations.append(f'[{index}] Click [here](sandbox:/files/{cited_file.id}) to download {cited_file.filename}')

    # Add footnotes to the end of the message before displaying to the user
    full_response = message_content.value + '\n\n' + '\n'.join(citations)
    return full_response

# Main functions for processing website and files, starting chat, etc.
def process_website_and_files(website_url, uploaded_file):
    # Call the relevant functions from your backend
    scraped_text = scrape_website(website_url)
    pdf_path = text_to_pdf(scraped_text, "scraped_content.pdf")
    file_id = upload_to_openai(pdf_path)
    st.session_state.file_id_list.append(file_id)

def start_chat():
    # Call the relevant functions from your backend
    if st.session_state.file_id_list:
        st.session_state.start_chat = True
        # Create a thread and store its id in the session state
        thread = client.beta.threads.create()
        st.session_state.thread_id = thread.id
        st.sidebar.write("Thread ID:", thread.id)
    else:
        st.sidebar.warning("Enter at least one file to start the chat❗")

    # Rest of your chat functionality, including message handling and interaction with OpenAI API
    # ...
