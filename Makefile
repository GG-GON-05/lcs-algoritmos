PYTHON  := python3
VENV    := .venv
VENV_PY := $(VENV)/bin/python
RESULTS := results/results.csv

.PHONY: all help test bench plots clean
.NOTPARALLEL:

all: test bench plots

help:
	@echo "Uso: make [objetivo]"
	@echo ""
	@echo "  make         Ejecuta todo: tests, benchmark y gráficas (≈ 3 min)"
	@echo "  make help    Muestra esta ayuda"
	@echo "  make test    Ejecuta los tests unitarios de las versiones A, B y C"
	@echo "  make bench   Mide CPU y memoria → results/results.csv, tables.md, pairs.csv"
	@echo "  make plots   Genera las gráficas → results/time.png, memory.png"
	@echo "               (crea .venv e instala matplotlib la primera vez)"
	@echo "  make clean   Elimina .venv, results/ y las cachés de Python"

test:
	$(PYTHON) -m unittest discover -s tests -v

bench:
	$(PYTHON) -m bench.run

$(RESULTS):
	$(PYTHON) -m bench.run

plots: $(VENV)/.installed $(RESULTS)
	$(VENV_PY) -m bench.plots

$(VENV)/.installed: requirements.txt
	$(PYTHON) -m venv $(VENV)
	$(VENV_PY) -m pip install --quiet --upgrade pip
	$(VENV_PY) -m pip install --quiet -r requirements.txt
	touch $@

clean:
	rm -rf $(VENV) results
	find . -name __pycache__ -type d -prune -exec rm -rf {} +
