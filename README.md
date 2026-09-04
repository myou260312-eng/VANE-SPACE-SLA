# VANE-SPACE-SLA (v2.0)

Deterministic Multi-Gate Telemetry Validation & Strict Prompt Grounding — v2.0 (demo / test harness)

This repository is a self-contained, testable demonstration of multi-gate telemetry checks and strict prompt grounding. External AI and infra integrations (watsonx, Milvus, FAISS, Redis, PostgreSQL, etc.) are intentionally simulated so the project can run without paid services and remain fully testable in CI.

This v2.0 release includes:
- Deterministic, unit-testable RAG orchestration stub (rag_pipeline.py)
- Strict prompt builder (Python + JavaScript) that reads config from environment variables
- Simulated telemetry validator (vane_space_init.py) with deterministic seeding for tests
- Voice orchestrator demo (extensions-core/voice_agents.py) using environment configuration and structured logging
- Pytest test suite and GitHub Actions CI to enforce tests and coverage
- Sanitized public HTML pages: no personal emails, IDs, or account secrets are published

Quick start

```bash
git clone https://github.com/myou260312-eng/VANE-SPACE-SLA.git
cd VANE-SPACE-SLA
python -m venv .venv
source .venv/bin/activate    # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# run tests
pytest --cov=. --cov-report=term
# run telemetry demo
python vane_space_init.py
# run a RAG demo cycle from Python REPL
python - <<'PY'
from rag_pipeline import run_rag_cycle
print(run_rag_cycle('Check server 01 status', ['Server 01: CPU 42.8% status SECURE'], grounding_strength='strict', seed=42))
PY
```

Environment configuration

This project uses environment variables for anything that would otherwise be a secret or tenant-specific identifier. Copy `.env.example` to `.env` and edit values as needed for local testing. Public defaults are safe placeholders.

Key variables in `.env.example`:
- OUR_IBM_SAAS_ACCOUNT_ID
- OUR_EU_EXPERT_ID
- OUR_CONTRACT_RESELLER_ID
- OUR_CONTRACT_SERVICE_BPA
- OUR_CUSTOMER_INDEX
- OUR_EU_CELLAR_DOC_ID
- OUR_EU_RSS_HASH

Project structure (important files)

- config.py — central config object reading env vars and defining thresholds
- rag_pipeline.py — deterministic RAG orchestration stub (retrieval, prompt-building, inference stub, grounding score)
- strict_prompt_builder.py — Python strict prompt builder (also mirrored in strict_prompt_builder.js for browser demos)
- vane_space_init.py — simulated multi-gate telemetry validator and demo CLI
- extensions-core/voice_agents.py — demo voice orchestrator using env-driven config and logging
- tests/ — pytest suite covering prompt builder, telemetry, RAG flow, and logging
- .github/workflows/ci.yml — CI workflow running pytest + coverage on push and PRs
- .env.example — example env vars (do NOT commit real credentials)
- README.md, CONTRIBUTING.md, SECURITY.md — docs and contributor guidance

Notes about scope and safety

- This repository is a demo. The RAG pipeline and telemetry modules are intentionally self-contained stubs so they can be run in CI without external dependencies or paid services.
- No real credentials, personal emails, or account IDs are included in the public repo. All sensitive values should be provided via environment variables or a secure secret manager in production.
- HTML pages are sanitized and intentionally omit PII. If you need to present public identifiers, add them locally or via environment-driven templating.

Testing and CI

- Unit tests: pytest
- Coverage: pytest-cov (CI enforces a minimum coverage threshold — configurable in `.github/workflows/ci.yml`)
- To run tests locally: `pytest --cov=. --cov-report=term`

Contributing

- Please open issues or pull requests on GitHub. Keep changes small and include tests for new functionality.
- Do not commit credentials or personal data. Use `.env` and `.env.example` to share non-sensitive defaults.

License

MIT — see LICENSE file.

Contact / Support

- For maintenance, open an issue in this repository: https://github.com/myou260312-eng/VANE-SPACE-SLA/issues

---

This repository was prepared as a sanitized, testable demonstration for VANE-SPACE-SLA v2.0. If you want help connecting real vector stores or an LLM provider, open an issue and I can propose an integration plan and implementation steps.