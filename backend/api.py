import os
import logging
from google import generativeai as genai
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
from fastapi import FastAPI
from typing import Dict, Any

load_dotenv()  # Load environment variables from .env file

# Configure generative AI
import os
import google.generativeai as genai

# Make sure your API key is set in your environment variables
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

# Example function to vectorize response (if needed)
def vectorize_response(response_list):
    transformer_model = SentenceTransformer('all-MiniLM-L6-v2')
    input_vectors = transformer_model.encode(response_list)
    return input_vectors



#logic for ai chatbot
def HeroBot(message: str):
    try:
        # Add message to the conversation
        conversation = [
            "\"input\": \"System Instructions\",\n  \"output\": \"I am PDFHero, your academic AI assistant. I specialize in helping students learn effectively by:\n  - Analyzing academic documents with precision and clarity\n  - Providing explanations in a supportive, encouraging tone\n  - Using academic language while remaining accessible\n  - Offering comprehensive assistance backed by both document content and reliable academic sources\n  - Always maintaining academic integrity\n\nWhen responding, I will:\n1. Acknowledge your uploads/requests clearly\n2. Provide structured, organized responses\n3. Ask clarifying questions when needed\n4. Offer options for different learning styles\n5. Maintain a professional yet friendly demeanor\"",
            f"input: {message}",
            "output: "
        ]
        
        # Generate response
        response = model.generate_content(conversation)
        return response.text
    except Exception as e:
        return str(e)
    

# Run the chatbot

