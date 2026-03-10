"""
Configuration module — loads environment variables and defines app-wide settings.
"""

import os
from dotenv import load_dotenv
import json 

load_dotenv()

# ── API Keys ──────────────────────────────────────────────────────────────────
PINECONE_API_KEY: str = os.getenv("PINECONE_API_KEY", "")
OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")

# ── Pinecone Settings ────────────────────────────────────────────────────────
PINECONE_INDEX_NAME: str = "rag-classic"
PINECONE_NAMESPACE: str = "documents"
PINECONE_CLOUD: str = "aws"
PINECONE_REGION: str = "us-east-1"
PINECONE_EMBED_MODEL: str = "multilingual-e5-large"  # Pinecone hosted embedding
PINECONE_RERANK_MODEL: str = "bge-reranker-v2-m3"    # Pinecone hosted reranker

# ── Chunking Settings ────────────────────────────────────────────────────────
CHUNK_SIZE: int = 512          # characters per chunk
CHUNK_OVERLAP: int = 64        # overlap between chunks

# ── Retrieval Settings ────────────────────────────────────────────────────────
TOP_K: int = 10                # candidates to fetch from vector search
RERANK_TOP_N: int = 5          # results to keep after reranking

# ── Generation Settings ──────────────────────────────────────────────────────
OPENAI_MODEL: str = "gpt-4o-mini"
MAX_TOKENS: int = 1024
TEMPERATURE: float = 0.2


#azure ai searhc vairables 


file_path=r"D:\Machine_learning\Deeplearning\aiml_tutorials\config_json.txt"
config_json = json.load(open(file_path))



AZURE_SEARCH_ENDPOINT=config_json["AZURE_SEARCH_ENDPOINT"]
AZURE_SEARCH_API_KEY=config_json["AZURE_SEARCH_API_KEY"]
AZURE_SEARCH_INDEX=config_json["AZURE_SEARCH_INDEX"]
AZURE_OPENAI_ENDPOINT=config_json["AZURE_OPENAI_ENDPOINT"]
AZURE_OPENAI_API_KEY=config_json["AZURE_OPENAI_API_KEY"]
AZURE_OPENAI_DEPLOYMENT_GPT_ID=config_json["AZURE_OPENAI_DEPLOYMENT_GPT_ID"]
AZURE_OPENAI_EMBEDDING_DEPLOYMENT_ID=config_json["AZURE_OPENAI_EMBEDDING_DEPLOYMENT_ID"]
api_version = "2024-12-01-preview"
AZURE_STORAGE_CONNECTION=config_json["AZURE_STORAGE_CONNECTION"]
AccountKey="AccountKey"
AI_FOUNDRY_AI_SERVICES_URL=config_json["AI_FOUNDRY_AI_SERVICES_URL"]
AI_FOUNDRY_KEY=config_json["AI_FOUNDRY_KEY"]
FOUNDRY_EMBEDDING_DEPLOYMENT_NAME=config_json["FOUNDRY_EMBEDDING_DEPLOYMENT_NAME"]
FOUNDRY_EMBEDDING_MODEL_NAME=config_json["FOUNDRY_EMBEDDING_MODEL_NAME"]
gpt4modelname= config_json["gpt4modelname"]
gpt4deployment=config_json["gpt4deployment"]
ocr_endpoint=config_json["ocr_endpoint"]
ocr_endpoint_key=config_json["ocr_endpoint_key"]

if __name__ == "__main__":
    print("=== Config Test ===")
    print(f"PINECONE_API_KEY : {'✅ set' if PINECONE_API_KEY else '❌ missing'}")
    print(f"OPENAI_API_KEY   : {'✅ set' if OPENAI_API_KEY else '❌ missing'}")
    print(f"Index name       : {PINECONE_INDEX_NAME}")
    print(f"Embed model      : {PINECONE_EMBED_MODEL}")
    print(f"Rerank model     : {PINECONE_RERANK_MODEL}")
    print(f"Chunk size       : {CHUNK_SIZE}, overlap: {CHUNK_OVERLAP}")
    print(f"LLM model        : {OPENAI_MODEL}")
    print("✅ Config loaded successfully!")
