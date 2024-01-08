import time, sys, os
from typing import Any
import streamlit as st
import google.generativeai as genai

def type_text(text: str, delay: float = 0.03):
    with st.empty():  # Use st.empty for dynamic text
        current_text = ""  # Track the currently typed text
        for char in text:
            current_text += char
            st.session_state.text = current_text  # Update the text
            st.write(current_text, unsafe_allow_html=True)  # Update and render
            time.sleep(delay)
st.title("OpenAI Chatbot")

genai.configure(api_key=st.secrets["api_key"])

if "gemini_model_name" not in st.session_state:
    st.session_state["gemini_model_name"] = "models/chat-bison-001"

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ask me about something"):
    with st.chat_message("user"):
        st.markdown(prompt)

    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("assistant"):
        # Display a spinner while fetching the response
        spinner_container = st.empty()
        with spinner_container:
            spinner = st.text(" AI is thinking...")
            full_response = ""

            display_model_name = st.session_state["gemini_model_name"]

            # Generate a response to the user prompt
            response = genai.chat(model=display_model_name, prompt=prompt, temperature=0.1)

            # Check if the response object and 'last' attribute are present
            if response and hasattr(response, 'last') and response.last:
                # Stop the spinner
                full_response = response.last
                # Create an empty placeholder for dynamic content
                response_placeholder = st.empty()
                # Display the full response with typing animation
                type_text(full_response)
            else:
                # Handle the case where response is None or 'last' attribute is not present
                full_response = "I'd like to inform you that, as an AI language model, I lack the ability to perform physical actions, access real-time data, execute code in external systems, or offer personal experiences or opinions. My expertise lies in processing and generating text, drawing insights from the data on which I've been trained. If you have any inquiries within these confines, please feel free to ask!"
                st.markdown(full_response)

        st.session_state.messages.append({"role": "assistant", "content": full_response})