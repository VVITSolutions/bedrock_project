
import boto3
import json
import chromadb
import argparse

client = boto3.client('bedrock-runtime', region_name='us-east-1')
chroma_client = chromadb.PersistentClient(path="./chroma_db")
collection = chroma_client.get_or_create_collection(name="ravi_memory")

def get_embedding(text):
    body = json.dumps({"inputText": text})
    response = client.invoke_model(
        body=body,
        modelId="amazon.titan-embed-text-v2:0",
        accept="application/json",
        contentType="application/json"
    )
    return json.loads(response["body"].read())["embedding"]

parser = argparse.ArgumentParser()
parser.add_argument("--text", type=str, required=True)
args = parser.parse_args()

embedding = get_embedding(args.text)
collection.add(
    embeddings=[embedding],
    documents=[args.text],
    ids=[str(collection.count() + 1)]
)
print(f"Added to memory: {args.text}")


#usage example: 
# python add_to_db.py --text "My name is Ravi"
# python add_to_db.py --text "I live in UK"
# python add_to_db.py --text "I am learning AWS Bedrock and LangChain in 2025"
# python add_to_db.py --text "My favorite food is steak and eggs"