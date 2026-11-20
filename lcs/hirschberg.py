from typing import List


def lcs_hirschberg(a: str, b: str) -> str:
    """Versión B: divide y vencerás de Hirschberg, O(n·m) en tiempo y O(n+m) en espacio."""
    chars: List[str] = []
    _solve(a, b, 0, len(a), 0, len(b), chars)
    return "".join(chars)


def _solve(a: str, b: str, a_lo: int, a_hi: int, b_lo: int, b_hi: int, out: List[str]) -> None:
    """Añade a `out` una LCS de a[a_lo:a_hi] y b[b_lo:b_hi]."""
    if a_lo == a_hi or b_lo == b_hi:
        return
    if a_hi - a_lo == 1:
        if b.find(a[a_lo], b_lo, b_hi) != -1:
            out.append(a[a_lo])
        return
    mid = (a_lo + a_hi) // 2
    split = _best_split(a, b, a_lo, mid, a_hi, b_lo, b_hi)
    _solve(a, b, a_lo, mid, b_lo, split, out)
    _solve(a, b, mid, a_hi, split, b_hi, out)


def _best_split(a: str, b: str, a_lo: int, mid: int, a_hi: int, b_lo: int, b_hi: int) -> int:
    """Posición de b donde cortar; las filas se liberan al volver, antes de recursar."""
    forward = _forward_scores(a, b, a_lo, mid, b_lo, b_hi)
    backward = _backward_scores(a, b, mid, a_hi, b_lo, b_hi)
    k = max(range(b_hi - b_lo + 1), key=lambda k: forward[k] + backward[k])
    return b_lo + k


def _forward_scores(a: str, b: str, a_lo: int, a_hi: int, b_lo: int, b_hi: int) -> List[int]:
    """scores[k] = |LCS(a[a_lo:a_hi], b[b_lo:b_lo+k])|, calculado con dos filas."""
    width = b_hi - b_lo
    prev = [0] * (width + 1)
    for i in range(a_lo, a_hi):
        curr = [0] * (width + 1)
        ch = a[i]
        for k in range(1, width + 1):
            if ch == b[b_lo + k - 1]:
                curr[k] = prev[k - 1] + 1
            else:
                curr[k] = max(prev[k], curr[k - 1])
        prev = curr
    return prev


def _backward_scores(a: str, b: str, a_lo: int, a_hi: int, b_lo: int, b_hi: int) -> List[int]:
    """scores[k] = |LCS(a[a_lo:a_hi], b[b_lo+k:b_hi])|, recorriendo ambas cadenas al revés."""
    width = b_hi - b_lo
    prev = [0] * (width + 1)
    for i in range(a_hi - 1, a_lo - 1, -1):
        curr = [0] * (width + 1)
        ch = a[i]
        for k in range(width - 1, -1, -1):
            if ch == b[b_lo + k]:
                curr[k] = prev[k + 1] + 1
            else:
                curr[k] = max(prev[k], curr[k + 1])
        prev = curr
    return prev
