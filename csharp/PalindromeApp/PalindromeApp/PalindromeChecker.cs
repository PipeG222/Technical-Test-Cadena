using System;
using System.Runtime.CompilerServices;

namespace PalindromeApp;

/// <summary>
/// Provides a highly efficient palindrome check that ignores spaces,
/// punctuation, and letter case.
/// </summary>
/// <remarks>
/// Implementation uses a two-pointer approach over a <see cref="ReadOnlySpan{T}"/>
/// so no additional heap allocation is needed beyond the single char-normalised
/// span built once from the input.  Overall complexity: O(n) time, O(n) space.
/// </remarks>
public static class PalindromeChecker
{
    /// <summary>
    /// Determines whether <paramref name="input"/> is a palindrome after
    /// stripping non-alphanumeric characters and normalising to lower-case.
    /// </summary>
    /// <param name="input">The string to evaluate.</param>
    /// <returns>
    /// <see langword="true"/> when the cleaned string reads the same forwards
    /// and backwards; <see langword="false"/> otherwise.  An empty or
    /// whitespace-only string is considered <em>not</em> a palindrome.
    /// </returns>
    /// <exception cref="ArgumentNullException">
    /// Thrown when <paramref name="input"/> is <see langword="null"/>.
    /// </exception>
    /// <exception cref="ArgumentException">
    /// Thrown when <paramref name="input"/> exceeds the maximum safe length
    /// (<see cref="MaxInputLength"/>).
    /// </exception>
    public static bool IsPalindrome(string input)
    {
        ArgumentNullException.ThrowIfNull(input, nameof(input));

        if (input.Length > MaxInputLength)
            throw new ArgumentException(
                $"Input length ({input.Length:N0}) exceeds the maximum allowed " +
                $"value of {MaxInputLength:N0} characters.",
                nameof(input));

        // --- Build a normalised char array (alphanumeric, lower-case) --------
        // Allocate on the stack for small strings; heap for large ones.
        Span<char> buffer = input.Length <= 256
            ? stackalloc char[input.Length]
            : new char[input.Length];

        int len = 0;
        foreach (char c in input)
        {
            if (char.IsLetterOrDigit(c))
                buffer[len++] = char.ToLowerInvariant(c);
        }

        if (len == 0)
            return false;   // No alphanumeric content — treat as non-palindrome.

        ReadOnlySpan<char> cleaned = buffer[..len];

        // --- Two-pointer check -----------------------------------------------
        int left  = 0;
        int right = len - 1;

        while (left < right)
        {
            if (cleaned[left] != cleaned[right])
                return false;

            left++;
            right--;
        }

        return true;
    }

    /// <summary>Maximum input length accepted (10 MB of UTF-16 chars ≈ 5 MB text).</summary>
    public const int MaxInputLength = 5_000_000;
}
