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
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
python run.py                   # http://localhost:5000/health
curl -X POST localhost:5000/api/chat -H "Content-Type: application/json" -d '{"message":"How do I budget?"}'
```

## Tests
```bash
pytest -v
python -m security.ai_report    # writes reports/ai-security-report.md
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
| Tool | Purpose | Report |
| --- | --- | --- |
| Bandit | Python SAST | bandit-report.json |
| Semgrep | Custom rule SAST (`security/semgrep/rules.yml`) | semgrep-report.json |
| pip-audit | Dependency CVEs | dependency-report.json |
| Trivy | Docker image CVEs | trivy-report.json |
| OWASP ZAP | DAST baseline | zap-report.json |
| AI tests | Prompt injection etc. (mock) | ai-security-report.md |

## Accessing reports
GitHub -> Actions -> select run -> Artifacts -> `vulnfinbot-security-reports`.

## Limitations
The AI responses are a mock. The AI tests check application-level controls only; they do not prove
that a real LLM resists prompt injection.

## Findings and remediation
Fill in after your pipeline run (see technical report table).
