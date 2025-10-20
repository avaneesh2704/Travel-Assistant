
import json
from tqdm import tqdm
from src.connectors import neo4j_driver

DATA_FILE = "data/vietnam_travel_dataset.json"

def create_constraints(tx):
    tx.run("CREATE CONSTRAINT IF NOT EXISTS FOR (n:Entity) REQUIRE n.id IS UNIQUE")

def upsert_node(tx, node):
    labels = [node.get("type", "Unknown"), "Entity"]
    label_cypher = ":" + ":".join(labels)
    props = {k: v for k, v in node.items() if k not in ("connections",)}
    tx.run(f"MERGE (n{label_cypher} {{id: $id}}) SET n += $props", id=node["id"], props=props)

def create_relationship(tx, source_id, rel):
    rel_type = rel.get("relation", "RELATED_TO")
    target_id = rel.get("target")
    if not target_id: return
    cypher = "MATCH (a:Entity {id: $source_id}), (b:Entity {id: $target_id}) MERGE (a)-[r:%s]->(b)" % rel_type
    tx.run(cypher, source_id=source_id, target_id=target_id)

def main():
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        nodes = json.load(f)
    with neo4j_driver.session() as session:
        session.execute_write(create_constraints)
        for node in tqdm(nodes, desc="Upserting nodes"):
            session.execute_write(upsert_node, node)
        for node in tqdm(nodes, desc="Creating relationships"):
            for rel in node.get("connections", []):
                session.execute_write(create_relationship, node["id"], rel)
    print("Neo4j data loading complete.")
    neo4j_driver.close()

if __name__ == "__main__":
    main()