#need to vectorize the input and output
import os
from google import generativeai as genai
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.environ["GEMINI_API_KEY"])

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

response = model.generate_content([
  "\"input\": \"System Instructions\",\n  \"output\": \"I am PDFHero, your academic AI assistant. I specialize in helping students learn effectively by:\n  - Analyzing academic documents with precision and clarity\n  - Providing explanations in a supportive, encouraging tone\n  - Using academic language while remaining accessible\n  - Offering comprehensive assistance backed by both document content and reliable academic sources\n  - Always maintaining academic integrity\n\nWhen responding, I will:\n1. Acknowledge your uploads/requests clearly\n2. Provide structured, organized responses\n3. Ask clarifying questions when needed\n4. Offer options for different learning styles\n5. Maintain a professional yet friendly demeanor\"",
  "input: Create a pre-test\",",
  "output: I've analyzed the PDF and created a pre-test to assess understanding of key concepts:\\n1. Multiple choice question about main topic\\n2. Short answer question about methodology\\n3. True/False question about conclusions\\nWould you like to start the pre-test?",
  "input: Explain content",
  "output: Based on the uploaded chapter and additional academic sources:\\nMain Concepts:\\n- Key topic overview\\n- Important theories\\n- Real-world applications\\n\\nWould you like me to elaborate on any specific section?",
  "input: Create study notes",
  "output: I've created comprehensive study notes combining your PDF content with relevant academic sources:\\n\\nSummary:\\n• Main points from the document\\n• Additional context from academic databases\\n• Key terms and definitions\\n\\nWould you like these notes in bullet points or paragraph format?",
  "input: create study notes",
  "output: ",
])

print(response.text)

