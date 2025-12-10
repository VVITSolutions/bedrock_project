# add_to_db.py
import boto3
import json
import chromadb
from chromadb.utils import embedding_functions
import argparse
import os

# Initialize Bedrock client
client = boto3.client('bedrock-runtime', region_name='us-east-1')

# Initialize ChromaDB — it saves everything in ./chroma_db folder automatically
chroma_client = chromadb.PersistentClient(path="./chroma_db")
collection = chroma_client.get_or_create_collection(name="my_documents")

def text_to_embedding(text, model_id="amazon.titan-embed-text-v2:0"):
    body = json.dumps({"inputText": text})
    response = client.invoke_model(
        body=body,
        modelId=model_id,
        accept="application/json",
        contentType="application/json"
    )
    response_body = json.loads(response["body"].read())
    return response_body["embedding"]

# Command line arguments
parser = argparse.ArgumentParser(description="Add text to local vector database")
parser.add_argument("--text", type=str, required=True, help="Text to store")
parser.add_argument("--id", type=str, help="Optional custom ID (default: auto number)")
args = parser.parse_args()

# Generate embedding
print("Generating embedding with Titan Embeddings v2...")
embedding = text_to_embedding(args.text)

# Auto-generate ID if not provided
doc_id = args.id or str(collection.count() + 1)

# Save to ChromaDB
collection.add(
    embeddings=[embedding],
    documents=[args.text],
    ids=[doc_id]
)

print(f"Successfully added to database!")
print(f"   ID: {doc_id}")
print(f"   Text: {args.text[:80]}{'...' if len(args.text)>80 else ''}")
print(f"   Vector length: {len(embedding)}")
print(f"   Total documents in DB: {collection.count()}")

#usage example: 
# python add_to_db.py --text "My name is Ravi"
# python add_to_db.py --text "I live in UK"
# python add_to_db.py --text "I am learning AWS Bedrock and LangChain in 2025"
# python add_to_db.py --text "My favorite food is steak and eggs"