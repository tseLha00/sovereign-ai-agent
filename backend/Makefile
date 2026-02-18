run:
	uvicorn sai_backend.main:app --reload --port 8000

test:
	pytest -q

perf:
	python qa/perf/run_perf.py --requests 100 --concurrency 10