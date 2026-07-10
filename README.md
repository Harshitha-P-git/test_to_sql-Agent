# Text-to-SQL Agent (LangGraph + Ollama)

An agentic Text-to-SQL system that converts natural language questions into SQL, executes them against a live SQLite database, and returns natural-language answers — running fully offline on a local LLM (Llama 3.2 via Ollama), no API key required.

## Overview

Instead of a single LLM prompt, this project uses **LangGraph** to orchestrate a stateful, multi-step agent workflow:

1. **Resolve current user** — looks up the requesting user via SQLAlchemy ORM.
2. **Check relevance** — the LLM decides whether the question is even answerable from the schema (`users`, `food`, `orders`) before doing anything else, so off-topic questions get a friendly deflection instead of hallucinated SQL.
3. **Convert to SQL** — generates SQL constrained by the live, runtime-introspected DB schema, using structured JSON output (validated with Pydantic) rather than free-form text.
4. **Execute SQL** — runs the query for real against SQLite, including writes (`INSERT`), not just reads.
5. **Self-correction loop** — if execution fails, the question is rewritten and SQL regenerated, up to 5 attempts, before giving up gracefully.
6. **Generate human-readable answer** — turns raw query results into a natural, personalized response.

State (question, generated SQL, results, error flags, retry count) is threaded through every node so the graph can make routing decisions based on what happened in earlier steps.

## Tech Stack

- **LangGraph** — stateful agent orchestration
- **LangChain core** — prompt templates, structured output parsing
- **Ollama + Llama 3.2** — local LLM inference, zero cost, zero API key
- **SQLAlchemy** — ORM, schema introspection, SQL execution
- **SQLite** — database

## Setup

```bash
pip install langgraph langchain-core langchain-community langchain-ollama sqlalchemy pydantic python-dotenv ipython notebook
ollama pull llama3.2
python -m notebook sql-agent-llama.ipynb
```

Then run all cells. `example.db` ships with sample `users`, `food`, and `orders` data.

## Notes from getting this running locally

A few real issues came up standing this up on a fresh machine, worth documenting:

- **Deprecated import**: `langchain_community.chat_models.ChatOllama` no longer exists in current `langchain-community` — it moved to the standalone `langchain_ollama` package. Fixed by updating the import.
- **`create_sql_agent` (LangChain's built-in tool-calling agent) silently hallucinated results** instead of running real queries when paired with a local model — traced by testing `bind_tools()` directly (which worked fine), which pointed to the legacy `AgentExecutor` path as the problem, not the model. This project's hand-rolled LangGraph implementation (structured JSON output instead of native tool-calling) proved more reliable with a small local model.


