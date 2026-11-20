import csv
from collections import defaultdict
from pathlib import Path
from typing import Dict, List, Tuple

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.ticker import FuncFormatter, LogLocator, NullFormatter  # noqa: E402

RESULTS_DIR = Path(__file__).resolve().parent.parent / "results"
STYLE = {
    "A": ("#2a78d6", "o", "A · Recursiva"),
    "B": ("#eb6834", "s", "B · Hirschberg"),
    "C": ("#1baf7a", "^", "C · PD tabular"),
}
PANELS = {
    "small": ("Serie pequeña (A, B y C)", "linear"),
    "large": ("Serie grande (B y C)", "log"),
}
METRICS = {
    "time.png": ("cpu_s", 1000.0, "Tiempo de CPU (ms, escala log)"),
    "memory.png": ("peak_kib", 1.0, "Memoria pico (KiB, escala log)"),
}

Points = Dict[Tuple[str, str], List[Dict[str, float]]]


def load_results(path: Path) -> Points:
    """Agrupa las filas del CSV por (serie, algoritmo), ordenadas por n."""
    data: Points = defaultdict(list)
    with path.open() as f:
        for row in csv.DictReader(f):
            data[(row["series"], row["algorithm"])].append(
                {"n": int(row["n"]), "cpu_s": float(row["cpu_s"]), "peak_kib": float(row["peak_kib"])}
            )
    for points in data.values():
        points.sort(key=lambda p: p["n"])
    return data


def plot_metric(data: Points, field: str, scale: float, ylabel: str, path: Path) -> None:
    """Dos paneles (serie pequeña y grande) de una métrica frente a n."""
    fig, axes = plt.subplots(1, 2, figsize=(10, 4))
    for ax, (series, (title, xscale)) in zip(axes, PANELS.items()):
        panel_ns = sorted({p["n"] for name in STYLE for p in data.get((series, name), [])})
        if not panel_ns:
            ax.set_visible(False)
            continue
        for name, (color, marker, label) in STYLE.items():
            points = data.get((series, name))
            if not points:
                continue
            ns = [p["n"] for p in points]
            ys = [p[field] * scale for p in points]
            ax.plot(ns, ys, color=color, marker=marker, markersize=7, linewidth=2, label=label)
            ax.annotate(name, (ns[-1], ys[-1]), xytext=(8, 0), textcoords="offset points",
                        va="center", fontsize=10, color="#333333")
        ax.set_title(title, fontsize=11)
        ax.set_xscale(xscale)
        ax.set_yscale("log")
        ax.set_xticks(panel_ns)
        ax.xaxis.set_major_formatter(FuncFormatter(lambda v, _: f"{v:g}"))
        ax.xaxis.set_minor_formatter(NullFormatter())
        low, high = ax.get_ylim()
        if high / low < 100:
            ax.yaxis.set_major_locator(LogLocator(base=10, subs=(1.0, 2.0, 5.0)))
            ax.yaxis.set_major_formatter(FuncFormatter(lambda v, _: f"{v:g}"))
            ax.yaxis.set_minor_formatter(NullFormatter())
        ax.set_xlabel("n = m (símbolos)" + (", escala log" if xscale == "log" else ""))
        ax.set_ylabel(ylabel)
        ax.grid(True, which="major", color="#e6e6e6", linewidth=0.8)
        ax.spines[["top", "right"]].set_visible(False)
        ax.legend(frameon=False, fontsize=9)
    fig.tight_layout()
    fig.savefig(path, dpi=200)
    plt.close(fig)


def main() -> None:
    data = load_results(RESULTS_DIR / "results.csv")
    for filename, (field, scale, ylabel) in METRICS.items():
        plot_metric(data, field, scale, ylabel, RESULTS_DIR / filename)
        print(f"Generada {RESULTS_DIR / filename}")


if __name__ == "__main__":
    main()
