import re
from dataclasses import dataclass

PROMPT_INJECTION_PATTERNS = [
    r"ignore (all|any|the) previous instructions",
    r"ignore (all|any) prior instructions",
    r"system prompt",
    r"reveal .*secret",
    r"print .*environment variables",
    r"deploy .*immediately",
    r"bypass .*security",
    r"disable .*security",
]

SECRET_PATTERNS = [
    r"(?i)(api[_-]?key|secret|password|token)\s*=\s*['\"][^'\"]{8,}['\"]",
    r"(?i)sk-[A-Za-z0-9]{20,}",
    r"(?i)ghp_[A-Za-z0-9]{20,}",
]

@dataclass
class Finding:
    severity: str
    category: str
    message: str

def detect_prompt_injection(text: str):
    findings = []
    for pattern in PROMPT_INJECTION_PATTERNS:
        if re.search(pattern, text):
            findings.append(Finding("HIGH", "prompt_injection",
                                    "Instruction-like content detected inside untrusted requirement text."))
    return findings

def detect_secrets(text: str):
    findings = []
    for pattern in SECRET_PATTERNS:
        if re.search(pattern, text):
            findings.append(Finding("CRITICAL", "secret", "Possible hardcoded secret detected."))
    return findings
