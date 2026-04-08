using System;
using Xunit;
using PalindromeApp;

namespace PalindromeApp.Tests;

public class PalindromeCheckerTests
{
    // ── Happy path ─────────────────────────────────────────────────────────

    [Theory]
    [InlineData("A man a plan a canal Panama", true)]   // spec example
    [InlineData("racecar",                             true)]
    [InlineData("Was it a car or a cat I saw",         true)]
    [InlineData("No lemon no melon",                   true)]
    [InlineData("Madam",                               true)]
    [InlineData("hello",                               false)]
    [InlineData("world",                               false)]
    [InlineData("Not a palindrome",                    false)]
    public void IsPalindrome_ReturnsExpectedResult(string input, bool expected)
    {
        Assert.Equal(expected, PalindromeChecker.IsPalindrome(input));
    }

    [Fact]
    public void IsPalindrome_SingleCharacter_IsTrue()
    {
        Assert.True(PalindromeChecker.IsPalindrome("a"));
    }

    [Fact]
    public void IsPalindrome_SingleDigit_IsTrue()
    {
        Assert.True(PalindromeChecker.IsPalindrome("1"));
    }

    [Fact]
    public void IsPalindrome_PunctuationOnly_ReturnsFalse()
    {
        // No alphanumeric content → treated as non-palindrome.
        Assert.False(PalindromeChecker.IsPalindrome("!!! ???"));
    }

    [Fact]
    public void IsPalindrome_EmptyString_ReturnsFalse()
    {
        Assert.False(PalindromeChecker.IsPalindrome(string.Empty));
    }

    [Fact]
    public void IsPalindrome_WhitespaceOnly_ReturnsFalse()
    {
        Assert.False(PalindromeChecker.IsPalindrome("   "));
    }

    [Fact]
    public void IsPalindrome_NumericPalindrome_IsTrue()
    {
        Assert.True(PalindromeChecker.IsPalindrome("12321"));
    }

    [Fact]
    public void IsPalindrome_MixedAlphanumeric_IsTrue()
    {
        Assert.True(PalindromeChecker.IsPalindrome("A1B2B1A"));  // a1b2b1a
    }

    // ── Large input ────────────────────────────────────────────────────────

    [Fact]
    public void IsPalindrome_LargeEvenPalindrome_IsTrue()
    {
        // Build "aaa...aaa" — trivially a palindrome.
        string large = new string('a', 1_000_000);
        Assert.True(PalindromeChecker.IsPalindrome(large));
    }

    [Fact]
    public void IsPalindrome_LargeNonPalindrome_IsFalse()
    {
        string large = new string('a', 999_999) + "b";
        Assert.False(PalindromeChecker.IsPalindrome(large));
    }

    // ── Error handling ──────────────────────────────────────────────────────

    [Fact]
    public void IsPalindrome_NullInput_ThrowsArgumentNullException()
    {
        Assert.Throws<ArgumentNullException>(() =>
            PalindromeChecker.IsPalindrome(null!));
    }

    [Fact]
    public void IsPalindrome_ExceedsMaxLength_ThrowsArgumentException()
    {
        string tooLong = new string('x', PalindromeChecker.MaxInputLength + 1);
        var ex = Assert.Throws<ArgumentException>(() =>
            PalindromeChecker.IsPalindrome(tooLong));
        Assert.Contains("exceeds", ex.Message, StringComparison.OrdinalIgnoreCase);
    }
}
