
# Imported necessary libraries
import time
import pdfkit
import requests
from bs4 import BeautifulSoup
import openai
from openai.types.beta import Assistant
import streamlit as st



# Initilaized the client to set the api key from user in sidebar within the app
client = openai


# Initialize the Assistant
assistant: Assistant = client.beta.assistants.create(
  name = "Assistant",
  instructions="Utilize your knowledge base and the uploaded file to provide optimal responses to user queries as a knowledgeable AI assistant.",
  model="gpt-3.5-turbo-1106",
  tools=[{"type": "retrieval"}],
)

# Initialize the session state variables for file IDs and chat control
if "file_id_list" not in st.session_state:
    st.session_state.file_id_list = []

if "start_chat" not in st.session_state:
    st.session_state.start_chat = False 

if "thread_id" not in st.session_state:
    st.session_state.thread_id = None


# setup the streamlit page with icon
st.set_page_config(page_title="ChatGpt- Like Chat App", 
                   page_icon=":speech_baloon",
                   )




# Define the function for scaping , converting text to pdf, uploading pdf
# Scrap text from website url
def scrape_website(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    return soup.get_text()

# Convert text content to pdf
def text_to_pdf(text, filename):
    path_wkhtmltopdf =r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'
    config = pdfkit.configuration(wkhtmltopdf = path_wkhtmltopdf)
    pdfkit.from_string(text, filename,configuration=config)
    return filename
  

# Upload and read the file to openai:- 
def upload_to_openai(filepath):
    with open(filepath, "rb") as file:
        response = client.files.create(file=file.read(), purpose="assistants")
    return response.id

# Create a sidebar for api configuration:-
st.sidebar.header("🌈Configuration Parameters 🌈")
api_key = st.sidebar.text_input("Enter your openai_key🔑", type="password")
if api_key:
    openai.api_key = api_key


# Additional feature for scraping and file uploading:-
st.sidebar.header("✨Exceptional Capabilities ✨")
website_url = st.sidebar.text_input("Enter website Url to convert into Pdf🌐", key="website_url")

# Button to scrap a website , convert into pdf and upload to openai:-
if st.sidebar.button("Scrap and Upload 🔄"):
    scraped_text = scrape_website(website_url)
    pdf_path  = text_to_pdf(scraped_text, "scraped_content.pdf")
    file_id = upload_to_openai(pdf_path)
    st.session_state.file_id_list.append(file_id)


# Sidebar options : Upload personnel files :-
    
uploaded_file = st.sidebar.file_uploader("Upload your personnel files for Embeddings📂", key="file_uploader")

if st.sidebar.button("Upload Files 🚀"):
    if uploaded_file:
        # locally file will be saved 
        with open(f"{uploaded_file.name}", "wb") as f:
            f.write(uploaded_file.getbuffer())
        # file uploaded to openai for embeddings
        upload_file_id = upload_to_openai(f"{uploaded_file.name}")
        st.session_state.file_id_list.append(upload_file_id)

# Display the file ids
if st.session_state.file_id_list:
    st.sidebar.write("Uploaded the files IDs")
    for file_id in st.session_state.file_id_list:
        st.sidebar.write(file_id)
        assistant_file = client.beta.assistants.files.create(
            assistant_id=assistant.id,
            file_id=file_id
        )

# Enable the button to start the chat session

if st.sidebar.button("Start Chat💬"):
    # check if the file ids are there
    if st.session_state.file_id_list:
        st.session_state.start_chat = True
        #Create a thread and store and store its id in session state
        thread = client.beta.threads.create()
        st.session_state.thread_id = thread.id
        st.sidebar.write("thread id ;", thread.id)

    else:
        st.sidebar.warning("Enter atleast one file to start the chat❗")


# process message  with citations
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
            citations.append(f'[{index}] Click <here> to download {cited_file.filename}')
            # Note: File download functionality not implemented above for brevity

    # Add footnotes to the end of the message before displaying to user
    full_response = message_content.value + '\n\n' + '\n'.join(citations)
    return full_response


# Main chat interface 
st.title("🤖penAI Assistant Chat App")
st.write("🌟 Welcome to the future of chat! 🚀 Immerse yourself in this vibrant chat experience powered by OpenAI's Assistant API and Knowledge retrieval. Let the magic of technology unfold in each response! ✨💬")

# show chat interface when chat start in sidebar has been clicked

if st.session_state.start_chat:
    # Initialize the model if not already in the session state
    if "openai_model" not in st.session_state:
        st.session_state.openai_model = "gpt-3.5-turbo-1106"
    # Initialize the message list if not already in the session state
    if "messages" not in st.session_state:
        st.session_state.messages = []
    # Display existaing messages in chat
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Take input from user to start the chat
    if prompt := st.chat_input("Enter your prompt💬"):
        # add the user prompt to sesssion state
        st.session_state.messages.append({"role":"user", "content":prompt})
        #display the user messages
        with st.chat_message("user"):
            st.markdown(prompt)

        # add users message to existing thread
        client.beta.threads.messages.create(
            thread_id=st.session_state.thread_id,
            role="user",
            content= prompt
        )

        # Initialize the run
        run = client.beta.threads.runs.create(
            assistant_id = assistant.id,
            thread_id= st.session_state.thread_id,
            instructions="Please answer the queries using the knowledge provided in the files.When adding other information mark it clearly as such with a different color"
        )  
        

        

        # Poll for the run to complete and retrieve the assistant's messages
        while run.status != "completed":
            time.sleep(1)
            run = client.beta.threads.runs.retrieve(
                thread_id=st.session_state.thread_id,
                run_id=run.id

            )
            

            # retrieve messages added by the assistant
            messages = client.beta.threads.messages.list(
                thread_id=st.session_state.thread_id,

            )

            # process and display assistant messages
            assistant_messages_for_run = [
                message for message in messages
                if message.run_id == run.id and message.role =='assistant'
            ]
            for message in assistant_messages_for_run:
                #full_response = process_message_citations(message)
                full_response = process_message_citations(message)
                st.session_state.messages.append({"role":"assistant", "content":full_response})
                with st.chat_message("assistant"):
                    st.markdown(full_response, unsafe_allow_html=True)
else:
    st.write("Please Upload the file and click on 'Start Chat' to begin conversation")

    

    
