# Mini-VulnFinBot Secure Pipeline

Small Flask "financial assistant" (mock AI responses) with a GitHub Actions pipeline that runs
unit tests, SAST, dependency, container and DAST scans, plus AI-specific security tests.

## Technologies

Python 3.12, Flask, pytest, gunicorn, Docker, GitHub Actions, Bandit, Semgrep, pip-audit, Trivy, OWASP ZAP.

## Architecture

```
client -> Flask app (app/routes.py)
            |- GET  /health
            |- POST /api/chat -> validation -> mock AI generator -> output validation -> JSON
GitHub push/PR -> tests job -> security job (Bandit, Semgrep, pip-audit, Docker build, Trivy, ZAP, AI tests) -> artifact
```

## Install and run

```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\\Scripts\\activate
pip install -r requirements.txt
python run.py                   # http://localhost:5000/health
curl -X POST localhost:5000/api/chat -H "Content-Type: application/json" -d '{"message":"How do I budget?"}'
```

## Tests

```bash
pytest -v
python -m security.ai\_report    # writes reports/ai-security-report.md
```

## Docker

```bash
docker build -t vulnfinbot:latest .
docker run --rm -p 5000:5000 vulnfinbot:latest
```

## CI/CD pipeline

`.github/workflows/security-pipeline.yml` runs on push and pull requests to `main`.
Scanner steps use `continue-on-error`, so reports are always uploaded.

## Security tools

|Tool|Purpose|Report|
|-|-|-|
|Bandit|Python SAST|bandit-report.json|
|Semgrep|Custom rule SAST (`security/semgrep/rules.yml`)|semgrep-report.json|
|pip-audit|Dependency CVEs|dependency-report.json|
|Trivy|Docker image CVEs|trivy-report.json|
|OWASP ZAP|DAST baseline|zap-report.json|
|AI tests|Prompt injection etc. (mock)|ai-security-report.md|

## Accessing reports

GitHub -> Actions -> select run -> Artifacts -> `vulnfinbot-security-reports`.

## Limitations

The AI responses are a mock. The AI tests check application-level controls only; they do not prove
that a real LLM resists prompt injection.

## Findings and remediation

The following results were obtained during the security assessment of Mini-VulnFinBot.

| Security tool | Result | Assessment and remediation |
| --- | --- | --- |
| Bandit | No findings detected | No Bandit-detected Python security issues were reported in the scanned files. |
| Semgrep | No findings detected | No matches were found for the configured custom security rules. |
| pip-audit | 0 known vulnerabilities | No known vulnerabilities were reported in the scanned Python dependencies. |
| Trivy | 246 findings: 51 HIGH, 106 MEDIUM, 82 LOW, 7 UNKNOWN | Review the affected OS packages and Python dependencies. Prioritize HIGH findings, update affected packages or the base image where compatible, then rebuild and rescan the image. |
| OWASP ZAP | Informational alert: Non-Storable Content | The alert appeared on the application and default resource URLs. Review the response headers and confirm that caching behavior is intentional. |
| AI Security Tests | 5 scenarios passed | Application-level tests passed for prompt injection handling, system prompt disclosure, sensitive information disclosure, unauthorized tool usage, and output validation. These tests use a mock AI generator and do not prove the security of a real LLM. |

### Security limitations

- A clean Bandit or Semgrep report does not prove that the application is completely free of vulnerabilities.
- Trivy findings require individual review; the total number of findings does not necessarily represent the number of unique exploitable vulnerabilities.
- The ZAP informational alert should not automatically be treated as an exploitable vulnerability.
- AI security tests validate application-level controls around a mock generator, not the behavior of a production LLM.

### Remediation approach

1. Review and prioritize the findings reported by Trivy.
2. Update vulnerable or outdated packages and the Docker base image where appropriate.
3. Rebuild the Docker image and run Trivy again.
4. Review the ZAP alert and verify the application's security headers.
5. Rerun unit tests and all security checks after changes.
6. Compare the initial and final reports and document the results.

## Step 11 — Controlled Vulnerability Detection and Remediation

A controlled insecure coding pattern was introduced in
`security/demo/insecure_example.py` to validate SAST detection.

**Before remediation:**
- Semgrep detected 1 finding: `python-eval-usage` (ERROR).
- Bandit detected 1 finding: `B307` (MEDIUM severity, HIGH confidence).
- The vulnerable code used `eval(user_input)`.

**Remediation:**
- Replaced `eval()` with `ast.literal_eval()`.
- Added validation allowing only integer and floating-point values.
- Rejected malicious expressions and unsupported input types.

**After remediation:**
- Semgrep: 0 findings.
- Bandit: No issues identified.
- Functional checks passed.
- Full test suite: 20 passed.

Detailed evidence and before/after JSON reports are available in
`reports/step11/`. Screenshots are available in `screenshots/`.

The experiment was conducted in a controlled test environment and was
not deployed to production.
