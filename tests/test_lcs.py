import random
import unittest

from lcs import ALGORITHMS
from lcs.check import is_subsequence
from lcs.dp import lcs_dp

KNOWN_CASES = [
    ("", "", 0),
    ("", "ABC", 0),
    ("ABC", "", 0),
    ("A", "A", 1),
    ("A", "B", 0),
    ("ABC", "ABC", 3),
    ("ABC", "DEF", 0),
    ("ABCBDAB", "BDCABA", 4),
    ("AGGTAB", "GXTXAYB", 4),
    ("ACGTACGT", "TGCATGCA", 3),
]


class TestLCS(unittest.TestCase):
    def assert_valid_lcs(self, result: str, a: str, b: str, expected_len: int) -> None:
        self.assertEqual(len(result), expected_len)
        self.assertTrue(is_subsequence(result, a), f"{result!r} no es subsecuencia de {a!r}")
        self.assertTrue(is_subsequence(result, b), f"{result!r} no es subsecuencia de {b!r}")

    def test_known_cases(self):
        for name, algorithm in ALGORITHMS.items():
            for a, b, expected_len in KNOWN_CASES:
                with self.subTest(algorithm=name, a=a, b=b):
                    self.assert_valid_lcs(algorithm(a, b), a, b, expected_len)

    def test_symmetric_length(self):
        for name, algorithm in ALGORITHMS.items():
            for a, b, _ in KNOWN_CASES:
                with self.subTest(algorithm=name, a=a, b=b):
                    self.assertEqual(len(algorithm(a, b)), len(algorithm(b, a)))

    def test_random_small_pairs_match_reference(self):
        rng = random.Random(2024)
        for _ in range(50):
            a = random_string(rng, rng.randint(0, 10))
            b = random_string(rng, rng.randint(0, 10))
            expected_len = len(lcs_dp(a, b))
            for name, algorithm in ALGORITHMS.items():
                with self.subTest(algorithm=name, a=a, b=b):
                    self.assert_valid_lcs(algorithm(a, b), a, b, expected_len)

    def test_large_pairs_match_reference(self):
        rng = random.Random(7)
        polynomial = {name: f for name, f in ALGORITHMS.items() if name != "A"}
        for _ in range(5):
            a = random_string(rng, 300)
            b = random_string(rng, rng.randint(150, 300))
            expected_len = len(lcs_dp(a, b))
            for name, algorithm in polynomial.items():
                with self.subTest(algorithm=name, len_a=len(a), len_b=len(b)):
                    self.assert_valid_lcs(algorithm(a, b), a, b, expected_len)


def random_string(rng: random.Random, length: int) -> str:
    """Cadena aleatoria sobre el alfabeto ACGT."""
    return "".join(rng.choice("ACGT") for _ in range(length))


if __name__ == "__main__":
    unittest.main()
