# sec-filings-ai-analyst

\# SEC Filings AI Analyst

Ask questions about public-company SEC filings and get answers grounded in the source documents, with citations.



\## Architecture (planned)

EDGAR ingestion → section-aware chunking → hybrid retrieval (vector + BM25) → tool-using agent → eval suite → FastAPI + Docker deployment



\## Roadmap



\### MVP (target: Dec 15, 2026)

\- \[ ] EDGAR ingestion with rate limiting and retries

\- \[ ] Section-aware chunking + embeddings

\- \[ ] Hybrid retrieval (vector + BM25)

\- \[ ] Research agent with tools (LangGraph + Claude)

\- \[ ] Eval suite: retrieval recall, citation accuracy, LLM-as-judge

\- \[ ] FastAPI + Docker, deployed



\### v2

\- \[ ] Multi-agent verifier loop (citation checking)

\- \[ ] Text2SQL over XBRL financial data

\- \[ ] MCP server exposing analyst tools

\- \[ ] Evals in CI (GitHub Actions) + tracing

\- \[ ] Guardrails + reusable `rag-eval-kit` package

\- \[ ] Web UI, demo video, write-up



\## Status

🚧 In active development

