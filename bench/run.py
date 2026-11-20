import csv
import gc
import statistics
import time
import tracemalloc
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Callable, Dict, List, Tuple

from bench.generate import random_pair
from lcs import ALGORITHMS
from lcs.check import is_common_subsequence

RESULTS_DIR = Path(__file__).resolve().parent.parent / "results"
REPEATS = 3
LONG_RUN_S = 5.0
SERIES = {
    "small": ((6, 10, 14, 18, 22), ("A", "B", "C")),
    "large": ((100, 250, 500, 1000, 2000), ("B", "C")),
}

LcsFunction = Callable[[str, str], str]


@dataclass
class Measurement:
    series: str
    n: int
    algorithm: str
    cpu_s: float
    peak_kib: float
    lcs_len: int


def measure_cpu(algorithm: LcsFunction, a: str, b: str) -> Tuple[float, str]:
    """Mediana del tiempo de CPU de REPEATS ejecuciones (una sola si supera LONG_RUN_S)."""
    times: List[float] = []
    while len(times) < REPEATS:
        gc.collect()
        start = time.process_time()
        result = algorithm(a, b)
        times.append(time.process_time() - start)
        if times[0] > LONG_RUN_S:
            break
    return statistics.median(times), result


def measure_peak_kib(algorithm: LcsFunction, a: str, b: str) -> float:
    """Pico de memoria reservada durante una ejecución, en KiB."""
    gc.collect()
    tracemalloc.start()
    algorithm(a, b)
    _, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    return peak / 1024


def run_series(series: str, sizes: Tuple[int, ...], names: Tuple[str, ...]) -> List[Measurement]:
    """Mide cada algoritmo sobre cada tamaño y valida que todos devuelven una LCS válida."""
    rows = []
    for n in sizes:
        a, b = random_pair(n)
        lengths = set()
        for name in names:
            cpu_s, result = measure_cpu(ALGORITHMS[name], a, b)
            if not is_common_subsequence(result, a, b):
                raise RuntimeError(f"{name} devolvió una cadena que no es subsecuencia común (n={n})")
            peak_kib = measure_peak_kib(ALGORITHMS[name], a, b)
            lengths.add(len(result))
            rows.append(Measurement(series, n, name, cpu_s, peak_kib, len(result)))
            print(f"[{series}] n={n:>5} {name}: {cpu_s:9.4f} s  {peak_kib:11.1f} KiB", flush=True)
        if len(lengths) != 1:
            raise RuntimeError(f"Longitudes de LCS distintas para n={n}: {lengths}")
    return rows


def write_csv(rows: List[Measurement], path: Path) -> None:
    with path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(asdict(rows[0])))
        writer.writeheader()
        writer.writerows(asdict(r) for r in rows)


def write_pairs(path: Path) -> None:
    """Guarda las parejas de entrada usadas (dataset reproducible)."""
    with path.open("w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["series", "n", "a", "b"])
        for series, (sizes, _) in SERIES.items():
            for n in sizes:
                writer.writerow([series, n, *random_pair(n)])


def format_number(value: float) -> str:
    if value >= 100:
        return f"{value:,.0f}".replace(",", " ")
    if value >= 1:
        return f"{value:.2f}"
    return f"{value:.3f}"


def markdown_table(rows: List[Measurement], names: Tuple[str, ...]) -> str:
    """Tabla con tiempo (ms) y memoria pico (KiB) por tamaño; '—' si no se ejecutó."""
    by_key: Dict[Tuple[int, str], Measurement] = {(r.n, r.algorithm): r for r in rows}
    sizes = sorted({r.n for r in rows})
    all_names = ("A", "B", "C")
    header = (["n", "\\|LCS\\|"]
              + [f"CPU {x} (ms)" for x in all_names]
              + [f"Mem {x} (KiB)" for x in all_names])
    lines = ["| " + " | ".join(header) + " |", "|" + "---|" * len(header)]
    for n in sizes:
        lcs_len = by_key[(n, names[0])].lcs_len
        cpu = [format_number(by_key[(n, x)].cpu_s * 1000) if x in names else "—" for x in all_names]
        mem = [format_number(by_key[(n, x)].peak_kib) if x in names else "—" for x in all_names]
        lines.append("| " + " | ".join([str(n), str(lcs_len)] + cpu + mem) + " |")
    return "\n".join(lines)


def write_tables(rows: List[Measurement], path: Path) -> str:
    titles = {"small": "Serie pequeña (A, B y C)", "large": "Serie grande (B y C)"}
    sections = []
    for series, (_, names) in SERIES.items():
        series_rows = [r for r in rows if r.series == series]
        sections.append(f"### {titles[series]}\n\n{markdown_table(series_rows, names)}\n")
    text = "\n".join(sections)
    path.write_text(text)
    return text


def main() -> None:
    RESULTS_DIR.mkdir(exist_ok=True)
    rows = []
    for series, (sizes, names) in SERIES.items():
        rows.extend(run_series(series, sizes, names))
    write_csv(rows, RESULTS_DIR / "results.csv")
    write_pairs(RESULTS_DIR / "pairs.csv")
    print("\n" + write_tables(rows, RESULTS_DIR / "tables.md"))


if __name__ == "__main__":
    main()
