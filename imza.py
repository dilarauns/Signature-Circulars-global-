import base64
import requests
import fitz 
from PIL import Image  
from dotenv import load_dotenv
import cv2
import numpy as np
import os

load_dotenv()
chat_api_key = os.getenv('CHAT_API_KEY')
api_key = chat_api_key  


def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')



def process_pdf(pdf_file):
    pdf_document = fitz.open(pdf_file)
    responses = []

    for page_num in range(len(pdf_document)):
        print(page_num)
        page = pdf_document.load_page(page_num)

       
        image_list = page.get_pixmap()
        img = Image.frombytes("RGB", [image_list.width, image_list.height], image_list.samples)

        
        img_cv = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)

    
        temp_image_path = f"temp_page_{page_num}.jpg"
        cv2.imwrite(temp_image_path, img_cv)

        
        base64_image = encode_image(temp_image_path)

        
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
                            "text": "Belgede görülen adres bilgisini ve tarih bilgisini bul."
                        },
                        {
                            "type": "text",
                            "text": "Belgede görülen her imzanın altında, üstünde veya etrafında bulunan imzaları belirleyin. Hangi kişinin hangi imzayı attığını tespit edin."
                        },
                        {
                            "type": "text",
                            "text": "Bu imzaların sahiplerini belirleyerek, her birinin belgedeki rolünü veya pozisyonunu yazın. Örneğin, imza sahiplerinin hangi departmana veya yetki alanına ait olduklarını açıklayın."
                        }
                       
                    ]
                }
            ],
            "max_tokens": 1000
        }

     
        response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
        responses.append(response.json())

        
        os.remove(temp_image_path)

    pdf_document.close()
    return responses

pdf_file = "imza_sirkuleri_ornek-rotated.pdf"


responses = process_pdf(pdf_file)


for response in responses:
    for choice in response['choices']:
        content = choice['message']['content']
        print(content)
        
