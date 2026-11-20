def is_subsequence(sub: str, s: str) -> bool:
    """Indica si `sub` es subsecuencia de `s`."""
    it = iter(s)
    return all(c in it for c in sub)


def is_common_subsequence(sub: str, a: str, b: str) -> bool:
    """Indica si `sub` es subsecuencia de `a` y de `b`."""
    return is_subsequence(sub, a) and is_subsequence(sub, b)
