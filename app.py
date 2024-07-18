import os
import nltk
from nltk.tokenize import sent_tokenize
from openai import OpenAI
from pinecone import Pinecone, ServerlessSpec
from flask import Flask, request, jsonify

# Download NLTK data
nltk.download('punkt')

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Initialize Pinecone
pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))

# Create or connect to the Pinecone index
index_name = "fintech-documents"
if index_name not in pc.list_indexes().names():
    pc.create_index(
        name=index_name,
        dimension=1536,
        metric='cosine',
        spec=ServerlessSpec(
            cloud='aws',
            region='us-east-1'
        )
    )
index = pc.Index(index_name)

def chunk_document(doc, max_chunk_size=1000):
    sentences = sent_tokenize(doc)
    chunks = []
    current_chunk = ""
    
    for sentence in sentences:
        if len(current_chunk) + len(sentence) <= max_chunk_size:
            current_chunk += sentence + " "
        else:
            chunks.append(current_chunk.strip())
            current_chunk = sentence + " "
    
    if current_chunk:
        chunks.append(current_chunk.strip())
    
    return chunks

def generate_embedding(text):
    text = text.replace("\n", " ")
    response = client.embeddings.create(input=[text], model="text-embedding-3-small")
    return response.data[0].embedding

def process_document(document):
    chunks = chunk_document(document)
    for i, chunk in enumerate(chunks):
        embedding = generate_embedding(chunk)
        index.upsert(vectors=[(str(i), embedding, {"text": chunk})])

def process_query(query):
    query_embedding = generate_embedding(query)
    search_results = index.query(vector=query_embedding, top_k=3, include_metadata=True)
    context = " ".join([result.metadata['text'] for result in search_results.matches])
    
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a financial expert assistant. Use the following context to answer the user's question."},
            {"role": "user", "content": f"Context: {context}\n\nQuestion: {query}"}
        ]
    )
    
    return response.choices[0].message.content

# Flask app
app = Flask(__name__)

@app.route('/add_document', methods=['POST'])
def add_document():
    document = request.json['document']
    process_document(document)
    return jsonify({"message": "Document added successfully"}), 200

@app.route('/query', methods=['POST'])
def query():
    user_query = request.json['query']
    answer = process_query(user_query)
    return jsonify({"answer": answer}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
