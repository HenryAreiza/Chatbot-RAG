import os
import torch
from langchain_community.vectorstores import Chroma
from langchain.memory import ConversationBufferWindowMemory
from langchain.chains import ConversationalRetrievalChain

class Chatbot:
    """
    Class to create a chatbot.

    This class provides functionality for creating and interacting with a chatbot.

    Attributes:
        embeddings (obj): Embeddings class object
        llm (obj): Large Language Model object
        vectorstore (obj): Vector store for RAG
        memory (obj): Chat memory object
        conversation (obj): Conversation chain object
    """

    def __init__(self, prod=True, openai=[True, True]):
        """
        Initializes the Chatbot class.

        Args:
            prod (bool): Production deployment flag
            openai (list): Embeddings and Models type {True:OpenAI, False:Local}
        """
        if prod:
            import streamlit as st
            os.environ['OPENAI_API_KEY'] = st.secrets['OPENAI_API_KEY']
        else:
            from dotenv import load_dotenv, find_dotenv
            _ = load_dotenv(find_dotenv())

        if openai[0]:
            from langchain_openai import OpenAIEmbeddings
            self.embeddings = OpenAIEmbeddings()
        else:
            from langchain_community.embeddings import HuggingFaceInstructEmbeddings
            embedding_model = os.path.join('models','embedding','distiluse-base-multilingual-cased-v1')
            self.embeddings = HuggingFaceInstructEmbeddings(model_name=embedding_model,
                                                model_kwargs = {'device':'cuda'})
        if openai[1]:
            from langchain_openai import ChatOpenAI
            self.llm = ChatOpenAI(model_name='gpt-3.5-turbo-1106', temperature=0)
        else:
            from langchain_community.llms.huggingface_pipeline import HuggingFacePipeline
            from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline, BitsAndBytesConfig
            nf4_config = BitsAndBytesConfig(
                load_in_4bit=True,
                bnb_4bit_quant_type='nf4',
                bnb_4bit_use_double_quant=True,
                bnb_4bit_compute_dtype=torch.bfloat16
            )
            llm_model = os.path.join('models','llm','zephyr-7b-alpha')
            tokenizer = AutoTokenizer.from_pretrained(llm_model)
            model = AutoModelForCausalLM.from_pretrained(llm_model,
                                                        quantization_config=nf4_config,
                                                        torch_dtype=torch.bfloat16,
                                                        device_map=0)
            pipe = pipeline("text-generation", model=model, tokenizer=tokenizer, max_new_tokens=500)
            self.llm = HuggingFacePipeline(pipeline=pipe, pipeline_kwargs={'device':0})
        
        self.vectorstore = Chroma(
            embedding_function=self.embeddings
        )
        self.memory = ConversationBufferWindowMemory(k=2, memory_key='chat_history', return_messages=True)
        self.conversation = ConversationalRetrievalChain.from_llm(
            llm=self.llm,
            retriever=self.vectorstore.as_retriever(search_type="mmr",
                                            search_kwargs={'k':3}),
            memory=self.memory
        )
    
    def update_dataset(self, chunks):
        """
        Update the knowledge dataset of the chatbot.

        Args:
            chunks (list): List of splited documents
        """
        _ = self.vectorstore.add_documents(chunks)
        self.conversation = ConversationalRetrievalChain.from_llm(
            llm=self.llm,
            retriever=self.vectorstore.as_retriever(search_type="mmr",
                                            search_kwargs={'k':3}),
            memory=self.memory
        )
