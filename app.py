import openai
import streamlit as st

# Access the API key from Streamlit secrets
openai.api_key = st.secrets["OPENAI_API_KEY"]

# Function to generate text with continuous stream
def generate_text(prompt):
    # Initialize an empty string for the response
    response_text = ""

    # Create a placeholder to update the message progressively
    chat_placeholder = st.empty()

    # Stream the response from the API
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a well-read journalist aware of India's recent performance in the 2024 Paralympics."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=200,  # Adjust token length as needed
        stream=True
    )

    # Update the response in chunks to simulate streaming
    for chunk in response:
        # Extract and append the latest part of the response
        response_text += chunk['choices'][0]['delta'].get('content', '')
        chat_placeholder.write(response_text)

    # Return final response text
    return response_text

# Streamlit UI setup
st.title("My first bot")
st.write("anything ")

# User input
user_input = st.text_input("You:", placeholder="Type your question here...")

# If there's a user input, get the response from the chatbot
if user_input:
    st.write("You: " + user_input)
    generate_text(user_input)
