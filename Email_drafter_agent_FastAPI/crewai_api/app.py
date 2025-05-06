import streamlit as st
import requests

# Define the FastAPI endpoint URL
API_URL = "http://127.0.0.1:8000/draft-email/"

# Title of the Streamlit app
st.title("Email Drafter")

# Input for the email content
input_email = st.text_area("Enter your email content here:", height=250)

# Button to submit the email for drafting
if st.button("Draft Email"):
    if input_email.strip():
        try:
            # Make the POST request to the FastAPI endpoint
            response = requests.post(API_URL, json={"input_email": input_email})
            
            # Check if the response is successful
            if response.status_code == 200:
                drafted_email = response.json().get("drafted_email", "No email drafted.")
                st.subheader("Drafted Email:")
                st.text_area("Here is your drafted email:", drafted_email['raw'], height=250)
            else:
                st.error(f"Error: {response.status_code} - {response.text}")
        except requests.exceptions.RequestException as e:
            st.error(f"An error occurred: {str(e)}")
    else:
        st.warning("Please enter the email content to draft a response.")
