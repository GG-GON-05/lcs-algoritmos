def lcs_recursive(a: str, b: str) -> str:
    """Versión A: recursión directa sin memorización, O(2^(n+m)) en el peor caso."""

    def solve(i: int, j: int) -> str:
        if i == 0 or j == 0:
            return ""
        if a[i - 1] == b[j - 1]:
            return solve(i - 1, j - 1) + a[i - 1]
        skip_a = solve(i - 1, j)
        skip_b = solve(i, j - 1)
        return skip_a if len(skip_a) >= len(skip_b) else skip_b

    return solve(len(a), len(b))
