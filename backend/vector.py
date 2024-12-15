from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
from typing import List
import numpy as np

load_dotenv()

model = SentenceTransformer('paraphrase-MiniLM-L6-v2')

def vectorize_text(text: List[str]) -> np.ndarray:
    sentence_vector = model.encode(text)
    return sentence_vector