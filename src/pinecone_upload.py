
import json
from tqdm import tqdm
from src.connectors import openai_client, pinecone_index
from src import config

DATA_FILE = "data/vietnam_travel_dataset.json"
BATCH_SIZE = 32

def get_embeddings_batch(texts: list[str]):
    response = openai_client.embeddings.create(model=config.EMBED_MODEL, input=texts)
    return [item.embedding for item in response.data]

def chunked(iterable, n):
    for i in range(0, len(iterable), n):
        yield iterable[i:i + n]

def main():
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        nodes = json.load(f)
    items = []
    for node in nodes:
        semantic_text = node.get("semantic_text") or (node.get("description") or "")[:1000]
        if not semantic_text.strip(): continue
        meta = {k: v for k, v in node.items() if k not in ["connections", "semantic_text"] and isinstance(v, (str, int, float, bool, list))}
        items.append((node["id"], semantic_text, meta))

    print(f"Preparing to upsert {len(items)} items to Pinecone...")

    for batch in tqdm(list(chunked(items, BATCH_SIZE)), desc="Uploading batches"):
        ids, texts, metas = zip(*batch)
        embeddings = get_embeddings_batch(list(texts))
        vectors = [{"id": ids[i], "values": embedding, "metadata": metas[i]} for i, embedding in enumerate(embeddings)]
        pinecone_index.upsert(vectors=vectors)
    
    print("Pinecone upload complete.")
    print(pinecone_index.describe_index_stats())

if __name__ == "__main__":
    main()