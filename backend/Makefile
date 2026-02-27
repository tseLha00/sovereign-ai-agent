run:
	uvicorn sai_backend.main:app --reload --port 8000

run-real:
	LLM_BACKEND=llamacpp uvicorn sai_backend.main:app --reload --port 8000

test:
	LLM_BACKEND=mock pytest -q

perf:
	LLM_BACKEND=mock python qa/perf/run_perf.py --requests 100 --concurrency 10