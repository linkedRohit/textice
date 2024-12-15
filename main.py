# 1. Importing necessary libraries
import streamlit as st  # Import the Streamlit library
import random  # Import the random library
import time  # Import the time library

# 2. Creating a title for our streamlit web application
st.title("Simple chat")  # Set the title of the web application

# 3. Initializing the chat history in the session state (how the chatbot tracks things)
if "messages" not in st.session_state:  # Check if "messages" exists in session state
    st.session_state.messages = []  # Initialize "messages" as an empty list

# 4. Displaying the existing chat messages from the user and the chatbot
for message in st.session_state.messages:  # For every message in the chat history
    with st.chat_message(message["role"]):  # Create a chat message box
        st.markdown(message["content"])  # Display the content of the message

# 5. Accepting the user input and adding it to the message history
if prompt := st.chat_input("What is up?"):  # If user enters a message
    with st.chat_message("user"):  # Display user's message in a chat message box
        st.markdown(prompt)  # Display the user's message
    st.session_state.messages.append({"role": "user", "content": prompt})  # Add user's message to chat history

# 6. Generating and displaying the assistant's response
with st.chat_message("assistant"):  # Create a chat message box for the assistant's response
    message_placeholder = st.empty()  # Create an empty placeholder for the assistant's message
    full_response = ""  # Initialize an empty string for the full response
    assistant_response = random.choice([
        "Hello there! How can I assist you today?",
        "Hi, human! Is there anything I can help you with?",
        "Do you need help?"
    ])  # Select assistant's response randomly

    # Simulate "typing" effect by gradually revealing the response
    for chunk in assistant_response.split():  # For each word in the response
        full_response += chunk + " "
        time.sleep(0.05)  # Small delay between each word
        message_placeholder.markdown(full_response + "▌")  # Update placeholder with current full response and a blinking cursor

    message_placeholder.markdown(full_response)  # Remove cursor and display full response
    st.session_state.messages.append({"role": "assistant", "content": full_response})  # Add assistant's response to chat history
    
# This implementation is taken directly from Streamlits documentation here and is far from the final product that we’ll get to. However, this simple code with comments is a great way to understand how the chatbot (and chatbots in general) function at their core.

# Running this chatbot — To give this simple chatbot a go:
# 1) Go to File > Open Folder and select the folder containing your chatbot project (main.py file).
# 2) Open the integrated terminal by going to View > Terminal
# 3) In the terminal, type streamlit run main.py and press enter.
# 4) After running the command, Streamlit will display a URL in the terminal (usually http://localhost:8501/), and your chatbot should load so that you can play around with it!


# Actual output from the Innovation Pilot; includes many advanced features
# Advanced Chatbot Features
# Now that we understand how a basic streamlit chatbot works at the core, let’s take a look at how we can build one with the following functionalities.

# NOTE: For a completed GenAI chatbot template which incorporates and packages up these features and more, check out my repository here.

# Incorporate OpenAI/LLM responses. Instead of the random phrases from above, looping in an LLM like OpenAI will allow us to summarize, criticize, converse, and all of the other magic you’ve seen ChatGPT do.
# An implementation of a response function which captures the initial message,
# last chatbot message, last user message, and constructs a prompt with this
# Note: This does not included indexed information (more on that below)

def generate_response(prompt, history, model_name, temperature):
      # Get the last message sent by the chatbot
      chatbot_message = history[-1]['content']

      # Extract the user's initial message from history
      first_message = history[1]['content']

      # Extract the last message sent by the user
      last_user_message = history[-2]['content']
    
      # Now, we're creating a 'full_prompt'. Think of this as the complete message we send to the chatbot, giving it all the context it needs to understand our request.
      # The '\n\' line breaks and the '###' help to structure our prompt in a more understandable format for an LLM.
      full_prompt = f"{prompt}\n\
      ### The original message: {first_message}. \n\
      ### Your latest message to me: {chatbot_message}. \n\
      ### Previous conversation history for context: {history}"
      
      # Generate a response using OpenAI API
      api_response = openai.ChatCompletion.create(
        model=model_name, # Specifying which model to use. This can be hardcoded or passed as a user value depending on your use case.
        temperature=temperature,
        messages=[
            {"role": "system", "content": full_prompt},
            {"role": "user", "content": last_user_message},
        ]
      )
      
      # Then we add this part of the response to our 'full_response' placeholder.
      full_response = api_response['choices'][0]['message']['content']

      # After getting the chatbots full response, we package it in a specific format and present it as the final result of this function.
      yield {"type": "response", "content": full_response}