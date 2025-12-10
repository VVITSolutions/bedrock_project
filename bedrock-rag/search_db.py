# search_db.py  ← FIXED VERSION
import boto3
import json
import chromadb
import argparse

# === Bedrock client ===
client = boto3.client('bedrock-runtime', region_name='us-east-1')

# === ChromaDB setup ===
chroma_client = chromadb.PersistentClient(path="./chroma_db")
collection = chroma_client.get_or_create_collection(name="my_documents")

# === Embedding function (fixed: added missing accept/contentType) ===
def text_to_embedding(text, model_id="amazon.titan-embed-text-v2:0"):
    body = json.dumps({"inputText": text})
    
    response = client.invoke_model(
        body=body,
        modelId=model_id,
        accept="application/json",      # ← these were missing!
        contentType="application/json"  # ← these were missing!
    )
    response_body = json.loads(response["body"].read())
    return response_body["embedding"]

# === Command line args ===
parser = argparse.ArgumentParser(description="Search your local vector database")
parser.add_argument("--query", type=str, required=True, help="Search query")
parser.add_argument("--n", type=int, default=3, help="Number of results (default: 3)")
args = parser.parse_args()

# === Run the search ===
print(f"Searching for: '{args.query}'\n")
query_embedding = text_to_embedding(args.query)

results = collection.query(
    query_embeddings=[query_embedding],
    n_results=args.n,
    include=["documents", "distances"]
)

# === Pretty print results ===
print(f"Found {len(results['documents'][0])} matches:\n")
for i, (doc, dist) in enumerate(zip(results["documents"][0], results["distances"][0])):
    similarity = 1 - dist  # cosine distance → similarity
    print(f"{i+1}. [Similarity: {similarity:.4f}]")
    print(f"   {doc}\n")