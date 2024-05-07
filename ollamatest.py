import streamlit as st
import ollama
import json


def simplereq():
    response = ollama.chat(model='llava', messages=[
        {
            'role': 'user',
            'content': 'please provide a summary from the content at this link: https://twitter.com/GreaterKashmir/status/1778058864476500166 . please output as a JSON object with summary and resources as items',
        },
    ])
    print(response['message']['content'])
    return response['message']['content']


st.title("Testing Ollama inside Streamlit")
testit = st.button("Test Ollama")

if testit:
    response = simplereq()
    try:
        # Attempt to parse JSON object
        data = json.loads(response)
        # Assign fields to variables
        summary = data.get('summary', 'Summary not available')
        # resources = data.get('resources', [])
        # Display summary and resources
        st.header("Summary")
        st.write(summary)
        # st.header("Resources")
        # st.write(resources)
    except json.JSONDecodeError as e:
        st.write(response)
        st.error("Error decoding JSON response from Ollama. Please check the response format.")
