# Roamly — Multi-Agent AI Travel Planner

Roamly is an AI-powered travel planning application that turns a natural-language request into a researched, budget-aware, day-by-day itinerary.

## Problem statement

Planning a trip often requires switching between flight searches, hotel listings, weather forecasts, budgeting tools, and travel guides. Comparing this information manually is time-consuming, and the final plan can still feel disconnected or incomplete.

Roamly solves this problem by coordinating specialist AI agents that research different parts of a trip and combine their work into one itinerary that the traveller can review before finalizing.

## Solution / overview

The traveller describes a trip in plain language, including details such as the destination, duration, budget, interests, and preferences. A supervisor agent interprets the request and selects the specialists needed for the task.

The selected agents research flights, accommodation, weather, and estimated costs. An itinerary agent then combines their findings into a draft plan. The traveller can approve the draft or request changes before Roamly produces the final response.

## Key features

- Natural-language travel requests
- Supervisor-controlled multi-agent workflow
- Flight and airport research through AviationStack MCP
- Hotel and destination research through Tavily MCP
- Current weather and forecast information through OpenWeather
- Budget estimation based on the complete trip
- Day-by-day itinerary generation
- Human approval and revision before finalization
- Separate trip sessions using thread identifiers
- PostgreSQL checkpoint support with an in-memory fallback
- Responsive Streamlit interface

## Architecture / workflow

```text
Traveller request
       │
       ▼
Input guardrail
       │
       ▼
Supervisor agent
       │
       ├── Flight agent ───── AviationStack MCP
       ├── Hotel agent ────── Tavily MCP
       ├── Weather agent ──── OpenWeather MCP
       └── Budget agent
                │
                ▼
         Itinerary agent
                │
                ▼
          Human review
          ┌─────┴─────┐
       Approve      Revise
          └─────┬─────┘
                ▼
         Final travel plan
```

LangGraph controls the workflow and passes a shared travel state between agents. Streamlit provides the user interface, while MCP connects the agents to external travel and weather services.

## Tech stack

- Python
- Streamlit
- LangGraph
- LangChain
- Groq
- Model Context Protocol (MCP)
- Tavily
- AviationStack
- OpenWeather
- PostgreSQL and Psycopg

## Project structure

```text
itinerary_planer/
├── .streamlit/
│   └── config.toml              # Streamlit theme and toolbar settings
├── aviationstack-mcp/
│   └── src/aviationstack_mcp/   # Local AviationStack MCP server
├── agents.py                     # Supervisor and specialist agent logic
├── config.py                     # Environment and language-model configuration
├── frontend.py                   # Streamlit user interface
├── graph.py                      # LangGraph workflow and checkpoints
├── mcp_client.py                 # MCP server connections and tool wrappers
├── state.py                      # Shared workflow state definition
└── weather_mcp_server.py         # Local OpenWeather MCP server
```

The local `itinerary/` directory, when present, is the Python virtual environment and is not application source code.

## Setup & installation

### 1. Create a virtual environment

```bash
python3 -m venv itinerary
source itinerary/bin/activate
```

On Windows:

```powershell
python -m venv itinerary
itinerary\Scripts\activate
```

### 2. Install dependencies

```bash
pip install streamlit langgraph langchain langchain-groq \
  langchain-mcp-adapters "mcp>=1.24,<2" python-dotenv requests \
  "psycopg[binary,pool]" langgraph-checkpoint-postgres
```

### 3. Create the environment file

Create a `.env` file in the project root and add the variables listed below. Do not commit, publish, or share this file.

### 4. Configure PostgreSQL (optional)

Create a PostgreSQL database and provide its connection string through `DATABASE_URL`. If PostgreSQL is unavailable, Roamly uses in-memory checkpoints and trip state will be lost when the application restarts.

## Environment variables

Required for the complete experience:

```text
GROQ_API_KEY
TAVILY_API_KEY
AVIATIONSTACK_API_KEY
OPENWEATHER_API_KEY
```

Optional:

```text
GROQ_MODEL
DATABASE_URL
```

Never place real API keys in documentation, screenshots, or source files.

## How to run

Activate the virtual environment, then run:

```bash
streamlit run frontend.py
```

Open the address printed by Streamlit, normally:

```text
http://127.0.0.1:8501
```

Enter a trip request, select **Plan my journey**, review the research and draft itinerary, then select **Finish my plan** to generate the final response.

## Example input/output

### Example input

```text
Plan a 7-day Japan trip from Delhi under ₹2 lakh. I prefer boutique hotels,
vegetarian food, cultural experiences, and no overnight flights.
```

### Example output

Roamly returns a workspace containing:

- Suggested flight routes and airlines
- Recommended hotels or neighbourhoods
- Destination weather and packing guidance
- An estimated trip budget
- A seven-day sightseeing and activity schedule
- A final itinerary updated from the traveller's approval or feedback

Actual recommendations, prices, and availability depend on the request, travel dates, external APIs, and their subscription limits.
