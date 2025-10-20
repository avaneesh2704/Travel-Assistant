
import os
from dotenv import load_dotenv

load_dotenv()

# API Keys and Connection URIs
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
NEO4J_URI = os.getenv("NEO4J_URI")
NEO4J_USER = os.getenv("NEO4J_USER")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")

# Pinecone Configuration
PINECONE_INDEX_NAME = "vietnam-travel"
# Critical Change: OpenAI's embedding model uses a dimension of 1536
PINECONE_VECTOR_DIM = 1536

# Model Configuration
EMBED_MODEL = "text-embedding-3-small"
CHAT_MODEL = "gpt-4o-mini"