import os
import sys
from fastapi import FastAPI, Body, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer
from api import HeroBot
import logging
from fastapi.responses import FileResponse

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

favicon_path = os.path.join(os.path.dirname(__file__), '..', 'static', 'favicon.ico')



print("Current Working Directory:", os.getcwd())
print("Python Path:", sys.path)

app = FastAPI()

transformer_model = SentenceTransformer('all-MiniLM-L6-v2')

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
    expose_headers=["*"],
)
#avoiding favicon error
@app.get('/favicon.ico', include_in_schema=False)
async def favicon():
    if (os.path.exists(favicon_path)):
        return FileResponse(favicon_path)
    return {"error": "favicon.ico not found"}

@app.get("/")
async def root():
    return {"message": "Welcome to PDFhero API"}

class ChatRequest(BaseModel):  # Fixed naming convention
    message: str


@app.post("/chat")
async def chat(request: ChatRequest):
    try:
        # Direct use of HeroBot function, not as class
        response = HeroBot(request.message)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/test")
async def test():
    return {"message": "API is working"}


#calling the uvicorn server to run the app
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.app:app", host="0.0.0.0", port=8000, reload=True)
