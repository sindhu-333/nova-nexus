# Nova Nexus

> Manufacturing Order Management (backend + minimal frontend)

Summary
- Lightweight FastAPI backend that provides intent-driven chat and REST endpoints to create and manage manufacturing orders.
- Minimal frontend UI at `index.html` for demo/interaction.
- In-memory datastore (no external DB). AI-powered extraction uses Groq (optional, requires API key).

Tech stack
- Python 3.10+ (recommend)
- FastAPI, Uvicorn
- Groq (optional, for `AIService`)

Getting started
1. Clone repo and enter project folder.
2. Install dependencies:

```bash
python -m pip install -r requirements.txt
```

3. Create a `.env` file with your Groq API key if you want AI extraction:

```text
GROQ_API_KEY=your_groq_api_key_here
```

Run (development)

```bash
# Option A - run via uvicorn
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Option B - run main directly
python main.py
```

Open the API docs at: http://localhost:8000/docs

Important files
- `main.py` — application entrypoint and route registration.
- `index.html` — minimal frontend UI (demo only).
- `requirements.txt` — Python dependencies.
- `test_person_b.py` — integration/unit-style tests used by the project.

Backend structure (brief)
- `routes/` — API route handlers
  - `chat_routes.py` — POST `/api/chat` and WebSocket `/ws` (main chat flow)
  - `order_routes.py` — REST endpoints for orders
- `services/` — business logic
  - `intent_service.py` — regex-based intent detection and utilities
  - `ai_service.py` — Groq-based extraction (raises if `GROQ_API_KEY` missing)
  - `order_service.py` — order CRUD helpers
  - `response_service.py` — canonical response formats (includes `ui_hint`)
- `database/` — in-memory stores (`orders`, `chat_history`)
- `websocket/` — `socket_manager.py` for broadcasting and streaming
- `utils/regex_utils.py` — extraction helpers (IDs, qty, material, deadline)

API Endpoints (summary)
- GET `/` — basic status and available endpoints
- POST `/api/chat` — main natural-language endpoint.
  - Expected body: `{ "message": "...", "user_id": "optional" }`
  - Routes based on detected intent: create order, update status, quality reports, show accepted orders.
- WebSocket `ws://<host>/ws` — real-time message broadcast and typing stream support.
- GET `/api/orders` — list all orders
- GET `/api/orders/{order_id}` — get order details
- POST `/api/orders` — create an order via REST (body: order fields)
- PUT `/api/orders/{order_id}/status` — update status (body: `{ "status": "..." }`)

Notes & behavior
- Storage is in-memory: `database/memory_store.py`. Restarting the server clears data.
- Intent detection is regex-first (`services/intent_service.py`) — AI is used only for structured extraction when needed.
- `services/ai_service.py` will raise if `GROQ_API_KEY` is not set; the system is designed to degrade gracefully.
- Responses follow the `ResponseGenerator` format and include `ui_hint` for frontend animations.

Testing
- See `HOW_TO_TEST.md` for detailed test instructions and expected outputs.
- Run the included test script:

```bash
python test_person_b.py
```

Quick troubleshooting
- If Groq calls fail, confirm `GROQ_API_KEY` in `.env` and installed packages.
- If you get `ModuleNotFoundError`, ensure `pip install -r requirements.txt` ran in the same Python environment.

Next steps
- Add persistent storage (Postgres, SQLite) if you need data durability.
- Add auth for the API and WebSocket connections for production.

License
- MIT-style (add a LICENSE file if needed)
