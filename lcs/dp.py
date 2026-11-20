from typing import List


def lcs_dp(a: str, b: str) -> str:
    """Versión C: programación dinámica tabular, Θ(n·m) en tiempo y espacio."""
    n, m = len(a), len(b)
    table = [[0] * (m + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        prev, row = table[i - 1], table[i]
        for j in range(1, m + 1):
            if a[i - 1] == b[j - 1]:
                row[j] = prev[j - 1] + 1
            else:
                row[j] = max(prev[j], row[j - 1])
    return _backtrack(table, a, b)


def _backtrack(table: List[List[int]], a: str, b: str) -> str:
    """Reconstruye una LCS recorriendo la tabla desde (n, m) hasta el origen."""
    i, j = len(a), len(b)
    chars = []
    while i > 0 and j > 0:
        if a[i - 1] == b[j - 1]:
            chars.append(a[i - 1])
            i -= 1
            j -= 1
        elif table[i - 1][j] >= table[i][j - 1]:
            i -= 1
        else:
            j -= 1
    return "".join(reversed(chars))
