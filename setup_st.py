# Example of a setup_st.py file which is called in your main file to setup the UI/UX and initialize the session

#1. Function to set up the page's layout and design elements
def set_design():
    # Creating a 3-column layout for the Streamlit app
    col1, col2, col3 = st.columns([1, 2, 1])
    
    # The main logo will be displayed in the middle column
    with col2:
        # Loading and displaying a logo image from the repository, and centering it
        st.image("sample_logo.png", use_column_width=True)

    # Adding a title to the Streamlit app, center-aligned
    st.markdown("<p style='text-align: center; font-size: 30px;'><b>[Sample Generative AI Chatbot]</b></p>", unsafe_allow_html=True)

# 2. Function to initialize variables that will hold the state of the app (illustrative list, not complete)
def initialize_session_state():
    # Used to generate the initial message for the conversation
    if 'messages' not in st.session_state:
        st.session_state['messages'] = [
            {"role": "assistant", "content": "Hi there, what can I help you with today?"}
        ]
    # Can be used to make the chatbot end the convo or perform an action when some limit is reached
    if 'message_count' not in st.session_state:
        st.session_state['message_count'] = 0
    # Initializes the model_name session state variable
    if 'model_name' not in st.session_state:
        st.session_state['model_name'] = ""
    # Initializes the temperature session state variable
    if 'temperature' not in st.session_state:
        st.session_state['temperature'] = []
    # Initializes the OpenAI API key variable
    if 'api_key' not in st.session_state:
        st.session_state['api_key'] = ""
    # Initializes the use index variable to determine if we use index in replies
    if 'use_index' not in st.session_state:
        st.session_state['use_index'] = False

# 3. Function to initialize the sidebar UI elements
def sidebar():
    # Adding a header to the sidebar
    st.sidebar.markdown("""
    <h1 style='color: black; font-size: 24px;'>Chatbot Configuration</h1>
    """, unsafe_allow_html=True)

# 4.Function to create a 'Clear Conversation' button on the sidebar
def clear_button():
    # Creating the 'Clear Conversation' button
    clear_button = st.sidebar.button("Clear Conversation", key="clear")
    
    # If the button is clicked, this block will execute and the conversation will clear
    if clear_button:
        st.session_state['messages'] = [
            {"role": "assistant", "content": "Hi there, what can I help you with today?"}
        ]
        st.session_state['message_count'] = 0

# 5. Function to track the conversation for download functionality
def download_convo():
    # Checking if there are enough messages to download
    if 'messages' in st.session_state and len(st.session_state['messages']) > 0:
        # Concatenating all messages into a single string
        full_conversation = "\n".join([
            f"\n{'-'*20}\n"
            f"Role: {msg['role']}\n"
            f"{'-'*20}\n"
            f"{msg['content']}\n"
            for msg in st.session_state['messages']
        ])
        return full_conversation
    else:
        # If not enough messages, show a warning
        st.warning("There aren't enough messages in the conversation to download it. Please refresh the page")
        return ""

# 6. Function to create a 'Download Conversation' button on the sidebar
def download_button():
    # Generating the full conversation text
    full_conversation = download_convo()
    
    # Creating a download button for the full conversation
    st.sidebar.download_button(
        label="Download conversation",
        data=full_conversation,
        file_name='conversation.txt',
        mime='text/plain'
    )
Add user-customizable chatbot configurations. This is where you can be most creative. Some of the ones I looped into the Innovation CoPilot include GPT model selection, temperature (randomness) adjustment, custom prompts, API keys, and more.
# Note: Add this code into your setup_set.py file
#7.  This function is designed to capture the user's preferences for how the chatbot should respond. The possibilities here are endless!
def get_user_config():
    # Define a few AI models the user can choose from.
    model_options = {
        "GPT-3.5 Turbo (16K tokens)": "gpt-3.5-turbo-16k-0613", # Recommended as it has a 16K token limit, much higher than the other two. This allows longer 'memory recall'.
        "GPT-3.5 Turbo": "gpt-3.5-turbo", # Fewer token version of above - not recommended
        "GPT-4": "gpt-4" # Latest model from OpenAI. Recommended for complex chatbots, though has a lower token limit, higher token usage cost, and slower returns.
    }

    # Display button choices in the sidebar of the app for the user to pick their desired model from the ones just defined.
    st.sidebar.markdown("<b style='color: darkgreen;'>Choose a GPT model:</b>", unsafe_allow_html=True) # HTML for beautifying the label, not necessary
    # Create the radio button. Label is hidden (since we have HTMl label), it defaults to the first option (turbo 16k) of the model_options above.
    model_name = st.sidebar.radio("", list(model_options.keys()), index=0, label_visibility="collapsed") 

    # Display a slider option for the user to choose 'temperature' or randomness of the chatbot responses. Higher values are recommended for creative chatbots.
    st.sidebar.markdown("<b style='color: darkgreen;'>Choose a temperature (randomness):</b>", unsafe_allow_html=True)
    temperature = st.sidebar.slider("", min_value=0.1, max_value=1.0, value=0.5, step=0.1, label_visibility="collapsed")

    # Display an input text box to capture user's OpenAI API key so that the chatbot will be able to generate responses
    st.sidebar.markdown("<b style='color: darkgreen;'>Enter OpenAI API Key to use chatbot:</b>", unsafe_allow_html=True)
    api_key = st.sidebar.text_input("", type="password", label_visibility="collapsed")  # Hides the entered text for privacy

    # Display a checkbox to include users data so that the chatbot will be able to append information to its responses
    st.sidebar.markdown("<b style='color: darkgreen;'>Use indexed data for responses:</b>", unsafe_allow_html=True)
    use_index = st.sidebar.checkbox("", value=st.session_state.get('use_index', False), label_visibility="collapsed")

    # Save the values to the Streamlit 'memory' to be used later
    st.session_state['model_name'] = model_options[model_name]
    st.session_state['temperature'] = temperature
    st.session_state['api_key'] = api_key
    st.session_state['use_index'] = use_index