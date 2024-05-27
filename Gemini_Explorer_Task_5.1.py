import time
import vertexai
import streamlit as st
from vertexai.preview import generative_models
from vertexai.preview.generative_models import GenerativeModel, Part, Content, ChatSession

# Initialize project
project = "rising-amp-423822-n8"
vertexai.init(project=project)

config = generative_models.GenerationConfig(
    temperature=0.4
)

# Load model with config
start_time = time.time()
model = GenerativeModel(
    "gemini-pro",
    generation_config=config
)
load_time = time.time() - start_time
st.write(f"Model loaded in {load_time:.2f} seconds")
print(f"Model loaded in {load_time:.2f} seconds")

chat = model.start_chat()
st.write("Chat session started")
print("Chat session started")

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.user_name = ""
    st.session_state.initial_prompt_sent = False
    st.write("Session state initialized")
    print("Session state initialized")

# Set title
st.title("Gemini Explorer")

# Capture user name
if not st.session_state.user_name:
    st.session_state.user_name = st.text_input("Please enter your name")
else:
    # Initial message startup logic
    if not st.session_state.initial_prompt_sent:
        st.write("Sending initial prompt")
        print("Sending initial prompt")
        initial_prompt = f"Hey {st.session_state.user_name}! I'm ReX, an assistant powered by Google Gemini. I use emojis to be interactive."

        st.session_state.messages.append(
            {
                "role": "model",
                "content": initial_prompt  # Use the initial prompt directly
            }
        )
        with st.chat_message("model"):
            st.markdown(initial_prompt)  # Display the initial prompt directly

        st.session_state.initial_prompt_sent = True

    # Display and load chat history
    st.write("Displaying chat history")
    print("Displaying chat history")
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Capture user input
    query = st.chat_input("Enter your message:")

    if query:
        st.write("Processing user input")
        print("Processing user input")
        if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
            st.error("Please wait for the model to respond before sending another message.")
        else:
            def llm_function(chat: ChatSession, query, role="user"):
                st.write("Sending message to model")
                print("Sending message to model")
                start_time = time.time()
                try:
                    response = chat.send_message(query)
                    response_time = time.time() - start_time
                    st.write(f"Message sent to model and response received in {response_time:.2f} seconds")
                    print(f"Message sent to model and response received in {response_time:.2f} seconds")
                    output = response.candidates[0].content.parts[0].text

                    if role != "initial_prompt":
                        st.session_state.messages.append(
                            {
                                "role": role,
                                "content": query
                            }
                        )
                        with st.chat_message("user"):
                            st.markdown(query)

                    st.session_state.messages.append(
                        {
                            "role": "model",
                            "content": output
                        }
                    )
                    with st.chat_message("model"):
                        st.markdown(output)
                except Exception as e:
                    st.error("An error occurred while processing the response. Please try again.")
                    st.write(f"Error: {e}")
                    print(f"Error: {e}")
            llm_function(chat, query, role="user")
