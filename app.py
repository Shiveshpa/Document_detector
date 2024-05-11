import streamlit as st
from PIL import Image

import os
import google.generativeai as genai


MODEL_CONFIG = {
      "temperature": 0.5,
      "top_p": 1,
      "top_k": 32,
      "max_output_tokens": 4096,
    }

    ## Safety Settings of Model
safety_settings = [
    {
        "category": "HARM_CATEGORY_DANGEROUS",
        "threshold": "BLOCK_NONE",
    },
    {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_NONE",
    },
    {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_NONE",
    },
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_NONE",
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_NONE",
    },
]

# genai.configure(api_key='AIzaSyCik4UK646hpxLD5XugbOH6lPU48ngYCOE')
## Function to load OpenAI model and get respones

def get_gemini_response(system_prompt, image):
    print(image)
    model = genai.GenerativeModel(model_name="gemini-pro-vision",
                                  generation_config=MODEL_CONFIG,
                                  safety_settings=safety_settings)
    response = model.generate_content([system_prompt, image])
    
    # Check if the response contains parts
    return response.text




##initialize our streamlit app

st.set_page_config(page_title="Check your document?")

st.header("Government ID card detector")
system_prompt = """Please identify the type of card from the provided image. 
Here are the criteria:

1.If the image contains text related to 'income tax' or similar words, it's a Pan card so return "Pan card".
2.If a 12-digit Aadhar card number is detected, it's an Aadhar card so return "Aadhar card".
3.Texts related to 'election' or 'election commission' indicate a voter ID card so return "voter ID card".
4.Any text mentioning 'driving' suggests a driving license so return "Driving license".
If none of the above criteria are met, it's not a recognized card return "some other card" . jsut print which card is no extra information and that too in english only"""

uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
image=""   
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image.", use_column_width=True)


submit=st.button("Check!!")

if submit:
    
    response=get_gemini_response(system_prompt,image)
    st.subheader("The Response is")
    print(response)
    st.write(response)
