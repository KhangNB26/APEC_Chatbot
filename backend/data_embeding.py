import json
from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct, VectorParams, Distance
import os
from dotenv import load_dotenv
import warnings
warnings.filterwarnings("ignore")

# Load environment variables
load_dotenv()

# Get QDRANT API key and host from environment variables
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
QDRANT_HOST = os.getenv("QDRANT_HOST")

# Load data
with open("APEC_Chatbot/backend/APEC.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# Prepare embedding model
model = SentenceTransformer("intfloat/multilingual-e5-large-instruct")

# Connect to Qdrant (local or cloud)
qdrant_client = QdrantClient(
    api_key=QDRANT_API_KEY,  # Qdrant API key
    url=QDRANT_HOST,  # Qdrant server URL 
    https=True,  # Use HTTPS
)

# Create collection (if needed)
qdrant_client.recreate_collection(
    collection_name="apec_docs",
    vectors_config=VectorParams(size=1024, distance=Distance.COSINE),
)

def flatten_content(content):
    if isinstance(content, str):
        return content
    elif isinstance(content, list):
        # If all elements are strings, join them
        if all(isinstance(x, str) for x in content):
            return "\n".join(content)
        # If all elements are dictionaries, format them
        elif all(isinstance(x, dict) for x in content):
            return "\n".join(
                [", ".join(f"{k}: {v}" for k, v in entry.items()) for entry in content]
            )
    return str(content)

# Convert and upload data
points = []
for idx, item in enumerate(data):
    text = flatten_content(item["content"])
    vector = model.encode(text).tolist()
    point = PointStruct(
        id=idx,
        vector=vector,
        payload={
            "section": item["section"],
            "content": text
        }
    )
    points.append(point)

# Upload points to Qdrant
qdrant_client.upsert(
    collection_name="apec_docs",
    points=points
)