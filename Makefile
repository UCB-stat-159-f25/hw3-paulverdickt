# --------- Makefile for STAT 159 HW3 (Paul Verdickt) ---------
# Usage:
#   make env          # create/update conda env from environment.yml (no activation)
#   make html         # local MyST build; prints where the site was written
#   make clean        # remove local build outputs

# Name of the conda/mamba environment to create/update
ENV_NAME ?= ligo-hw3

# Prefer mamba if available, else conda
CONDA := $(shell command -v mamba >/dev/null 2>&1 && echo mamba || echo conda)

.PHONY: env html clean

env:
	@test -f environment.yml || (echo "ERROR: environment.yml not found"; exit 1)
	@echo ">> Using $(CONDA) to create/update environment: $(ENV_NAME)"
	# Update if it exists; otherwise create it
	@$(CONDA) env update -n $(ENV_NAME) -f environment.yml --prune \
	|| $(CONDA) env create -n $(ENV_NAME) -f environment.yml
	@echo ">> Done. Environment $(ENV_NAME) created/updated (not activated)."

html:
	@echo ">> Building local MyST site…"
	# Some MyST versions use different output folders; keep it simple
	@myst build
	@echo ">> Build complete. Checking common output locations:"
	@( [ -d _site ] && echo "   - _site exists" ) || true
	@( [ -d .myst/site ] && echo "   - .myst/site exists" ) || true
	@( [ -d .myst/build ] && echo "   - .myst/build exists" ) || true
	@( [ -d _build/site ] && echo "   - _build/site exists" ) || true
	@( [ -d _build/html ] && echo "   - _build/html exists" ) || true
	@( [ -d _build ] && echo "   - _build exists" ) || true
	@echo ">> Open the local HTML from one of the folders above (for local viewing only)."

clean:
	@echo ">> Cleaning figures, audio, and build folders…"
	@rm -rf figures audio _site .myst _build
	@echo ">> Clean complete."
