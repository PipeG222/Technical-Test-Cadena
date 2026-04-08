using System;
using PalindromeApp;

// ── Entry point ─────────────────────────────────────────────────────────────

Console.WriteLine("=== Palindrome Checker ===");
Console.WriteLine($"(Max input length: {PalindromeChecker.MaxInputLength:N0} characters)");
Console.WriteLine();

while (true)
{
    Console.Write("Enter a string (or 'exit' to quit): ");
    string? line = Console.ReadLine();

    if (line is null || line.Equals("exit", StringComparison.OrdinalIgnoreCase))
        break;

    try
    {
        bool result = PalindromeChecker.IsPalindrome(line);
        Console.WriteLine($"Output: {result}");
    }
    catch (ArgumentNullException ex)
    {
        Console.Error.WriteLine($"[Error] {ex.Message}");
    }
    catch (ArgumentException ex)
    {
        Console.Error.WriteLine($"[Error] {ex.Message}");
    }

    Console.WriteLine();
}
