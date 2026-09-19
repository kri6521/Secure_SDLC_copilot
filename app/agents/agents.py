import json
from .prompts import (
    REQUIREMENT_SYSTEM, PLANNER_SYSTEM, DEVELOPER_SYSTEM,
    REVIEW_SYSTEM, SECURITY_SYSTEM
)
from app.core.llm import GroqLLM

class RequirementAgent:
    def __init__(self, llm): self.llm = llm
    def run(self, requirement):
        return self.llm.ask(REQUIREMENT_SYSTEM, requirement)

class PlanningAgent:
    def __init__(self, llm): self.llm = llm
    def run(self, normalized_requirement):
        return self.llm.ask(PLANNER_SYSTEM, normalized_requirement)

class DeveloperAgent:
    def __init__(self, llm): self.llm = llm
    def run(self, plan):
        return self.llm.ask(DEVELOPER_SYSTEM, plan)

class CodeReviewAgent:
    def __init__(self, llm): self.llm = llm
    def run(self, code):
        return self.llm.ask(REVIEW_SYSTEM, code)

class SecurityAgent:
    def __init__(self, llm): self.llm = llm
    def run(self, code):
        return self.llm.ask(SECURITY_SYSTEM, code)
