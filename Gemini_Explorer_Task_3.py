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
model = GenerativeModel(
    "gemini-pro",
    generation_config=config
)

chat = model.start_chat()

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []
    # Add welcome message
    st.session_state.messages.append(
        {
            "role": "model",
            "content": "Welcome to the Gemini Explorer! How can I assist you today?"
        }
    )

# Helper function to display and send Streamlit messages
def llm_function(chat: ChatSession, query):
    response = chat.send_message(query)
    output = response.candidates[0].content.parts[0].text

    with st.chat_message("model"):
        st.markdown(output)

    st.session_state.messages.append(
        {
            "role": "model",
            "content": output
        }
    )

st.title("Gemini Explorer")

# Display and load chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Capture user input
query = st.chat_input("Enter your message:")

if query:
    if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
        st.error("Please wait for the model to respond before sending another message.")
    else:
        with st.chat_message("user"):
            st.markdown(query)
        st.session_state.messages.append(
            {
                "role": "user",
                "content": query
            }
        )
        llm_function(chat, query)
