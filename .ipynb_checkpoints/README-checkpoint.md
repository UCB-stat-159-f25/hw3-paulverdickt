# HW3 – LIGO Event Analysis

Author: Paul Verdickt  
Course: STAT 159 (Fall 2025)  
Assignment: Homework 3 – LIGO Event Tutorial  

---

## Launch the Project

Run the notebook live on Binder:  
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/UCB-stat-159-f25/hw3-paulverdickt/HEAD?labpath=LOSC_Event_tutorial.ipynb)

View the rendered MyST site:  
https://ucb-stat-159-f25.github.io/hw3-paulverdickt/

---

## Repository Contents
- `LOSC_Event_tutorial.ipynb` – Main LIGO event analysis notebook  
- `ligotools/` – Python package with helper functions (`readligo`, `utils`, etc.)  
- `tests/` – Unit tests for core functions  
- `myst.yml` – Configuration for MyST site structure  
- `Makefile` – Automates environment setup, build, and cleanup  
- `.github/workflows/` – GitHub Actions configuration for automated site deployment  
- `ai_documentation.txt` – Notes on AI assistance during development  

---

## Makefile Targets
- `make env` – Creates or updates the conda environment using `environment.yml`  
- `make html` – Builds the HTML version of the MyST site locally  
- `make clean` – Removes `_build`, `_site`, `figures/`, and `audio/` directories  

---

## Notes
- The MyST site is automatically deployed to GitHub Pages through a workflow.  
- Binder launches the live Jupyter environment directly from this repository.  
- Developed and maintained by Paul Verdickt.
