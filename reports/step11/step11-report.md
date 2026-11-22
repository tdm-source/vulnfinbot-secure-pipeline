# Step 11 — Controlled Vulnerability Detection and Remediation

## 1. Objective

The objective was to introduce a controlled insecure coding pattern in a
separate demonstration file, verify its detection using SAST tools, fix the
vulnerability, and compare the scan results.

The demonstration was performed in a test environment and was not deployed
to production.

## 2. Vulnerability Before Remediation

File: security/demo/insecure_example.py

Insecure code:
    return eval(user_input)

Semgrep detected:
- Rule: security.semgrep.python-eval-usage
- Severity: ERROR
- Findings: 1

Bandit detected:
- Test ID: B307
- Issue: blacklist — possibly insecure function eval()
- Severity: MEDIUM
- Confidence: HIGH
- Findings: 1

The use of eval() with untrusted input can lead to arbitrary code execution.

## 3. Remediation

The insecure eval() call was replaced with ast.literal_eval().

Additional input validation was implemented to allow only integer and
floating-point values.

The corrected implementation rejects unsupported data types and does not
execute arbitrary Python expressions.

## 4. Verification After Remediation

Semgrep:
- Findings: 0

Bandit:
- No issues identified
- Findings: 0

Functional tests:
- Integer input: passed
- Floating-point input: passed
- Malicious Python expression: rejected

## 5. Before and After Comparison

| Scanner | Before | After |
|---------|--------|-------|
| Semgrep | 1 finding | 0 findings |
| Bandit | 1 medium issue | 0 issues |

## 6. Conclusion

Both SAST tools successfully detected the intentionally introduced
insecure eval() pattern.

After replacing eval() with ast.literal_eval() and adding numeric
type validation, both scanners reported zero findings.

The remediation was verified with functional tests. The full project
test suite also passed: 20 tests passed.

This experiment demonstrates the value of integrating static
application security testing into the development workflow.
