# Hybrid AI Travel Assistant ✈️

This project is a sophisticated, retrieval-augmented generation (RAG) travel assistant for Vietnam. It leverages a hybrid approach, combining semantic search from a Pinecone vector database with contextual graph data from a Neo4j knowledge graph to provide intelligent, context-aware travel recommendations.

The application features a fully interactive web interface built with Streamlit and supports conversational memory for follow-up questions.

---


### **Architecture**

The system follows a three-stage process to answer user queries:

1.  **Semantic Retrieval (Pinecone):** The user's query is vectorized to find the most conceptually similar travel entities from the Pinecone index.
2.  **Graph Enrichment (Neo4j):** The top semantic matches are used to query the Neo4j database, fetching a rich 2-hop neighborhood of connected entities and relationships.
3.  **LLM Synthesis (OpenAI):** The semantic results, graph facts, and conversational history are compiled into an advanced prompt. An OpenAI model then synthesizes this information to generate a coherent response.



---
### **Key Features**

-   **Hybrid Retrieval:** Combines vector search for relevance with graph search for context.
-   **Professional Structure:** Organized with separate `src` and `data` directories for scalability and maintainability.
-   **Secure Configuration:** Manages all API keys and secrets securely using a `.env` file, protected by `.gitignore`.
-   **Modular Codebase:** Built with separate modules for database connectors and data retrieval logic.
-   **Interactive Web UI:** A user-friendly interface built with Streamlit makes the assistant easy and engaging to use.
-   **Conversational Memory:** Remembers the last few turns of the conversation to answer follow-up questions naturally.

---
### **Setup and Installation**

#### **1. Prerequisites**
* Python 3.8+
* Docker Desktop
* Git

#### **2. Set Up Environment**
Create a .env file in the root directory and populate it with your API keys using the following template:
OPENAI_API_KEY="sk-..."
PINECONE_API_KEY="..."
NEO4J_URI="bolt://localhost:7687"
NEO4J_USER="neo4j"
NEO4J_PASSWORD="password"

Create and activate a Python virtual environment:
python -m venv .venv
####  Windows 
.venv\Scripts\activate
####  macOS/Linux
source .venv/bin/activate

**Install dependencies:**
pip install -r requirements.txt

---
#### **3. Start Services**
Make sure Docker Desktop is running.

Start the Neo4j database container:

docker run --rm -d -p 7687:7687 -p 7474:7474 --name neo4j-belabs -e NEO4J_AUTH=neo4j/password neo4j:5-community

---
#### **4. How to Run**
Load Neo4j Data:

python -m src.load_to_neo4j

Upload Pinecone Data (Requires a working OpenAI API key):
python -m src.pinecone_upload

---
#### **5. Launch the Web App:**
streamlit run app.py

