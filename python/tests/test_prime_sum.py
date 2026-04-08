"""
Unit tests for prime_sum.py
----------------------------
Run with:  pytest python/tests/ -v
"""

import pytest

from python.prime_sum import is_prime, sum_of_primes


# ---------------------------------------------------------------------------
# is_prime
# ---------------------------------------------------------------------------

class TestIsPrime:
    def test_zero_is_not_prime(self):
        assert is_prime(0) is False

    def test_one_is_not_prime(self):
        assert is_prime(1) is False

    def test_two_is_prime(self):
        assert is_prime(2) is True

    def test_three_is_prime(self):
        assert is_prime(3) is True

    def test_four_is_not_prime(self):
        assert is_prime(4) is False

    def test_large_prime(self):
        assert is_prime(7_919) is True   # 1000th prime

    def test_large_composite(self):
        assert is_prime(7_920) is False


# ---------------------------------------------------------------------------
# sum_of_primes — happy path
# ---------------------------------------------------------------------------

class TestSumOfPrimesHappyPath:
    def test_example_from_spec(self):
        assert sum_of_primes([1, 2, 3, 4, 5, 6, 7, 8, 9, 10]) == 17

    def test_empty_list(self):
        assert sum_of_primes([]) == 0

    def test_no_primes(self):
        assert sum_of_primes([0, 1, 4, 6, 8, 9]) == 0

    def test_all_primes(self):
        assert sum_of_primes([2, 3, 5, 7]) == 17

    def test_single_prime(self):
        assert sum_of_primes([7]) == 7

    def test_single_non_prime(self):
        assert sum_of_primes([1]) == 0

    def test_duplicate_primes(self):
        # Each occurrence is counted individually.
        assert sum_of_primes([2, 2, 3, 3]) == 10

    def test_generator_input(self):
        # Function accepts any iterable, not just lists.
        assert sum_of_primes(x for x in range(1, 11)) == 17

    def test_large_list(self):
        # 10 000 numbers; result must be computed without timeout.
        numbers = list(range(1, 10_001))
        result = sum_of_primes(numbers)
        # Known sum of primes up to 10 000 is 5 736 396.
        assert result == 5_736_396

    def test_list_with_zero(self):
        assert sum_of_primes([0, 2, 3]) == 5


# ---------------------------------------------------------------------------
# sum_of_primes — error handling
# ---------------------------------------------------------------------------

class TestSumOfPrimesErrors:
    def test_non_iterable_raises_type_error(self):
        with pytest.raises(TypeError, match="iterable"):
            sum_of_primes(42)  # type: ignore[arg-type]

    def test_float_element_raises_type_error(self):
        with pytest.raises(TypeError, match="integers"):
            sum_of_primes([1, 2.0, 3])

    def test_string_element_raises_type_error(self):
        with pytest.raises(TypeError, match="integers"):
            sum_of_primes([1, "two", 3])

    def test_none_element_raises_type_error(self):
        with pytest.raises(TypeError, match="integers"):
            sum_of_primes([1, None, 3])

    def test_bool_element_raises_type_error(self):
        # True/False are technically int subclasses but semantically wrong.
        with pytest.raises(TypeError, match="Boolean"):
            sum_of_primes([True, False, 2])

    def test_negative_integer_raises_value_error(self):
        with pytest.raises(ValueError, match="Negative"):
            sum_of_primes([-1, 2, 3])

    def test_mixed_invalid_types_raises_on_first(self):
        # Should raise on the first bad element encountered.
        with pytest.raises(TypeError):
            sum_of_primes([1, "bad", -1])
