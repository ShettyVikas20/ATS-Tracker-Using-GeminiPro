from fastapi import APIRouter,File,UploadFile
import random
from PIL import Image
import base64
from io import BytesIO
import pandas as pd
import fitz
import google.generativeai as genai
import tempfile
import os
import shutil
from pathlib import Path
import json


home_api_router = APIRouter()

GEMINI_API = "AIzaSyD-HzbQwUFUN9libpS9NtXvYWVq8ibXCTA"

generation_config = {
    "temperature": 0,
    "top_p": 1,
    "top_k": 1,
    "max_output_tokens": 400,
}

safety_settings = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
]

genai.configure(api_key=GEMINI_API)
model_vision = genai.GenerativeModel("gemini-pro-vision", safety_settings=safety_settings)




def save_upload_file(upload_file: UploadFile, destination: Path) -> str:
    try:
        with destination.open("wb") as buffer:
            shutil.copyfileobj(upload_file.file, buffer)
            file_name = buffer.name
            print(type(file_name))
    finally:
        upload_file.file.close()
    return file_name


def delete_file(filename):
    try:
        os.remove(filename)
    except:
        return NULL




def pdf2img(pdf_path):
        pdf_document = fitz.open(pdf_path)
        image_list = []

        for page_number in range(pdf_document.page_count):
            page = pdf_document[page_number]
            image_list.append(page.get_pixmap())

        pdf_document.close()

        images = [
            Image.frombytes("RGB", (image.width, image.height), image.samples)
            for image in image_list
        ]

        # Combine all images vertically
        combined_image = Image.new(
            "RGB", (images[0].width, sum(image.height for image in images))
        )
        offset = 0

        for image in images:
            combined_image.paste(image, (0, offset))
            offset += image.height

        # Save the combined image
        combined_image.save("temp.jpeg", "JPEG")
        

def evaluate_answer(job_discription,resume_pdf_path,input):
    extracted_text = ""
    additional_points = ""
    image_string = ""
    try:
        print('[+]Converting pdf to image')
        pdf2img(resume_pdf_path)
        resume = Image.open("temp.jpeg")

    
        
        
        response=model.generate_content([input,resume,job_discription])
        
        
    

        print(f"{response.text}")
        
        return response.text
    except Exception as e:
        print(f"[-]Error during evaluation : {str(e)}") 
        return -1










@home_api_router.post('/home')
async def home(job_discription:str , resume: UploadFile = File()):
    
    
    resume_path = save_upload_file(resume, Path(f"resume.pdf"))
    
    
    input_prompt1 = """
 You are an experienced Technical Human Resource Manager,your task is to review the provided resume against the job description. 
  Please share your professional evaluation on whether the candidate's profile aligns with the role. 
 Highlight the strengths and weaknesses of the applicant in relation to the specified job requirements.
"""


    result = get_gemini_response(job_discription_path,resume_path,input_prompt1)
    
    
    #print(f"{file_one_path},,{file_two_path}")
    
    delete_file("resume.pdf")
    delete_file("resume.jpeg")

    print('[+]done: complited')
    #return result
    

    json_data=json.dumps(result)


    return {json_data}







