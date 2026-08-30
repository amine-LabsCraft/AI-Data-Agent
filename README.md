# 🤖 Agentic AI - Data Agent

A sophisticated multi-agent system for intelligent data processing and analysis using LangGraph. This project demonstrates a complete implementation of an agentic architecture with specialized sub-agents for SQL operations and ETL workflows.

![Project Overview](OverView.png)

## 📋 Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Project Structure](#project-structure)
- [Configuration](#configuration)
- [Usage](#usage)
- [Agent Descriptions](#agent-descriptions)
- [Data Models](#data-models)
- [Examples](#examples)
- [Security Features](#-security-features)
- [Development](#️-development)
- [Author](#-auteur)

---

## 🎯 Overview

**Agentic AI Data Agent** is an intelligent system that processes natural language queries and routes them to specialized agents for execution. The main agent acts as an intelligent router that understands user intent and delegates tasks to either the **SQL Analyst Agent** (for database queries) or the **ETL Analyst Agent** (for data extraction and transformation operations).

This project showcases modern AI engineering practices including:
- Multi-agent orchestration with LangGraph
- Intelligent routing based on natural language understanding
- Safety validation for SQL queries
- Tool-based agent architecture
- Dynamic reasoning selection based on task complexity

---

## 🏗️ Architecture

The system follows a hierarchical agent architecture:

```
┌─────────────────────────────────────────────────────────────┐
│                    Data Agent (Router)                      │
│         Routes user queries to appropriate sub-agents       │
└────────────────────┬────────────────────────────────────────┘
                     │
         ┌───────────┴───────────┐
         │                       │
         ▼                       ▼
    ┌──────────────┐        ┌──────────────┐
    │ SQL Analyst  │        │ ETL Analyst  │
    │   Agent      │        │   Agent      │
    └──────────────┘        └──────────────┘
         │                       │
         ├─► Query Curation      ├─► Extract Load
         ├─► Schema Context      ├─► Transform Load
         ├─► SQL Generation      └─► Code Execution
         ├─► Safety Validation   
         ├─► Query Execution     
         └─► Answer Generation   
```

### State Flow

1. **User Input** → Natural language query
2. **Router Node** → Classifies query as SQL or ETL
3. **Agent Dispatch** → Routes to appropriate sub-agent
4. **Processing** → Each agent processes the task
5. **Output** → Returns structured result to user

---

## ✨ Features

### Core Capabilities

- **Intelligent Query Routing**: Automatically classifies user queries as SQL or ETL operations
- **SQL Analysis Agent**:
  - Natural language to SQL query conversion
  - Automatic schema context gathering
  - SQL safety validation (prevents harmful operations)
  - Query execution on PostgreSQL database
  - Empty-schema guard: if no tables are found, the agent stops before generating SQL instead of hallucinating table/column names
  - Markdown-fence stripping on generated SQL (some models wrap SQL in ` ```sql ` blocks despite instructions not to)

- **ETL Agent**:
  - API data extraction (JSON to structured formats)
  - Data transformation using Pandas
  - Multi-format support (CSV, JSON, Parquet)
  - Dynamic code generation based on user requirements
  - Safe code execution

- **Two-Tier Reasoning Selection** (`pick_llm`):
  - `"low"` — reasoning disabled: fast, low-cost calls for simple tasks (question curation, final answer formatting)
  - `"high"` — reasoning enabled: used for SQL generation, safety judgment, and tool-use decisions
  - Both tiers call the **same OpenRouter model**; only the `reasoning` parameter is toggled between calls

- **Safety & Validation**:
  - SQL query safety checking via a dedicated LLM judge
  - Protection against database modifications (INSERT, UPDATE, DELETE, DROP, etc.)
  - Structured output validation using Pydantic
  - Fail-safe error handling: every LLM call is wrapped so a provider hiccup (timeout, rate limit) degrades gracefully instead of crashing the whole graph

---

## 📦 Prerequisites

- Python 3.12+
- PostgreSQL database (for SQL operations)
- OpenRouter API key (used by `pick_llm` for both reasoning tiers)
- Virtual environment (recommended)

---

## 🚀 Installation

### 1. Clone and Setup Project

```bash
cd Data_Agent
python -m venv .venv

# Activate virtual environment
# On Windows:
.\.venv\Scripts\Activate.ps1
# On macOS/Linux:
source .venv/bin/activate
```

### 2. Install Dependencies

```bash
uv pip install -r requirements.txt
# or
pip install -e .
```

This installs:
- **langchain**: Core LLM framework
- **langgraph**: Multi-agent orchestration
- **langchain-openai**: Used to talk to OpenRouter's OpenAI-compatible endpoint (`pick_llm`)
- **pandas**: Data processing
- **psycopg2**: PostgreSQL driver
- **pydantic**: Data validation
- **python-dotenv**: Environment configuration

### 3. Environment Configuration

Create a `.env` file in the root directory (see `.env.example`):

```env
# LLM Configuration (OpenRouter)
OPENROUTER_API_KEY=your_openrouter_api_key_here

# Database Configuration
host=localhost
port=5432
user=postgres
password=your_password
database=data_agent_db
```

---

## 📁 Project Structure

```
Data_Agent/
├── agents/                          # Agent implementations
│   ├── __init__.py
│   ├── data_agent.py               # Main router agent
│   ├── sql_analyst.py              # SQL query agent
│   └── etl_analyst.py              # ETL operations agent
│
├── Models/                          # Data models
│   ├── __init__.py
│   └── schema.py                   # Pydantic schemas for state management
│
├── utils/                           # Utility modules
│   ├── __init__.py
│   ├── database.py                 # PostgreSQL utilities
│   ├── etl_tools.py                # ETL operations toolkit
│   ├── llm_pick.py                 # LLM selection logic (OpenRouter, low/high reasoning)
│
├── data/                            # Data directory
│   ├── extract/                     # Extracted data storage
│   ├── transform/                   # Transformed data storage
│   ├── payments.csv                 # Sample dataset
│   ├── ratings.csv                  # Sample dataset
│   ├── rides.csv                    # Sample dataset
│   ├── users.csv                    # Sample dataset
│   └── vehicles.csv                 # Sample dataset
│
├── main.py                          # Entry point
├── feed_db.py                       # Database initialization script
├── pyproject.toml                   # Project metadata and dependencies
├── .env.example                     # Environment variables template
├── OverView.png                     # Project overview image
├── sql_analyst_graph.png            # Auto-generated LangGraph diagram (SQL Analyst)
└── README.md                        # This file
```

---

## ⚙️ Configuration

### LLM Selection (`utils/llm_pick.py`)

`pick_llm()` selects between two reasoning tiers on the **same OpenRouter model**, toggling the `reasoning` parameter rather than switching providers:

```python
from utils.llm_pick import pick_llm

llm_fast  = pick_llm("low")   # No reasoning — question curation, final answer formatting
llm_smart = pick_llm("high")  # Reasoning enabled — SQL generation, safety judgment, tool-use
```

### Database Configuration (`utils/database.py`)

```python
from utils.database import DatabaseUtil

conn_details = {
    "host": "localhost",
    "port": 5432,
    "user": "postgres",
    "password": "password",
    "dbname": "data_agent_db"
}

db = DatabaseUtil(conn_details)
schema_info = db.schema_details("public")
```

---

## 💻 Usage

### Running the Data Agent

**Basic Usage:**

```python
from agents.data_agent import data_agent
from langchain_core.messages import HumanMessage

# Example: Extract data from API
response = data_agent.invoke({
    "messages": [
        HumanMessage(content="""
            I want to extract the data from the API endpoint 
            'https://pokeapi.co/api/v2/pokemon' and save it to 
            data/extract folder in CSV format
        """)
    ],
    "route_response": ""
})

print(response)
```

**SQL Query Example:**

```python
response = data_agent.invoke({
    "messages": [
        HumanMessage(content="""
            What payment methods are used across all transactions?
        """)
    ],
    "route_response": ""
})
```

**ETL Example:**

```python
response = data_agent.invoke({
    "messages": [
        HumanMessage(content="""
            Transform the rides.csv data by filtering only completed 
            rides and save to data/transform
        """)
    ],
    "route_response": ""
})
```

### Running from Command Line

```bash
# Run the main data agent
python main.py

# Run individual agents
python agents/sql_analyst.py
python agents/etl_analyst.py
```

---

## 🤖 Agent Descriptions

### 1. **Data Agent (Main Router)**
**File:** `agents/data_agent.py`

**Responsibility:** 
- Receives natural language user queries
- Classifies queries as either SQL or ETL operations
- Routes queries to appropriate sub-agents
- Aggregates results and returns to user

**Components:**
- **Router Node**: Uses structured output to classify query intent
- **Conditional Routing**: Routes to SQL or ETL based on classification
- **Graph Orchestration**: Manages workflow using LangGraph

---

### 2. **SQL Analyst Agent**
**File:** `agents/sql_analyst.py`

![SQL Analyst Graph](sql_analyst_graph.png)

**Responsibility:**
- Converts natural language queries to SQL
- Handles all database query operations
- Validates query safety
- Executes queries and returns results

**Workflow:**
1. **Query Curation** - Rephrases the user's question into a single clear sentence (never answers it)
2. **Context Gathering** - Fetches database schema details
3. **Prompt Construction** - Creates detailed context for LLM
4. **SQL Generation** - Generates SQL query using LLM; skipped entirely if no tables were found in the schema
5. **Safety Check** - Validates query safety; defaults to "unsafe" if the query is empty or the judge call fails
6. **Query Execution** - Executes validated query on database
7. **Answer Generation** - Formats and returns results

**Safety Features:**
- Prevents execution of dangerous commands (INSERT, UPDATE, DELETE, DROP, ALTER)
- Validates query before execution
- Automatic result limiting to 10 rows (unless specified)
- Schema validation against database
- Fails safe: any missing schema, generation error, or judge error routes to the "unsafe/cancelled" path rather than proceeding blindly

---

### 3. **ETL Analyst Agent**
**File:** `agents/etl_analyst.py`

**Responsibility:**
- Handles data extraction from APIs
- Performs data transformation using Pandas
- Manages data loading to various formats
- Executes code safely in controlled environment

**Workflow:**
1. **Tool Binding** - Attaches ETL tools to LLM
2. **User Intent Understanding** - Analyzes transformation requirements
3. **Tool Selection** - Chooses appropriate ETL operation
4. **Code Generation** - Generates Pandas code for transformation
5. **Safe Execution** - Executes generated code in a controlled environment, capturing stdout as output
6. **Result Reporting** - Returns execution status, generated code, and any captured output

**Supported Tools:**
- **extract_load_tool**: Extract from API → Load to storage
- **transform_load_tool**: Transform data using Pandas → Load result

**Supported Formats:**
- CSV (default)
- JSON (Lines or Records)
- Parquet

---

## 📊 Data Models

### AgentSchema (SQL Agent State)
```python
class AgentSchema(BaseModel):
    messages: List                    # Conversation messages
    user_question: str                # Original user query
    curated_ques: str                 # Refined question
    prompt_query_context: str         # Database context + prompt
    generated_sql_query: str          # Generated SQL
    is_safe: Literal["Yes", "No"]     # Safety validation result
    comments: str                     # Safety check comments
    sql_query_execution_result: str   # Query result
    final_answer: str                 # Final formatted answer
```

### ETLAgentSchema (ETL Agent State)
```python
class ETLAgentSchema(BaseModel):
    messages: List                    # Conversation messages
```

### RouterSchema (Query Classification)
```python
class RouterSchema(BaseModel):
    answer: Literal["sql", "etl"]     # Query classification
    comments: str                     # Reasoning for classification
```

### DataAgentSchema (Main Agent State)
```python
class DataAgentSchema(BaseModel):
    messages: List                    # All conversation messages
    route_response: str               # Router decision (sql/etl)
```

---

## 📚 Examples

### Example 1: Database Query

**User Query:**
```
"What payment methods are used across all transactions?"
```

**Processing:**
1. Router classifies as SQL query
2. SQL Agent fetches schema (`users`, `vehicles`, `rides`, `payments`, `ratings`)
3. Generates: `SELECT DISTINCT payment_method FROM payments ORDER BY payment_method LIMIT 10;`
4. Validates safety ✓
5. Executes and returns: `apple_pay`, `credit_card`, `debit_card`, `google_pay`, `paypal`

---

### Example 2: Data Extraction

**User Query:**
```
"Extract the data from 'https://pokeapi.co/api/v2/pokemon' and save it as CSV"
```

**Processing:**
1. Router classifies as ETL operation
2. ETL Agent selects extract_load_tool
3. Makes API request to endpoint
4. Normalizes JSON response
5. Saves to `data/extract/extracted_data.csv`

---

### Example 3: Data Transformation

**User Query:**
```
"Transform rides.csv to keep only completed rides and save as JSON"
```

**Processing:**
1. Router classifies as ETL operation
2. ETL Agent analyzes requirement
3. Generates Pandas code filtering on `status == 'completed'`
4. Executes code safely
5. Saves result to `data/transform/` in JSON format

---

## 🔐 Security Features

✅ **SQL Safety Validation**
- Query inspection before execution via a dedicated LLM judge
- Blocks destructive operations
- Database structure protection
- Fails safe on any error: an empty generated query or a judge-call failure is always treated as "unsafe" rather than defaulting to "proceed"

✅ **Parameterized Schema Introspection**
- Table/column identifiers are quoted via `psycopg2.sql.Identifier` when sampling data, rather than interpolated with f-strings

✅ **Safe Code Execution**
- Sandboxed Python code execution with isolated locals
- Captured stdout returned as part of the execution report
- Input validation and typed error reporting

✅ **Environment Security**
- Credentials stored in `.env` (git-ignored via `.gitignore`)
- Sensitive data protection
- Proper exception handling throughout

✅ **Resilience**
- Every LLM call (curation, generation, judging, summarization) is wrapped in error handling with a safe fallback, so a single provider hiccup (timeout, rate limit) never crashes the whole pipeline

---

## 🛠️ Development

### Adding a New Agent

1. Create new agent file in `agents/` directory
2. Define state schema in `Models/schema.py`
3. Implement agent nodes using LangGraph
4. Add routing logic in `data_agent.py`
5. Update documentation

### Extending ETL Tools

Add new tools in `utils/etl_tools.py`:

```python
@tool
def new_tool(param: str) -> str:
    """Tool description"""
    # Implementation
    pass
```

### Customizing LLM Selection

Modify `utils/llm_pick.py` to adjust:
- Which OpenRouter model is used
- The `reasoning.max_tokens` budget for the `"high"` tier
- Temperature and other parameters

---

## 📝 Environment Variables Reference

| Variable | Description | Example |
|----------|-------------|---------|
| `OPENROUTER_API_KEY` | OpenRouter API key (used by `pick_llm`) | `sk-or-v1-...` |
| `host` | PostgreSQL host | `localhost` |
| `port` | PostgreSQL port | `5432` |
| `user` | PostgreSQL user | `postgres` |
| `password` | PostgreSQL password | `your_password` |
| `database` | Database name | `data_agent_db` |

---

## 🚨 Troubleshooting

### Issue: "Database connection failed"
**Solution:** Verify PostgreSQL is running and credentials in `.env` are correct.

### Issue: "API key not found"
**Solution:** Ensure `OPENROUTER_API_KEY` is set in `.env`.

### Issue: "SQL query unsafe" / query cancelled
**Solution:** The query contains destructive operations, or no valid query could be generated. Reformulate as a SELECT query only.

### Issue: Generated SQL references a table that doesn't exist
**Solution:** This usually means schema introspection returned no tables. Verify the target database actually has tables in the `public` schema, and that `.env` points to the right database — the agent now stops before generating SQL when the schema is empty, instead of guessing table names.

### Issue: "Module not found"
**Solution:** Activate virtual environment and reinstall dependencies.

---

## 📈 Performance Considerations

- **Reasoning Selection**: Simple tasks use the `"low"` tier (no reasoning) for faster, cheaper responses
- **Database Optimization**: Add indexes for frequently queried columns
- **API Rate Limiting**: Respect rate limits of external APIs and OpenRouter's free-tier models
- **Memory Usage**: Large dataset transformations may require optimization

---

**Last Updated:** August 2026
**Version:** 0.1.0

---

## 👤 Auteur
**Amine Ait Ali**  
Data Engineering · AI
[![GitHub](https://img.shields.io/badge/GitHub-amine--LabsCraft-181717?style=flat&logo=github)](https://github.com/amine-LabsCraft)
[![Portfolio](https://img.shields.io/badge/Portfolio-amine--aitali--5752.netlify.app-00C7B7?style=flat&logo=netlify&logoColor=white)](https://amine-aitali-5752.netlify.app/)