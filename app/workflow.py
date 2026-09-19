from typing import TypedDict, Any
from langgraph.graph import StateGraph, END

from app.agents.agents import (
    RequirementAgent, PlanningAgent, DeveloperAgent,
    CodeReviewAgent, SecurityAgent
)
from app.core.audit import audit
from app.core.security import detect_prompt_injection, detect_secrets
from app.scanners.scanners import (
    run_tests, run_bandit, run_pip_audit, security_gate, scan_text_for_secrets
)

class SDLCState(TypedDict, total=False):
    requirement: str
    normalized_requirement: str
    plan: str
    generated_code: str
    code_review: str
    security_review: str
    prompt_injection_findings: list
    secret_hits: list
    test_result: dict
    bandit_result: dict
    dependency_result: dict
    gate_failures: list
    status: str
    human_approved: bool
    deployment: str

def build_workflow():
    llm = __import__("app.core.llm", fromlist=["GroqLLM"]).GroqLLM()
    req = RequirementAgent(llm)
    planner = PlanningAgent(llm)
    dev = DeveloperAgent(llm)
    reviewer = CodeReviewAgent(llm)
    security = SecurityAgent(llm)

    def requirement_node(s):
        findings = [f.__dict__ for f in detect_prompt_injection(s["requirement"])]
        s["prompt_injection_findings"] = findings
        if findings:
            audit("requirement", "requirement-agent", "prompt_injection_scan", "BLOCKED", {"findings": findings})
            s["status"] = "BLOCKED"
            s["gate_failures"] = ["Prompt injection detected in untrusted input."]
            return s
        s["normalized_requirement"] = req.run(s["requirement"])
        audit("requirement", "requirement-agent", "analyze", "PASS")
        return s

    def planning_node(s):
        s["plan"] = planner.run(s["normalized_requirement"])
        audit("planning", "planning-agent", "plan", "PASS")
        return s

    def development_node(s):
        s["generated_code"] = dev.run(s["plan"])
        s["secret_hits"] = scan_text_for_secrets(s["generated_code"])
        audit("development", "developer-agent", "generate_code",
              "BLOCKED" if s["secret_hits"] else "PASS",
              {"secret_hits": len(s["secret_hits"])})
        return s

    def review_node(s):
        s["code_review"] = reviewer.run(s["generated_code"])
        audit("code_review", "code-review-agent", "review", "PASS")
        return s

    def security_node(s):
        s["security_review"] = security.run(s["generated_code"])
        s["bandit_result"] = run_bandit()
        s["dependency_result"] = run_pip_audit()
        s["test_result"] = run_tests()
        failures = security_gate(s["bandit_result"], s["dependency_result"], s["secret_hits"])
        if s["test_result"]["returncode"] != 0:
            failures.append("Automated tests failed.")
        s["gate_failures"] = failures
        s["status"] = "BLOCKED" if failures else "AWAITING_HUMAN_APPROVAL"
        audit("security_gate", "gatekeeper", "evaluate",
              "BLOCKED" if failures else "PASS",
              {"failures": failures})
        return s

    def human_gate(s):
        approved = bool(s.get("human_approved", False))
        if s.get("status") != "AWAITING_HUMAN_APPROVAL":
            s["deployment"] = "NOT_AUTHORIZED"
        elif approved:
            s["deployment"] = "SIMULATED_DEPLOYMENT_SUCCESS"
            s["status"] = "RELEASED"
            audit("release", "human", "approve_release", "PASS")
            audit("deployment", "release-coordinator", "simulate_deployment", "PASS")
        else:
            s["deployment"] = "WAITING_FOR_HUMAN_APPROVAL"
            audit("release", "human", "approve_release", "PENDING")
        return s

    graph = StateGraph(SDLCState)
    graph.add_node("requirement", requirement_node)
    graph.add_node("planning", planning_node)
    graph.add_node("development", development_node)
    graph.add_node("review", review_node)
    graph.add_node("security_gate", security_node)
    graph.add_node("human_gate", human_gate)

    graph.set_entry_point("requirement")
    graph.add_conditional_edges("requirement", lambda s: "stop" if s.get("status") == "BLOCKED" else "continue",
                                {"stop": END, "continue": "planning"})
    graph.add_edge("planning", "development")
    graph.add_edge("development", "review")
    graph.add_edge("review", "security_gate")
    graph.add_edge("security_gate", "human_gate")
    graph.add_edge("human_gate", END)
    return graph.compile()
