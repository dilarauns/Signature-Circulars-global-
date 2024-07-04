import base64
import requests

# OpenAI API Key
api_key = "sk-ai-job-create-1-3KixuXJqlV18iZMyR0khT3BlbkFJg4HYk1U5ScZoShlaIv3E"

# Function to encode the image
def encode_image(image_path):
  with open(image_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')

# Path to your image
image_path = "imza.png"

# Getting the base64 string
base64_image = encode_image(image_path)

headers = {
  "Content-Type": "application/json",
  "Authorization": f"Bearer {api_key}"
}

payload = {
  "model": "gpt-4o",
  "messages": [
    {
      "role": "user",
      "content": [
        {
          "type": "text",
          "text": "Find the signatures in the image and give the name of the signature owner."
        },
        {
          "type": "image_url",
          "image_url": {
            "url": f"data:image/jpeg;base64,{base64_image}"
          }
        }
      ]
    },
    {
      "role": "user",
      "content": [
        {
          "type": "text",
          "text": "Who are the individuals that signed this document?"
        },
        {
          "type": "text",
          "text": "Provide names of the individuals whose signatures are visible."
        }
      ]
    }
  ],
  "max_tokens": 300
}


response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)

print(response.json())