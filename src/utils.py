import os
import streamlit as st
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain_core.messages import HumanMessage, AIMessage
from src.html_templates import user_template, bot_template
from src.languages import chat_lang
from src.classes import Chatbot


def init_vars():
    """
    Initialize streamlit session variables.
    """
    if 'debug' not in st.session_state:
        st.session_state.debug = False
    if 'prod' not in st.session_state:
        st.session_state.prod = False
    if 'openai' not in st.session_state:
        st.session_state.openai = [True, True]
    if 'chatbot' not in st.session_state:
        st.session_state.chatbot = Chatbot(prod=st.session_state.prod,
                                           openai=st.session_state.openai)
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []

def get_docs(pdfs, user_folder='new'):
    """
    Get list of documents from loaded pdf files.

    Args:
        pdfs (list): Uploaded pdf files
        user_folder (str): User's folder name
    Returns:
        docs (list): List of documents
    """
    docs = []
    for pdf in pdfs:
        temp_file = os.path.join('users',user_folder,'temp.pdf')
        with open(temp_file, "wb") as file:
            file.write(pdf.getvalue())
        loader = PyPDFLoader(temp_file)
        docs.extend(loader.load())
    return docs

def get_chunks(docs):
    """
    Split documents into chunks.

    Args:
        docs (list): List of documents
    Returns:
        chunks (list): List of splited documents
    """
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=1000,
        chunk_overlap=150,
        length_function=len
    )
    chunks = text_splitter.split_documents(docs)
    return chunks

def update(chatbot, lang):       
    """
    Update user interaction with the chatbot.

    Args:
        question (str): User question
        lang (str): Current language of the interface
    """
    if 'chat_history' in st.session_state:
        if len(st.session_state.chat_history) < 1:
            st.session_state.chat_history.insert(0, AIMessage(content=chat_lang.get(lang).get('message')))

        response = chatbot.conversation.invoke({'question': st.session_state.user_question})
        st.session_state.chat_history.insert(0, HumanMessage(content=response['question']))                                      
        st.session_state.chat_history.insert(0, AIMessage(content=response['answer']))

def print_chat():
    """
    Update user interface.
    """
    with st.container(height=800):
        for i, message in enumerate(st.session_state.chat_history):
            if i % 2 == 0:
                st.write(bot_template.replace("{{MSG}}", message.content), unsafe_allow_html=True)
            else:
                st.write(user_template.replace("{{MSG}}", message.content), unsafe_allow_html=True)

def uploader_lang(lang, languages):    
    """
    Addapt the language of the file uploader widget.

    Args:
        lang (str): Current language of the interface
        languages (dict): Language options dictionary
    """
    hide_label = (
        """
    <style>
        div[data-testid="stFileUploader"]>section[data-testid="stFileUploadDropzone"]>button[data-testid="baseButton-secondary"] {
        color:rgba(0, 0, 0, 0.0);
        width: 150px;
        }
        div[data-testid="stFileUploader"]>section[data-testid="stFileUploadDropzone"]>button[data-testid="baseButton-secondary"]::after {
            content: "BUTTON_TEXT";
            color:rgba(128, 128, 128, 0.99);
            display: block;
            position: absolute;
        }
        div[data-testid="stFileDropzoneInstructions"]>div>span {
        visibility:hidden;
        }
        div[data-testid="stFileDropzoneInstructions"]>div>span::after {
        content:"INSTRUCTIONS_TEXT";
        visibility:visible;
        display:block;
        }
        div[data-testid="stFileDropzoneInstructions"]>div>small {
        visibility:hidden;
        }
        div[data-testid="stFileDropzoneInstructions"]>div>small::before {
        content:"FILE_LIMITS";
        visibility:visible;
        display:block;
        }
    </style>
    """.replace(
            'BUTTON_TEXT', languages.get(lang).get('button')
        )
        .replace('INSTRUCTIONS_TEXT', languages.get(lang).get('instructions'))
        .replace('FILE_LIMITS', languages.get(lang).get('limits'))
    )
    st.markdown(hide_label, unsafe_allow_html=True)