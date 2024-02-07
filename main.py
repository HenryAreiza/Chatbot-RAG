"""
HenRick Chat application

Authors: HenryAreiza
Date: 07/02/2024
"""

import streamlit as st
from src.languages import gen_lang, chat_lang
from src.html_templates import css, bot_template
from src.utils import init_vars, print_chat, update, get_docs, get_chunks, uploader_lang


def main():
    """
    Main function for the ENGAGE chat module.

    This function serves as the entry point for the ENGAGE chatbot application.
    """
    henrick_img = 'https://avatars.githubusercontent.com/u/53319367?v=4'
    st.set_page_config(page_title='HenRick Chat', page_icon=henrick_img, layout='wide')
    init_vars()

    with st.sidebar:
        st.markdown(f"<h1 style='text-align: center;'>HenRick Chat</h1>", unsafe_allow_html=True)
        _,logo_col,__ = st.columns((1,4,1))
        with logo_col:
            st.image(henrick_img)
        lang = st.radio('lang', options=['EN','ES','FR'], horizontal=True,
                        label_visibility='collapsed', key='lang')
        uploader_lang(lang, gen_lang)

    st.write(css, unsafe_allow_html=True)

    with st.container():
        st.chat_input(placeholder=chat_lang.get(lang).get('user_question'),
                      key='user_question',
                      on_submit=update,
                      args=(st.session_state.chatbot, lang))

    if len(st.session_state.chat_history) < 1:
        with st.container(height=700):
            st.write(bot_template.replace("{{MSG}}",
                     chat_lang.get(lang).get('message')),
                     unsafe_allow_html=True)
    else:
        print_chat()

    with st.sidebar:
        st.subheader(chat_lang.get(lang).get('subheader'))
        pdfs = st.file_uploader(chat_lang.get(lang).get('process_text'), accept_multiple_files=True)
        if st.button(chat_lang.get(lang).get('process')):
            with st.spinner(chat_lang.get(lang).get('processing')):
                # get pdf text
                docs = get_docs(pdfs, user_folder=st.session_state.user_folder)

                # get the text chunks
                chunks = get_chunks(docs)

                # update conversation chain
                st.session_state.chatbot.update_dataset(chunks)


if __name__ == '__main__':
    main()