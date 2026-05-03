Calculator FastAPI app

- Run: `pip install -r requirements.txt`
- Start: `python Calculator.py` (starts on port 8000)
- Opens UI at `http://localhost:8000/`
- API: POST `/api/calc` with JSON `{ "expr": "2+2" }` returns `{ "result": 4 }`
