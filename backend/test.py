#ai feature that will bring the user the questions that they need to study for the test
#according to the content that they have uploaded
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
            Based on the following content, generate 5 multiple choice questions.
            For each question, provide 4 options (A, B, C, D) and indicate the correct answer.
            Format each question like this:

            Question 1: [Question text]
            A) [Option A]
            B) [Option B]
            C) [Option C]
            D) [Option D]
            Correct Answer: [A/B/C/D]

            Content: {content}
            """
            
            # Generate test questions
            response = model.generate_content(prompt)
            return response.text
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error generating test: {str(e)}")