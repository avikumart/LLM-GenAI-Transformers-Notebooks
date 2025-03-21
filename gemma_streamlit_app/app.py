import os
import streamlit as st
import pandas as pd
import ollama

# set the config page
st.set_page_config(page_title="AI chatbot", page_icon="🤖", layout="centered", initial_sidebar_state="expanded")

# define the predict function to predict the response from the given prompt
def predict(prompt):
    response = ollama.generate(model="llama3.2:latest", prompt=prompt)
    return response['response']

st.markdown("# AI Chatbot")
st.markdown("This is an AI chatbot that can generate text based on the given prompt.")
st.markdown("You can start by typing a prompt in the text box below and then click on the 'Generate' button to see the response from the chatbot.")

def set_background():
    page_bg_img = '''
    <style>
    
    #MainMenu, header, footer {visibility: hidden;}

    [data-testid="stSidebar"][aria-expanded="true"] > div:first-child { 
    width: 275px;
    }]

    </style>
    '''
    st.markdown(page_bg_img, unsafe_allow_html=True)

set_background()

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Type a message..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    with st.chat_message("bot"):
        with st.spinner("Generating response..."):
            response = predict(prompt)
            st.markdown(response)
            st.session_state.messages.append({"role": "bot", "content": response})


