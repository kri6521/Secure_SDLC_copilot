from fastapi import FastAPI
from pydantic import BaseModel
from app.workflow import build_workflow

app = FastAPI(title="SecureSDLC Copilot")

class RunRequest(BaseModel):
    requirement: str
    human_approved: bool = False

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/run")
def run(req: RunRequest):
    workflow = build_workflow()
    result = workflow.invoke({
        "requirement": req.requirement,
        "human_approved": req.human_approved,
    })
    return result
