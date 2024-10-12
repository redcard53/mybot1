import openai
import streamlit as st

 # Set your OpenAI API key
openai.api_key = st.secrets["OPENAI_API_KEY"]

# Function to generate a response
def generate_text(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are well read journalist and are aware of the recent performance of India in Paralympics."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=50,  # Adjust token length as needed
        stream=True  # Enable streaming
    )
    return response

# Streamlit setup
st.title("Paralympics Chatbot")

# Session state to store chat history
if 'messages' not in st.session_state:
    st.session_state['messages'] = []

# Chat input
user_input = st.text_input("You: ", placeholder="Ask me about India's performance in the Paralympics...")

if user_input:
    # Append user's message to chat history
    st.session_state['messages'].append({"role": "user", "content": user_input})

    # Get chatbot's response
    with st.spinner("Bot is responding..."):
        # Streaming the response
        response_stream = generate_text(user_input)
        bot_response = ""
        for chunk in response_stream:
            if 'choices' in chunk:
                chunk_text = chunk['choices'][0]['delta'].get('content', '')
                bot_response += chunk_text
                st.markdown(bot_response + "▌")  # Adding a streaming cursor effect
        st.session_state['messages'].append({"role": "assistant", "content": bot_response})

# Display conversation history
if st.session_state['messages']:
    for message in st.session_state['messages']:
        if message['role'] == 'user':
            st.write(f"**You**: {message['content']}")
        else:
            st.write(f"**Bot**: {message['content']}")
