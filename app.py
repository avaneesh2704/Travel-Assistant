
import streamlit as st
from src import config
from src.retrievers import query_pinecone, fetch_graph_context
from src.connectors import openai_client

def get_rag_response(query, chat_history):
    pinecone_matches = query_pinecone(query)
    node_ids = [m["id"] for m in pinecone_matches]
    graph_facts = fetch_graph_context(node_ids)

    system_prompt = (
        "You are an expert travel assistant. Your task is to synthesize information from two sources to create a helpful travel recommendation. Follow these steps:\n"
        "1.  **Identify Key Entities:** Look at the 'Semantic Matches' to understand the primary locations, activities, or themes the user is interested in.\n"
        "2.  **Discover Relationships:** Examine the 'Knowledge Graph Facts' to see how these entities connect.\n"
        "3.  **Consider History:** Review the 'Previous Conversation' to understand the context and answer follow-up questions.\n"
        "4.  **Construct the Itinerary:** Based on your analysis, build a coherent and actionable response."
    )
    
    history_str = "\n".join([f"{msg['role']}: {msg['content']}" for msg in chat_history])
    vec_context = "\n".join([f"- {m['metadata'].get('name', m['id'])}" for m in pinecone_matches])
    graph_context = "\n".join([f"- ({f.get('source_name')}) is [{f.get('rel_type')}] ({f.get('target_name')})" for f in graph_facts if f.get('rel_type')])
    user_prompt = f"### Previous Conversation:\n{history_str}\n\n### Current User Query: '{query}'\n\n### Context:\n{vec_context}\n{graph_context}\n\nAnswer:"
    
    messages = [{"role": "system", "content": system_prompt}, {"role": "user", "content": user_prompt}]

    response = openai_client.chat.completions.create(
        model=config.CHAT_MODEL, messages=messages, max_tokens=800, temperature=0.4
    )
    return response.choices[0].message.content

# --- Streamlit App ---
st.set_page_config(page_title="AI Hybrid Travel Assistant")
st.title("AI Hybrid Travel Assistant ")

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "How can I help you plan your trip to Vietnam?"}]

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ask about attractions, itineraries, or activities..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = get_rag_response(prompt, st.session_state.messages)
            st.markdown(response)
    st.session_state.messages.append({"role": "assistant", "content": response})