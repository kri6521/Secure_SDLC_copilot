import subprocess
import sys
import re
from pathlib import Path

def run_command(args):
    try:
        p = subprocess.run(args, capture_output=True, text=True, timeout=60)
        return {
            "returncode": p.returncode,
            "stdout": p.stdout[-12000:],
            "stderr": p.stderr[-6000:],
        }
    except Exception as e:
        return {"returncode": 99, "stdout": "", "stderr": str(e)}

def run_tests():
    return run_command([sys.executable, "-m", "pytest", "-q"])

def run_bandit(path="sample_app"):
    return run_command([sys.executable, "-m", "bandit", "-r", path, "-q"])

def run_pip_audit():
    # pip-audit is deterministic; an unavailable network is treated as a scanner error,
    # not as a security pass.
    return run_command([sys.executable, "-m", "pip_audit", "-r", "requirements.txt"])

def scan_text_for_secrets(text):
    patterns = [
        r"(?i)(api[_-]?key|secret|password|token)\s*=\s*['\"][^'\"]{8,}['\"]",
        r"(?i)sk-[A-Za-z0-9]{20,}",
        r"(?i)ghp_[A-Za-z0-9]{20,}",
    ]
    return [p for p in patterns if re.search(p, text)]

def security_gate(bandit_result, audit_result, secret_hits):
    failures = []
    if secret_hits:
        failures.append("Possible hardcoded secret detected.")
    if bandit_result["returncode"] != 0:
        failures.append("Bandit reported security findings or could not complete.")
    if audit_result["returncode"] != 0:
        failures.append("Dependency scan failed or found vulnerable dependencies.")
    return failures
