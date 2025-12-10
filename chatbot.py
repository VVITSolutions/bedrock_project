# chatbot.py - Your Personal RAG Assistant
from rich.console import Console
from rich.markdown import Markdown
import boto3
import json
import chromadb

console = Console()
client = boto3.client('bedrock-runtime', region_name='us-east-1')
chroma_client = chromadb.PersistentClient(path="./chroma_db")
collection = chroma_client.get_or_create_collection(name="ravi_memory")

# === Get embedding for query ===
def get_embedding(text):
    body = json.dumps({"inputText": text})
    response = client.invoke_model(
        body=body,
        modelId="amazon.titan-embed-text-v2:0",
        accept="application/json",
        contentType="application/json"
    )
    return json.loads(response["body"].read())["embedding"]

# === Retrieve relevant memories ===
def retrieve_memories(query, top_k=5):
    if collection.count() == 0:
        return "No memories yet. Teach me something first!"
    results = collection.query(
        query_embeddings=[get_embedding(query)],
        n_results=top_k,
        include=["documents", "distances"]
    )
    memories = results["documents"][0]
    return "\n".join([f"• {m}" for m in memories])

# === Generate answer using Claude 3.5 Haiku ===
def generate_answer(question, context):
    prompt = f"""You are Ravi's personal AI assistant. You know everything about him from these facts:

{context}

Rules:
- Answer naturally and conversationally
- NEVER make anything up
- If you don't know, say "I don't have that in my memory yet"
- Keep it short and friendly

Question: {question}
Answer:"""

    body = json.dumps({
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 512,
        "temperature": 0.7,
        "messages": [{"role": "user", "content": [{"type": "text", "text": prompt}]}]
    })

    response = client.invoke_model(
        body=body,
        modelId="us.anthropic.claude-3-5-haiku-20241022-v1:0",
        accept="application/json",
        contentType="application/json"
    )
    return json.loads(response["body"].read())["content"][0]["text"]

# === Main chat loop ===
console.print(Markdown("# Ravi's Personal AI Assistant 🧠"))
console.print("Type 'quit' to exit | Type '/add <fact>' to teach me something new\n")

# First, add your core identity facts
initial_facts = [
    "My name is Ravi Kumar Boppudi",
    "I am of Indian origin and currently live in the UK",
    "I follow a strict carnivore diet",
    "My favorite meal is steak and eggs",
    "I am learning AWS Bedrock, RAG, and building AI systems in 2025"
]

for fact in initial_facts:
    if collection.count() < 5:  # only add once
        embedding = get_embedding(fact)
        collection.add(embeddings=[embedding], documents=[fact], ids=[str(collection.count() + 1)])

while True:
    user_input = console.input("[bold cyan]You:[/bold cyan] ")
    
    if user_input.lower() in ["quit", "exit", "bye"]:
        console.print("See you later, Ravi! 🥩")
        break
        
    if user_input.lower().startswith("/add "):
        fact = user_input[5:].strip()
        embedding = get_embedding(fact)
        collection.add(embeddings=[embedding], documents=[fact], ids=[str(collection.count() + 1)])
        console.print(f"[green]Learned:[/green] {fact}")
        continue

    console.print("[dim]Thinking...[/dim]")
    context = retrieve_memories(user_input)
    answer = generate_answer(user_input, context)
    console.print(Markdown(f"**Ravi's AI:** {answer}"))