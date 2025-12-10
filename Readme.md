Here’s a professional, clean README.md you can copy-paste directly into your GitHub repo. It’s beginner-friendly but looks impressive to recruiters or anyone checking your profile.markdown

# AWS Bedrock + Local Vector Database (RAG) Project

Personal knowledge base powered by **Amazon Bedrock** embeddings and **ChromaDB** — a fully working Retrieval-Augmented Generation (RAG) system that runs locally.

## Features
- Generate high-quality embeddings using **Amazon Titan Embeddings v2**
- Store text + vectors permanently in a local vector database (`chroma_db/`)
- Semantic search: ask questions in natural language → get the most relevant saved texts
- 100% local storage (SQLite + vector files)
- Works offline after documents are added
- Easy to extend into a personal AI assistant

## Project Structure

bedrock-rag/
├── add_to_db.py          → Add any text to your vector database
├── search_db.py          → Search your personal knowledge base
├── text_to_vector.py     → Simple script to test Titan embeddings
├── essay_writer.py       → Bonus: 8th-grade essay generator using Claude 3.5 Haiku
├── chroma_db/            → Automatically created: your vector database
└── README.md             → This file

## Prerequisites
- Python 3.9+
- AWS account with Bedrock access enabled in `us-east-1`
- IAM user/role with `bedrock:InvokeModel` permission
- Model access granted for:
  - `amazon.titan-embed-text-v2:0`
  - `anthropic.claude-3-5-haiku-20241022-v1:0` (optional)
  - `us.anthropic.claude-3-5-sonnet-20241022-v2:0` (optional)

## Setup

1. **Clone and enter the project**
   ```bash
   git clone https://github.com/vvitsolutions/bedrock-project.git
   cd bedrock-rag

Create virtual environmentbash

python -m venv bedrock
source bedrock/bin/activate    # Linux/Mac
# or
.\bedrock\Scripts\activate     # Windows PowerShell

Install dependenciesbash

pip install boto3 chromadb

Configure AWS credentialsbash

aws configure

Enter your Access Key, Secret Key, region: us-east-1

Usage1. Add knowledge to your databasebash

python add_to_db.py --text "My name is Ravi Kumar Boppudi"
python add_to_db.py --text "I am learning AWS Bedrock and RAG in 2025"
python add_to_db.py --text "I live in Hyderabad and love biryani"

2. Search your personal knowledge basebash

python search_db.py --query "Who is Ravi?"
python search_db.py --query "Where does Ravi live?" --n 2

Example output:

Searching for: 'Who is Ravi?'

Found 3 matches:

1. [Similarity: 0.9142]
   My name is Ravi Kumar Boppudi

2. [Similarity: 0.8721]
   I am learning AWS Bedrock and RAG in 2025

3. Generate essays with Claude 3.5 Haikubash

python essay_writer.py
# → Enter topic and length when prompted

Cost NotesAdding documents: ~$0.0001 per 100 tokens (very cheap)
Searching: one embedding call per query (still very cheap)
Future plan: switch to free local models (sentence-transformers) for $0 cost

Future IdeasBuild a chatbot that answers from everything you've ever added
Load PDFs/notes automatically
Web interface with Streamlit/Gradio
Switch to fully offline embeddings

AuthorRavi Kumar Boppudi
Learning AWS Bedrock, LangChain, and building AI applications in 2025 Star this repo if you found it helpful!


# Ravi's Personal AI Assistant 🧠 (AWS Bedrock + ChromaDB RAG)

A **fully working Retrieval-Augmented Generation (RAG)** system that knows everything about me — built with **AWS Bedrock**, **Titan Embeddings v2**, **Claude 3.5 Haiku**, and **ChromaDB**.

This is not a demo. This is **my real personal AI memory** that I use daily.

## Live Demo (It actually works!)

```bash
python chatbot.py

