#pip install -q -U google-generativeai
#pip install ipywidgets

from dotenv import load_dotenv
load_dotenv()  ## take environment variables from .env (here api key)

import streamlit as st
import os
import pathlib
import textwrap
from PIL import Image ## Import Image from PIL for handling images

import google.generativeai as genai

##Configure Google API key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

## Function to load Gemini-Pro-Vision model and get responses
## We'll use 'gemini-pro-vision' for multimodal capabilities (text & image)
model = genai.GenerativeModel('gemini-2.0-flash')

def get_gemini_response(input_text, image_data):
    if input_text and image_data:
        ## If both text and image are provided, query with both
        response = model.generate_content([input_text, image_data])
    elif image_data:
        ## If only image is provided, describe the image
        response = model.generate_content(image_data)
    else:
        response = model.generate_content(input_text)
    return response.text

## Initialize our streamlit app

st.set_page_config(page_title="Gemini Multimodal Q&A App")

st.header("Gemini Multimodal Application")

input_text = st.text_input("Ask a question about the image or anything else:", key="input")
uploaded_file = st.file_uploader("Upload an image...", type=["jpg", "jpeg", "png"])

image_data = ""
if uploaded_file is not None:
    image_data = Image.open(uploaded_file)
    st.image(image_data, caption="Uploaded Image.", use_column_width=True)

submit = st.button("Get Gemini Response")

## If submit button is clicked
if submit:
    if not input_text and not uploaded_file:
        st.warning("Please provide some text or upload an image to get a response.")
    else:
        with st.spinner("Generating response..."):
            response = get_gemini_response(input_text, image_data)
            st.subheader("Response")
            st.write(response)