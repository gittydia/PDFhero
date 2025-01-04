
import os
from dotenv import load_dotenv
import google.generativeai as genai
from pydantic import BaseModel
from fastapi import HTTPException

# Load environment variables from .env file
load_dotenv()

# Configure the API key
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Create the model
generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 40,
  "max_output_tokens": 8192,
  "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
  model_name="gemini-1.5-flash",
  generation_config=generation_config,
)



class TestRequest(BaseModel):
    content: str

class HeroTest:
    @staticmethod
    async def generate(content: str):
        try:
            # Create a more specific prompt for multiple choice questions
            prompt = f"""
            Based on the following content, create five multiple choice questions with four options, create ten fill-in-the-blank questions, and ten
            true or false questions. the multiple choice contains a, b, c, and d. Each question should have only one correct answer. 
            Make sure to make the questions challenging and engaging and the questions should be based on the content provided. Make ypour test presentable.
            Content: {content}
            """
            
            # Generate test questions
            response = model.generate_content(prompt)
            return response.text
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error generating test: {str(e)}")