from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
import numpy as np

load_dotenv()


# Initialize the transformer model once
transformer_model = SentenceTransformer('all-MiniLM-L6-v2')

# Create a function to process conversations
def vectorize_conversation(conversations):
    # Separate inputs and outputs
    inputs = []
    outputs = []
    
    for conv in conversations:
        if isinstance(conv, str) and "input:" in conv.lower():
            inputs.append(conv.split("input:")[1].strip())
        elif isinstance(conv, str) and "output:" in conv.lower():
            outputs.append(conv.split("output:")[1].strip())
    
    # Batch encode inputs and outputs
    input_vectors = transformer_model.encode(inputs, batch_size=32, show_progress_bar=False)
    output_vectors = transformer_model.encode(outputs, batch_size=32, show_progress_bar=False)
    
    return input_vectors, output_vectors

# Usage
response = []  # Example response list
response_list = [item.strip() for item in response]  # Clean the response items
input_vectors, output_vectors = vectorize_conversation(response_list)



