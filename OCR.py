from PIL import Image
import easyocr
import google.generativeai as genai
import numpy as np

# pip install easyocr use this to install easyocr

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

## Function to load Google Gemini Vision model and get response
def get_gemini_response(system_prompt, text):
    model = genai.GenerativeModel(
        model_name="gemini-pro",
        generation_config=MODEL_CONFIG,
        safety_settings=safety_settings
    )
    Total_text = system_prompt+text
    # print(Total_text)
    response = model.generate_content(Total_text)
    return response.text


# Load the image
# image_path = "/content/festisite_drivers-license-uk.png"
# image = Image.open(image_path)
image_path = "/content/maxresdefault.jpg"
image = Image.open(image_path)

# Convert image to RGB mode to ensure compatibility
image = image.convert("RGB")

# Convert PIL image to numpy array
image_np = np.array(image)

# Extract text from the image using EasyOCR with GPU disabled
reader = easyocr.Reader(['en'], gpu=False)
result = reader.readtext(image_np ,detail=0)
# print(result)
extracted_text = " ".join(result)
# print(extracted_text)
# extracted_text = " ".join([text for text, _, _ in result])

# Define system prompt
system_prompt = """Please identify the type of card from the provided text. 
Here are the criteria:

1. If the text contains 'income tax' or similar words, it's a Pan card.
2. Texts related to 'election' or 'election commission' indicate a voter ID card.
3. Any text mentioning 'driving' suggests a driving license.
4. If none of the above criteria are met, it's an Aadhar Card.
provided text:"""

# Pass extracted text through Google Gemini Vision model for classification
# get_gemini_response(system_prompt,extracted)
response = get_gemini_response(system_prompt, extracted_text)

print("The Response is:")
print(response)
