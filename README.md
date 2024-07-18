# FinTech RAG System

## Description

This project implements a cloud-native Retrieval-Augmented Generation (RAG) system tailored for FinTech applications. It uses OpenAI's GPT-4 for text generation, Pinecone for vector storage and similarity search, and Flask for serving the API.

The system can process financial documents, generate embeddings, store them in a vector database, and provide AI-powered responses to queries based on the stored information.

## Features

- Document processing and chunking
- Embedding generation using OpenAI's API
- Vector storage and retrieval using Pinecone
- Query processing with context-aware responses
- RESTful API for adding documents and querying the system

## Prerequisites

- Docker
- OpenAI API key
- Pinecone API key

## Setup

1. Clone this repository:
   ```
   git clone https://github.com/kidsil/fintech-rag-system.git
   cd fintech-rag-system
   ```

2. Create a `.env` file in the project root and add your API keys:
   ```
   OPENAI_API_KEY=your_openai_api_key_here
   PINECONE_API_KEY=your_pinecone_api_key_here
   ```

3. Build the Docker image:
   ```
   docker build -t fintech-rag .
   ```

## Running the Application

Run the Docker container with the following command:

```
docker run -it --name fintech-rag --rm --network host -v ${PWD}:/app -e PINECONE_API_KEY=your_pinecone_api_key -e OPENAI_API_KEY=your_openai_api_key fintech-rag
```

Replace `your_pinecone_api_key` and `your_openai_api_key` with your actual API keys.

## Usage

Once the application is running, you can interact with it using HTTP requests. Here are some example curl commands:

### Adding a Document

```bash
curl -X POST http://localhost:8000/add_document \
     -H "Content-Type: application/json" \
     -d '{
       "document": "The Securities and Exchange Commission (SEC) has proposed new regulations for cryptocurrency exchanges. These regulations aim to increase transparency and protect investors from fraud and market manipulation. Key points include mandatory registration of exchanges, implementation of robust cybersecurity measures, and regular reporting of trading activities."
     }'

# Expected response:
# {"message":"Document added successfully"}
```

### Querying the System

```bash
curl -X POST http://localhost:8000/query \
     -H "Content-Type: application/json" \
     -d '{
       "query": "What are the recent trends in cryptocurrency regulations?"
     }'

# Expected response:
# {"answer":"The recent trends in cryptocurrency regulations proposed by the Securities and Exchange Commission (SEC) include mandatory registration of exchanges, robust implementation of cybersecurity measures, and the regular reporting of trading activities. These regulations are designed to increase transparency and safeguard investors from potential fraud and market manipulation."}
```

## Project Structure

- `app.py`: Main application file containing the RAG system implementation and Flask API
- `requirements.txt`: List of Python dependencies
- `Dockerfile`: Instructions for building the Docker image

## Notes

- The system uses the `text-embedding-3-small` model for generating embeddings and `gpt-4` for answering queries. Ensure your OpenAI account has access to these models.
- The Pinecone index is created in the `us-east-1` region. Modify this in the code if you need a different region.
- The application runs on port 8000 by default. Ensure this port is available or modify the port in both the `app.py` and `Dockerfile` if needed.
