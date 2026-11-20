import random
from typing import Tuple

ALPHABET = "ACGT"
BASE_SEED = 2025


def random_pair(n: int) -> Tuple[str, str]:
    """Pareja reproducible de cadenas aleatorias de longitud n sobre ACGT."""
    rng = random.Random(BASE_SEED + n)
    a = "".join(rng.choice(ALPHABET) for _ in range(n))
    b = "".join(rng.choice(ALPHABET) for _ in range(n))
    return a, b
