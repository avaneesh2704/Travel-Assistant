
from src.connectors import openai_client, pinecone_index, neo4j_driver
from src import config

embedding_cache = {}

def get_embedding(text: str):
    """Generates an embedding using OpenAI."""
    if text in embedding_cache:
        return embedding_cache[text]
    
    response = openai_client.embeddings.create(model=config.EMBED_MODEL, input=[text])
    embedding = response.data[0].embedding
    embedding_cache[text] = embedding
    return embedding

def query_pinecone(query_text: str, top_k=5):
    query_embedding = get_embedding(query_text)
    return pinecone_index.query(
        vector=query_embedding, top_k=top_k, include_metadata=True
    )["matches"]

def fetch_graph_context(node_ids: list[str]):
    
    cypher_query = """
    UNWIND $node_ids AS nid
    MATCH (n:Entity {id: nid})
    CALL {
        WITH n
        MATCH (n)-[r]-(m) RETURN n, r, m LIMIT 10
    }
    CALL {
        WITH n
        MATCH (n)-[]-(m)-[r2]-(p) WHERE id(n) < id(p) RETURN n, r2 AS r, p AS m LIMIT 5
    }
    RETURN n.name AS source_name, type(r) AS rel_type, m.name AS target_name
    """
    with neo4j_driver.session() as session:
        result = session.run(cypher_query, node_ids=node_ids)
        return [record.data() for record in result]