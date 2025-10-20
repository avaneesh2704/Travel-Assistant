
from openai import OpenAI
from pinecone import Pinecone, ServerlessSpec
from neo4j import GraphDatabase
from src import config

def get_openai_client():
    return OpenAI(api_key=config.OPENAI_API_KEY)

def get_pinecone_index():
    pc = Pinecone(api_key=config.PINECONE_API_KEY)
    index_name = config.PINECONE_INDEX_NAME
    if index_name not in [index.name for index in pc.list_indexes()]:
        print(f"Creating Pinecone index with dimension {config.PINECONE_VECTOR_DIM}")
        pc.create_index(
            name=index_name,
            dimension=config.PINECONE_VECTOR_DIM,
            metric="cosine",
            spec=ServerlessSpec(cloud="aws", region="us-east-1")
        )
    return pc.Index(index_name)

def get_neo4j_driver():
    return GraphDatabase.driver(
        config.NEO4J_URI, auth=(config.NEO4J_USER, config.NEO4J_PASSWORD)
    )

# Global clients
openai_client = get_openai_client()
pinecone_index = get_pinecone_index()
neo4j_driver = get_neo4j_driver()