# LCS: recursiva, Hirschberg y programación dinámica

Tres algoritmos para la subsecuencia común más larga (LCS) de dos cadenas y un benchmark que compara su tiempo de CPU y su memoria pico.

| Versión | Archivo | Técnica |
|---|---|---|
| A | `lcs/recursive.py` | Recursión directa sin memorización |
| B | `lcs/hirschberg.py` | Divide y vencerás de Hirschberg |
| C | `lcs/dp.py` | Programación dinámica tabular |

## Requisitos

- Python ≥ 3.9 y `make` (incluidos en macOS y en la mayoría de distribuciones Linux). Los resultados de la memoria se obtuvieron con Python 3.9.6; desde Python 3.11 los marcos de recursión se gestionan de otra forma y `tracemalloc` puede no contabilizarlos, por lo que la memoria medida de la versión A podría diferir.
- Conexión a internet la primera vez, para instalar `matplotlib` en un entorno virtual local (`.venv`). Los algoritmos, los tests y el benchmark solo usan la librería estándar.

## Ejecución

```bash
make
```

Ejecuta, en orden, los tests, el benchmark y las gráficas. Tarda unos 3 minutos, casi todos en la versión A con n = 22.

Objetivos individuales:

```bash
make help    # lista y explica todos los comandos
make test    # tests unitarios
make bench   # benchmark → results/results.csv, results/tables.md, results/pairs.csv
make plots   # gráficas  → results/time.png, results/memory.png
make clean   # borra .venv, results/ y cachés
```

## Estructura

```
lcs/        algoritmos A, B y C
bench/      generación de parejas, medición y gráficas
tests/      tests unitarios (unittest)
results/    salidas generadas por make
```

## Salidas

`results/` contiene los resultados citados en la memoria (Python 3.9.6, Apple M5 Pro). Ejecutar `make` los regenera; los tiempos variarán ligeramente según la máquina.

- `results/results.csv`: una fila por (serie, n, algoritmo) con tiempo de CPU (s), memoria pico (KiB) y longitud de la LCS.
- `results/tables.md`: tablas resumen en Markdown.
- `results/pairs.csv`: parejas de cadenas usadas (generadas con semilla fija, reproducibles).
- `results/time.png`, `results/memory.png`: gráficas.
