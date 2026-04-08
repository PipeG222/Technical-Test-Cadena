"""
prime_sum.py
------------
Returns the sum of all prime numbers contained in a list of integers.

Algorithm: Sieve of Eratosthenes — O(n log log n) time, O(n) space.
For lists with a small upper bound the sieve is pre-built once and then
reused for every lookup, keeping the per-element cost O(1).
"""

from __future__ import annotations

from typing import Iterable


# ---------------------------------------------------------------------------
# Core helpers
# ---------------------------------------------------------------------------

def _sieve(limit: int) -> list[bool]:
    """Return a boolean array where index i is True iff i is prime."""
    if limit < 2:
        return [False] * max(limit + 1, 2)

    is_prime: list[bool] = [True] * (limit + 1)
    is_prime[0] = is_prime[1] = False

    for i in range(2, int(limit**0.5) + 1):
        if is_prime[i]:
            is_prime[i * i :: i] = [False] * len(is_prime[i * i :: i])

    return is_prime


def is_prime(n: int) -> bool:
    """Deterministic primality check for a single integer (trial division).

    Used as a fallback for values outside the pre-built sieve range.
    Time complexity: O(√n).
    """
    if n < 2:
        return False
    if n < 4:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def sum_of_primes(numbers: Iterable[object]) -> int:
    """Return the sum of all prime numbers in *numbers*.

    Parameters
    ----------
    numbers:
        Any iterable of integers.  Non-integer items and negative values
        are rejected with informative exceptions.

    Returns
    -------
    int
        Sum of prime numbers found in the input.  Returns 0 when the
        iterable is empty or contains no primes.

    Raises
    ------
    TypeError
        If *numbers* is not iterable or contains non-integer elements.
    ValueError
        If any integer in *numbers* is negative (primes are positive by
        definition, but a negative value likely indicates a data problem
        worth surfacing rather than silently skipping).

    Examples
    --------
    >>> sum_of_primes([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
    17
    >>> sum_of_primes([])
    0
    >>> sum_of_primes([4, 6, 8, 9])
    0
    """
    if not hasattr(numbers, "__iter__"):
        raise TypeError(
            f"Expected an iterable, got {type(numbers).__name__!r}."
        )

    # Materialise once so we can run two passes (validate then compute).
    items: list[object] = list(numbers)

    # --- Validation pass ---------------------------------------------------
    for idx, item in enumerate(items):
        if not isinstance(item, (int, bool)):  # bool is a subclass of int
            raise TypeError(
                f"All elements must be integers; got {type(item).__name__!r} "
                f"at index {idx} (value={item!r})."
            )
        if isinstance(item, bool):
            raise TypeError(
                f"Boolean values are not valid integers for this function; "
                f"got {item!r} at index {idx}."
            )
        if item < 0:
            raise ValueError(
                f"Negative integers are not valid input; "
                f"got {item!r} at index {idx}."
            )

    if not items:
        return 0

    int_items: list[int] = items  # type: ignore[assignment]
    max_val: int = max(int_items)

    # --- Sieve pass (avoids repeated sqrt checks for large lists) ----------
    sieve = _sieve(max_val)

    total = 0
    for n in int_items:
        if n <= max_val and sieve[n]:
            total += n

    return total


# ---------------------------------------------------------------------------
# CLI entry point (optional smoke test)
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    sample = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    result = sum_of_primes(sample)
    print(f"Input : {sample}")
    print(f"Output: {result}")   # Expected: 17
