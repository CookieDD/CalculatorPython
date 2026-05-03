Calculator FastAPI app

This repository contains a small calculator web app implemented with FastAPI (backend) and a static frontend shipped in `static/`.

Usage
- Run: `pip install -r requirements.txt`
- Start: `python Calculator.py` (starts on port 8000)
- Opens UI at `http://localhost:8000/`
- API: POST `/api/calc` with JSON `{ "expr": "2+2" }` returns `{ "result": 4 }`

Authorship & Repository Management
- Developed by: AI Agent (assistant) running in an automated code-assistant mode.
- Language model used: GPT-5 mini.
- Repository and git control: initialized, committed, and pushed to the remote by the AI Agent on the user's machine.

Notes
- Review the code before deploying to production. The AI Agent implemented and pushed the initial project code and repository configuration; any further changes should be audited and approved by a human maintainer.
