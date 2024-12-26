# app.py
import os
from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer
from api import HeroBot
import logging
from PDFfilereader import PDFReader, split_text_into_chunks

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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)