.PHONY: help setup validate analyze check-analyzer check-parity check demo clean

help:
	@echo "patterns-of-choice — common tasks"
	@echo ""
	@echo "  make setup           create .venv and install validator dependencies"
	@echo "  make validate        run scripts/validate.py against the corpus"
	@echo "  make analyze         run scripts/analyze.py on synthetic fixtures"
	@echo "  make check-analyzer  run analyzer regression gate (asserts thresholds)"
	@echo "  make check-parity    assert the JS projection and Python analyzer agree"
	@echo "  make check           run validate + both analyzer gates"
	@echo "  make demo            open the static HTML demo in the default browser"
	@echo "  make clean           remove .venv and Python bytecode caches"
	@echo ""
	@echo "First-time setup: make setup && make validate"

setup:
	python3 -m venv .venv
	./.venv/bin/pip install -q -r scripts/requirements.txt
	@echo "Setup complete. Try: make validate"

validate:
	@./.venv/bin/python scripts/validate.py

check-analyzer:
	@./.venv/bin/python scripts/check_analyzer_thresholds.py

check-parity:
	@./.venv/bin/python scripts/check_impl_parity.py

check: validate check-analyzer check-parity
	@echo "All checks passed."

analyze:
	@./.venv/bin/python scripts/analyze.py \
	  --log analysis/fixtures/sample-session-log.json \
	  --probes analysis/fixtures/sample-probe-responses.json \
	  --card-sort analysis/fixtures/sample-card-sort.json \
	  --pairwise analysis/fixtures/sample-pairwise.json \
	  --hexaco analysis/fixtures/sample-hexaco.json \
	  --informant-hexaco analysis/fixtures/sample-informant-hexaco.json \
	  --big5 analysis/fixtures/sample-big5.json \
	  --log-window-b analysis/fixtures/sample-session-log-window-b.json \
	  --probes-window-b analysis/fixtures/sample-probe-responses-window-b.json

demo:
	@open demo/first-session.html 2>/dev/null || xdg-open demo/first-session.html 2>/dev/null || \
	  echo "Open demo/first-session.html in a browser"

clean:
	rm -rf .venv
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	@echo "Cleaned: .venv removed, __pycache__ removed"
