import random
import pandas as pd
import requests
from dotenv import load_dotenv
import os
import streamlit as st

# Load environment variables from .env file
load_dotenv()
API_KEY = os.getenv("OPENROUTER_API_KEY")

# streamlit ui for the chatbot and taking input models from users
def get_user_input():
    st.title("Multi-LLM Chatbot")
    prompt = st.text_input("Please enter your prompt:")
    model = st.selectbox("Please select the model you want to use:", ["gpt-4", "gpt-3.5", "gpt-4-32k","gpt-3.5-turbo","mistral-7b-instruct","llama-3.1-70b-instruct","llama-3.1-8b-instruct","llama-3.1-70b-chat","llama-3.1-8b-chat"])
    num_responses = st.number_input("How many responses do you want?", min_value=1, max_value=5, value=3)
    return prompt, model, num_responses

# streamlit ui for displaying the chatbot ui
def display_chatbot_ui(prompt, model, num_responses):
    st.write(f"\nYou asked: {prompt}")
    st.write(f"Using model: {model}")
    st.write(f"Number of responses requested: {num_responses}\n")

# use openrouter api to get multiple model responses
def get_openrouter_responses(prompt, model="gpt-4", num_responses=3):
    url = f"https://openrouter.ai/api/v1/completions"
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": model,
        "prompt": prompt
    }
    responses = []
    for _ in range(num_responses):
        response = requests.post(url, headers=headers, json=payload)
        if response.status_code == 200:
            responses.append(response.json())
        else:
            print(f"Error: {response.status_code}")
    return responses

# streamlit UI for the front end ui to take input model from the list of the models and display the responses
def main():
    prompt, model, num_responses = get_user_input()
    display_chatbot_ui(prompt, model, num_responses)
    
    responses = get_openrouter_responses(prompt, model, num_responses)
    
    if responses:
        print("\nResponses received:")
        for i, response in enumerate(responses):
            print(f"Response {i + 1}: {response.get('text', 'No text found')}")
    else:
        print("No responses received.")
    # Display responses in the Streamlit app
    for i, response in enumerate(responses):
        st.write(f"**Response {i + 1}:** {response.get('text', 'No text found')}")  

if __name__ == "__main__":
    main()
    st.write("Chatbot is ready to use!")


