# Namma Vivasayam - Knowledge Graph RAG Chatbot

## Project Overview

Namma Vivasayam is a bilingual chatbot developed to help users understand Tamil Nadu government agricultural schemes, subsidies, eligibility criteria and benefits.

This project uses **Knowledge Graphs and Retrieval-Augmented Generation (RAG)** to retrieve relevant scheme information and generate responses in English or Tamil.

The application is built using Python, LangChain, Neo4j AuraDB and Streamlit.

## Objective

The main objective of this project is to understand how Knowledge Graphs can be combined with RAG to build an intelligent chatbot.

The application demonstrates how to:

- Extract information from agricultural scheme documents.
- Identify entities and relationships.
- Store structured information in Neo4j AuraDB.
- Retrieve relevant information using GraphRAG.
- Generate answers using an OpenAI language model.
- Implement basic AI guardrails for safer responses.
- Build a bilingual chatbot interface using Streamlit.

## Technologies Used

- **Python:** Application development
- **Streamlit:** Chatbot user interface
- **LangChain:** LLM integration and RAG workflow
- **Neo4j AuraDB:** Knowledge Graph database
- **OpenAI:** Language model and embeddings
- **Pydantic:** Structured information extraction
- **Python-dotenv:** Environment variable management
- **Regular Expressions:** Basic input guardrails

## Key Features

### 1. Knowledge Graph Creation

Agricultural scheme information is processed to identify important entities such as:

- Government schemes
- Departments
- Beneficiaries
- Benefits
- Eligibility criteria
- Required documents

These entities are connected through relationships and stored in Neo4j AuraDB.

### 2. GraphRAG Chatbot

The chatbot retrieves relevant scheme information from Neo4j and uses an OpenAI language model to generate answers.

The application combines vector similarity search with Knowledge Graph relationships to provide context-based responses.

### 3. Bilingual Support

Users can switch between English and Tamil to ask questions and receive responses in their preferred language.

### 4. AI Guardrails

Basic guardrails are implemented to:

- Restrict unrelated questions.
- Detect common prompt injection attempts.
- Prevent users from submitting certain personal information.
- Handle empty responses.
- Encourage answers based on available Knowledge Graph information.

These are introductory safeguards and do not guarantee complete protection against unsafe or inaccurate responses.

### 5. User-Friendly Interface

The Streamlit application includes:

- Agricultural-themed banner
- English and Tamil language selector
- Question input with Ask button
- Clear Chat option
- Suggested questions
- Conversation history
- Responsive layout

### 6. Knowledge Graph Visualization

The generated Knowledge Graph can be explored directly in Neo4j AuraDB using Cypher queries.

The graph is not displayed inside the chatbot interface.

## Project Structure

```text
Namma_vivasayam_knowledgegraph/
│
├── assets/
│   └── agri_banner.png
│
├── vivasayam.py
├── graph_pipeline.py
├── rag_engine.py
├── guardrails.py
├── test_neo4j.py
├── scheme_content.txt
├── requirements.txt
├── .env
├── .gitignore
└── README.md
```

## How the Application Works

**Step 1: Data Preparation**

Agricultural scheme information is collected and saved in `scheme_content.txt`.

**Step 2: Entity Extraction**

LangChain and an OpenAI model extract scheme details, entities and relationships.

**Step 3: Knowledge Graph Creation**

Extracted entities and relationships are stored in Neo4j AuraDB using `graph_pipeline.py`.

**Step 4: User Question**

The user enters a question in English or Tamil through the Streamlit application.

**Step 5: Guardrail Validation**

The question is checked for restricted content, personal information and common prompt injection patterns.

**Step 6: GraphRAG Retrieval**

The application searches the Neo4j Knowledge Graph for relevant information using `rag_engine.py`.

**Step 7: Response Generation**

The language model generates an answer using the retrieved information.

**Step 8: Chatbot Response**

The answer is displayed below the user's question in the selected language.

