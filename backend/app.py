# app.py
import os
from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer
from api import HeroBot
from test import HeroTest
import logging
from vector import vectorize_conversation
from PDFfilereader import PDFReader, split_text_into_chunks
from sklearn.metrics.pairwise import cosine_similarity

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = FastAPI()

# In-memory storage for PDF content
class PDFStorage:
    def __init__(self):
        self.current_text = ""
        self.chunks = []
        
pdf_storage = PDFStorage()
pdf_contents = {}
transformer_model = SentenceTransformer('all-MiniLM-L6-v2')

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5500", "http://127.0.0.1:5500", "http://127.0.0.1:5501"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
    expose_headers=["*"],
)

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    logger.debug(f"Received file upload request: {file.filename}")
    
    if not file.filename.lower().endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")
    
    try:
        # Read the file content
        content = await file.read()
        
        # Create PDFReader instance with the content
        pdf_reader = PDFReader(content)
        text = pdf_reader.PDFread()
        
        # Store the extracted text and chunks
        pdf_storage.current_text = text
        pdf_storage.chunks = split_text_into_chunks(text)
        
        logger.debug(f"Successfully processed PDF: {file.filename}")
        logger.debug(f"Extracted text length: {len(text)}")
        logger.debug(f"Number of chunks: {len(pdf_storage.chunks)}")
        
        return {
            "info": f"File {file.filename} uploaded and processed successfully",
            "chunks": len(pdf_storage.chunks),
            "text_length": len(text)
        }
            
    except Exception as e:
        logger.error(f"Error processing PDF: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error processing PDF: {str(e)}")

class ChatRequest(BaseModel):
    message: str

@app.post("/chat")
async def chat_with_context(request: ChatRequest):
            try:
                if not pdf_storage.current_text:
                    return {"response": "Please upload a PDF file first."}
                    
                logger.debug(f"Received chat request with context: {request.message}")
                logger.debug(f"Current PDF text length: {len(pdf_storage.current_text)}")
                
                # Use chunks instead of full text for better context management
                relevant_context = "\n".join(pdf_storage.chunks[:3])  # Using first few chunks as example
                
                # Create a more focused prompt combining context and question
                context = f"Using this document content as reference:\n\n{relevant_context}\n\nUser Question: {request.message}"
                
                response = HeroBot(context)
                return {"response": response}
                
            except Exception as e:
                logger.error(f"Error in chat-with-context endpoint: {str(e)}", exc_info=True)
                raise HTTPException(status_code=500, detail=str(e))

@app.get("/status")
async def get_status():
    return {
        "has_pdf": bool(pdf_storage.current_text),
        "chunks_count": len(pdf_storage.chunks) if pdf_storage.chunks else 0
    }

from pydantic import BaseModel

class TestRequest(BaseModel):
    content: str

@app.post("/test")
async def generate_test(request: TestRequest):
    try:
        content = request.content 
        test_questions = await HeroTest.generate(content) # Assuming HeroTest.generate expects the content directly

        # Split the response into individual questions
        questions = [q.strip() for q in test_questions.split('\n\n') if q.strip()]
        
        return {"questions": questions} 
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


class ContentResponse(BaseModel):
    content: str

@app.get("/content")
async def get_content():
    if not pdf_storage.current_text:
        raise HTTPException(status_code=404, detail="No PDF content found. Please upload a PDF first.")
    return ContentResponse(content=pdf_storage.current_text)

class AnswerRequest(BaseModel):
    test_id: str = None
    user_answer: str
    original_question: str

def generate_feedback(score: float) -> str:
    if score > 0.85:
        return "Excellent answer!"
    elif score > 0.7:
        return "Good answer, but could be more precise."
    else:
        return "Your answer needs improvement."

@app.post("/check-answer")
async def check_answer(request: AnswerRequest):
    try:
        # Vectorize the user's answer
        answer_vector = transformer_model.encode([request.user_answer])[0]
        
        # Compare with stored vectors using similarity
        similarity_score = cosine_similarity(
            [answer_vector], 
            [request.original_vectors["output"]]
        )[0][0]
        
        # Evaluate based on similarity threshold
        is_correct = similarity_score > 0.85  # Adjust threshold as needed
        
        return {
            "is_correct": is_correct,
            "similarity_score": float(similarity_score),
            "feedback": generate_feedback(similarity_score)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)