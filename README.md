# SecureSDLC Copilot

A focused prototype for an agent-assisted, security-gated Software Development Life Cycle.

## What it demonstrates

Requirement analysis → planning → development → code review → security assessment → testing → human approval → deployment simulation → audit evidence.

The key design principle is **controlled autonomy**:
- Agents have narrowly defined responsibilities.
- Generated code is treated as untrusted until reviewed.
- Security/quality failures block release.
- Deployment is simulated and requires explicit human approval.
- The workflow records an audit trail.
- Prompt-injection text in requirements is treated as data, not authority.

## Stack

- Python
- Groq API
- LangGraph
- FastAPI
- Streamlit
- pytest
- Bandit
- pip-audit
- python-dotenv

## Setup

### 1. Create a virtual environment

Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### 2. Configure Groq

Copy `.env.example` to `.env` and add your Groq API key.

```text
GROQ_API_KEY=your_key_here
GROQ_MODEL=openai/gpt-oss-120b
```

Never commit `.env`.

### 3. Run the API

```powershell
uvicorn app.main:app --reload
```

### 4. Run the dashboard

```powershell
streamlit run app/dashboard.py
```

## Usage

Use the sample requirement:

> Add a secure login endpoint to the sample Python application. Validate email and password, hash passwords securely, return a generic authentication error, and add tests.

The dashboard can also inject a synthetic malicious instruction into the requirement to demonstrate prompt-injection handling.

## Security gates

The prototype has explicit gates for:
- hardcoded secrets
- Bandit static security findings
- dependency vulnerabilities via pip-audit
- test failures
- code review findings
- prompt-injection indicators
- unauthorized deployment

A failed gate changes the workflow to `BLOCKED`. The release simulator refuses deployment unless all gates pass and a human approval flag is present.

## Important assessment talking points

1. **Human-in-the-loop:** code merge/release remains a human-controlled action.
2. **Least privilege:** each agent has a declared tool permission set.
3. **Untrusted input:** requirements are data; workflow policy is outside the requirement.
4. **Defense in depth:** LLM review is not considered a substitute for deterministic scanners.
5. **Traceability:** each stage writes structured evidence to `audit_logs/audit.jsonl`.
6. **Fail closed:** critical security/test failures stop release.
7. **No real deployment:** the prototype only simulates deployment.