## Installation and Setup

### 1. Clone the Repository

```bash
git clone <your-repository-url>
cd Namma_vivasayam_knowledgegraph
```

### 2. Activate the Virtual Environment

Create a virtual environment if you do not already have one:

```bash
python -m venv newvenv
```

Activate it on Windows:

```bash
newvenv\Scripts\activate
```

### 3. Install Required Packages

```bash
python -m pip install -r requirements.txt
```

If `truststore` is not included in your requirements file, install it separately:

```bash
python -m pip install truststore
```

### 4. Configure Environment Variables

Create a `.env` file in the project folder and add:

```dotenv
OPENAI_API_KEY=your_openai_api_key

NEO4J_URI=neo4j+s://your-instance.databases.neo4j.io
NEO4J_USERNAME=your_neo4j_username
NEO4J_PASSWORD=your_neo4j_password
NEO4J_DATABASE=neo4j
```

Replace the placeholder values with your own credentials.

Do not upload the `.env` file to GitHub.

### 5. Test Neo4j Connection

```bash
python test_neo4j.py
```

Expected output:

```text
Neo4j AuraDB connected successfully!
Hello from Neo4j!
```

### 6. Create the Knowledge Graph

```bash
python graph_pipeline.py
```

This processes the agricultural scheme information and stores the entities and relationships in Neo4j AuraDB.

### 7. Run the Streamlit Application

```bash
python -m streamlit run vivasayam.py
```

Open the application in your browser:

```text
http://localhost:8501
```

## View the Knowledge Graph in Neo4j

Log in to Neo4j AuraDB and open the Query workspace.

Run the following Cypher query:

```cypher
MATCH (s:Scheme)-[r]-(n)
RETURN s, r, n
LIMIT 100;
```

To view the relationships for a specific scheme:

```cypher
MATCH (s:Scheme)-[r]-(n)
WHERE toLower(s.name) CONTAINS toLower("PM-KISAN")
RETURN s, r, n;
```

This allows users to explore individual scheme relationships without displaying the Knowledge Graph in the chatbot.

## Sample Questions

**English:**

- What are the benefits of PM-KISAN?
- What agricultural subsidies are available?
- Who is eligible for irrigation subsidies?
- What documents are required for government schemes?

**Tamil:**

- பிஎம் கிசான் திட்டத்தின் பயன்கள் என்ன?
- விவசாயிகளுக்கு என்ன மானியங்கள் உள்ளன?
- பாசன மானியத்திற்கு யார் தகுதியானவர்கள்?
- அரசு திட்டங்களுக்கு என்ன ஆவணங்கள் தேவை?

Answers depend on the scheme information available in the Knowledge Graph.

## Learning Outcomes

Through this project, I learned:

- The fundamentals of Knowledge Graphs and GraphRAG.
- How to create nodes and relationships in Neo4j.
- How to use Cypher queries to explore graph data.
- How to combine vector search and graph relationships.
- How to integrate OpenAI models with LangChain.
- How to implement basic AI guardrails.
- How to develop a bilingual Streamlit chatbot.
- How to connect a Python application to Neo4j AuraDB.

## Future Improvements

- Add more verified government agricultural schemes.
- Improve entity extraction and relationship mapping.
- Implement stronger retrieval confidence checks.
- Add official government source references to responses.
- Improve Tamil-language query understanding.
- Add automated testing for guardrails and retrieval accuracy.

## Disclaimer

This application is developed for educational purposes.

Scheme details, benefits and eligibility requirements should be verified through official government websites before making decisions.

## Conclusion

Namma Vivasayam demonstrates how Knowledge Graphs, Neo4j AuraDB, LangChain and RAG can be combined to build a bilingual agricultural scheme assistant.

The project helped me gain practical experience in Knowledge Graph creation, graph-based retrieval, AI guardrails and Streamlit application development."# Nammavivasayam_Chatbot" 
