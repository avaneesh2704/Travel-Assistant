
from pyvis.network import Network
from src.connectors import neo4j_driver

def fetch_subgraph(tx, limit=200):
    """Fetches nodes and relationships as graph objects."""
    q = "MATCH (a:Entity)-[r]->(b:Entity) RETURN a, b, r LIMIT $limit"
    # Return the list of records directly
    return list(tx.run(q, limit=limit))

def main(output_html="neo4j_viz.html"):
    net = Network(height="900px", width="100%", notebook=False, directed=True)
    with neo4j_driver.session() as session:
        # Use execute_read to fix the deprecation warning
        results = session.execute_read(fetch_subgraph)
        
        for record in results:
            a_node = record["a"]
            b_node = record["b"]
            r_rel = record["r"]
            
            # Now a_node and b_node are actual Node objects
            # and we can safely access their .element_id attribute
            net.add_node(a_node.element_id, label=a_node.get('name', 'Unknown'), title=str(dict(a_node.items())))
            net.add_node(b_node.element_id, label=b_node.get('name', 'Unknown'), title=str(dict(b_node.items())))
            net.add_edge(a_node.element_id, b_node.element_id, label=r_rel.type)
            
    net.show_buttons(filter_=['physics'])
    net.save_graph(output_html)
    print(f"Graph visualization saved to {output_html}")
    neo4j_driver.close()

if __name__ == "__main__":
    main()