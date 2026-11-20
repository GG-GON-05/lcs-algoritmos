"""Implementaciones de la subsecuencia común más larga (LCS)."""

from lcs.dp import lcs_dp
from lcs.hirschberg import lcs_hirschberg
from lcs.recursive import lcs_recursive

ALGORITHMS = {
    "A": lcs_recursive,
    "B": lcs_hirschberg,
    "C": lcs_dp,
}
