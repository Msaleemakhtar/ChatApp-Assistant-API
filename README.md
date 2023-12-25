
# ChatGPT - Chat App Using Assistants API(Knowledge Retrieval) 🤖💬

## Introduction
Welcome to the ChatGPT web application, a powerful tool that harnesses the capabilities of OpenAI's Assistants API. This Streamlit-based app lets users engage in real-time conversations with AI, leveraging context from uploaded documents. Additionally, it provides features such as web scraping, PDF conversion, and efficient file management.

## Features 🚀
* **Real-time AI Chat:** Engage in dynamic conversations with the AI, incorporating context from uploaded documents.
* **Web Scraping:** Extract valuable information by scraping text content from provided URLs.
* **PDF Conversion:** Convert scraped text or any textual data into convenient PDF files.
* **File Upload and Management:** Easily upload and manage PDF files within the app to enhance AI conversations.
* **Contextual Responses:** The AI utilizes uploaded documents to provide informed and context-aware responses.
* **Citations and References:** Boost the reliability of AI responses with citations and references to uploaded documents.

## Requirements 🛠️
* Python 3.6 or higher
* Streamlit
* Requests library
* Beautiful Soup 4
* PDFKit library
* wkhtmltopdf (PDFKit dependency)

## Create a Python Environment
```shell
conda create --name myenv3_11 python=3.12.0
conda env list
conda activate myenv3_11
python --version
```
## Setup Instructions 🛠️
```shell
Copy code
pip install streamlit openai requests beautifulsoup4 pdfkit
```
## API Key Configuration 🔑
* Securely input your OpenAI API key into the Streamlit app's sidebar to authenticate your API requests.

##  Installation
Ensure that wkhtmltopdf is installed and accessible in your system's PATH for PDF conversion with pdfkit.

## Usage Guide 📝
* the Streamlit app
```shell
Copy code
streamlit run main.py
```
* Optionally, scrape web content and convert it to a PDF for the AI to use as context.
* Input your OpenAI API key in the provided sidebar field.
* Upload any documents you want the AI to reference during the conversation.
* Initiate the chat by clicking "Start Chat" and begin your conversation with the AI.

## Contributing 🤝
* If you'd like to contribute to the project, please fork the repository and issue a pull request with your suggested changes. Happy coding! 🚀🎉


