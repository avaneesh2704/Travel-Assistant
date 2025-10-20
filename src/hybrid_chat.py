
from src.connectors import openai_client, neo4j_driver
from src.retrievers import query_pinecone, fetch_graph_context
from src import config

def build_prompt(user_query, pinecone_matches, graph_facts):
    system_prompt = (
        "You are an expert travel assistant. Your task is to synthesize information from two sources to create a helpful travel recommendation. Follow these steps:\n"
        "1.  **Identify Key Entities:** Look at the 'Semantic Matches' to understand the primary locations, activities, or themes the user is interested in.\n"
        "2.  **Discover Relationships:** Examine the 'Knowledge Graph Facts' to see how these entities connect.\n"
        "3.  **Construct the Itinerary:** Based on your analysis, build a coherent and actionable response."
    )
    vec_context = "\n".join([f"- {m['metadata'].get('name', m['id'])}" for m in pinecone_matches])
    graph_context = "\n".join([f"- ({f.get('source_name')}) is [{f.get('rel_type')}] ({f.get('target_name')})" for f in graph_facts if f.get('rel_type')])
    user_prompt = f"User query: '{user_query}'\n\n### Semantic Matches:\n{vec_context}\n\n### Knowledge Graph Facts:\n{graph_context}\n\nAnswer:"
    
    return [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ]

def main():
    print("Hybrid travel assistant (CLI). Type 'exit' to quit.")
    while True:
        query = input("\nEnter your travel question: ").strip()
        if not query or query.lower() in ("exit","quit"):
            neo4j_driver.close()
            break

        matches = query_pinecone(query)
        match_ids = [m["id"] for m in matches]
        graph_facts = fetch_graph_context(match_ids)
        prompt = build_prompt(query, matches, graph_facts)
        
        response = openai_client.chat.completions.create(
            model=config.CHAT_MODEL, messages=prompt, max_tokens=600, temperature=0.3
        )
        print("\n=== Assistant Answer ===\n")
        print(response.choices[0].message.content)
        print("\n======================\n")

if __name__ == "__main__":
    main()