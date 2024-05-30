import json
import re
import os
import openai
import logging
import base64
import requests
from dotenv import load_dotenv

load_dotenv()

# Ensure the OpenAI API key is set
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

# Ensure the OpenAI API key is set
if not OPENAI_API_KEY:
    raise ValueError("The OPENAI_API_KEY environment variable is not set.")

openai.api_key = OPENAI_API_KEY
def process_image_with_ai(image_path):
    try:
        # Open the image file
        with open(image_path, "rb") as image_file:
            # Encode image to base64
            image_base64 = base64.b64encode(image_file.read()).decode('utf-8')
        
        # Prepare the payload for OpenAI API
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {OPENAI_API_KEY}"
        }

        payload = {
            "model": "gpt-4o",
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text", 
                            "text": "This is an image of a recipe, please analyze and parse the text into 2 arrays, 'ingredients' and 'instructions'. Only return the JSON object without any introduction or additional text, your repsonse should look like this {'instructions':[],'ingredients':[]}."
                        },
                        {
                            "type": "image_url", 
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{image_base64}"
                            }
                        }
                    ]
                }
            ],
            "max_tokens": 300
        }

        response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)

        # Check for bad request status and log details
        if response.status_code != 200:
            logging.error(f"Bad Request - Status Code: {response.status_code}")
            logging.error(f"Response: {response.text}")
            response.raise_for_status()
        
        logging.debug(f"AI Response: {response.json()}")

        ai_response = response.json()['choices'][0]['message']['content']

        # Clean and complete the JSON string
        cleaned_json_string = clean_json_string(ai_response)
        ai_response_json = json.loads(cleaned_json_string)

        return ai_response_json

    except requests.exceptions.RequestException as e:
        logging.error(f"Request error during AI processing: {str(e)}")
        return None
    except Exception as e:
        logging.error(f"Error during AI processing: {str(e)}")
        return None
    
def clean_json_string(json_string):
    # Remove any text before the JSON object starts
    json_string = re.sub(r'^[^{]*', '', json_string)
    # Remove any text after the JSON object ends
    json_string = re.sub(r'[^}]*$', '', json_string)
    
    # Try to balance braces
    open_braces = json_string.count('{')
    close_braces = json_string.count('}')
    if open_braces > close_braces:
        json_string += '}' * (open_braces - close_braces)
    elif close_braces > open_braces:
        json_string = json_string[:json_string.rfind('}')]

    return json_string

# Example usage
if __name__ == '__main__':
    image_path = 'path/to/your/image.jpg'
    response = process_image_with_ai(image_path)
    print(response)