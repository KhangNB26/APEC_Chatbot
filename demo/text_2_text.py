from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM
from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
import os
from utils.time_logger import timeit
import torch
from dotenv import load_dotenv
import warnings
warnings.filterwarnings("ignore")

# Load environment variables
load_dotenv()

# Get QDRANT API key and host from environment variables
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
QDRANT_HOST = os.getenv("QDRANT_HOST")

# Check if GPU is available and set device accordingly
if torch.cuda.is_available():
    device = 0  # Use GPU
    print("Using GPU for text generation.")
else:
    device = -1 # Use CPU
    print("Using CPU for text generation.")

# Create pipeline for text generation using HuggingFace token
tokenizer = AutoTokenizer.from_pretrained("TinyLlama/TinyLlama-1.1B-Chat-v1.0")
model = AutoModelForCausalLM.from_pretrained("TinyLlama/TinyLlama-1.1B-Chat-v1.0")
text_gen_pipeline = pipeline("text-generation", model=model, tokenizer=tokenizer, device=device)

# Initialize Qdrant client for Docker 
qdrant_client = QdrantClient(
    api_key=QDRANT_API_KEY,  # Qdrant API key
    url=QDRANT_HOST,  # Qdrant server URL 
    https=True,  # Use HTTPS
)

# Collection name for Qdrant
COLLECTION_NAME = "apec_docs"

# Initialize SentenceTransformer model
embedding_model = SentenceTransformer("intfloat/multilingual-e5-large-instruct")

# Qdrant search function to retrieve context based on a question
@timeit("LLM: Qdrant Search")
def get_context(question, k=5):
    """
    Retrieve context from Qdrant based on the question.
    
    Args:
        question (str): The question to search for.
        k (int): Number of nearest neighbors to retrieve.
        
    Returns:
        list: List of contexts retrieved from Qdrant.
    """
    embedding = embedding_model.encode(f"Documents for retrieving: {question}").tolist()
    response = qdrant_client.search(
        collection_name=COLLECTION_NAME,
        query_vector=embedding,
        limit=k,
        with_payload=True
    )
    context = "\n".join([pt.payload.get("text", "") for pt in response])
    return context

# Function to generate text using the LLM
@timeit("LLM: Generate Answer")
def generate_answer(question):
    """
    Generate an answer to the question using the LLM.
    
    Args:
        question (str): The question to answer.
        
    Returns:
        str: Generated answer from the LLM.
    """
    context = get_context(question)
    prompt = (
    "You are an expert assistant. "
    "Answer the question **only based on the Context below**. "
    "If you don't know, reply: 'I don't have enough information from the context.'\n\n"
    f"Context:\n{context}\n\nQuestion: {question}\nAnswer:"
)
    
    # Adjust based on model's max input length
    max_prompt_length = 2048
    if len(prompt) > max_prompt_length:
        prompt = prompt[:max_prompt_length]

    response = text_gen_pipeline(prompt, max_new_tokens=128, do_sample=False, temperature=0.5)
    answer = response[0]['generated_text'].strip()
    if "Answer:" in answer:
        answer = answer.split("Answer:")[-1].strip()
    print("🤖 Chatbot Answer:\n", answer)
    return answer
