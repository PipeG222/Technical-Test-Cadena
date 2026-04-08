# Technical Test — Cadena

> Practical Component (50%) + AWS & DevOps Concepts (50%)

---

## Repository Structure

```
Technical-Test-Cadena/
├── python/
│   ├── prime_sum.py          # Exercise 1 — Sum of primes
│   ├── requirements.txt
│   └── tests/
│       └── test_prime_sum.py
│
├── csharp/
│   └── PalindromeApp/
│       ├── PalindromeApp.sln
│       ├── PalindromeApp/
│       │   ├── PalindromeChecker.cs   # Exercise 2 — Palindrome checker
│       │   └── Program.cs
│       └── PalindromeApp.Tests/
│           └── PalindromeCheckerTests.cs
│
├── aws/
│   └── answers.md            # AWS & DevOps written answers (questions 1–5)
│
└── docs/
    └── architecture.md       # Algorithm diagrams and architecture notes
```

---

## Exercise 1 — Python: Sum of Prime Numbers

### Approach

The function uses the **Sieve of Eratosthenes** — a classical algorithm with
*O(M log log M)* time complexity (where *M* is the maximum value in the list)
that pre-computes primality for every integer up to *M* in a single pass.
This makes per-element lookup *O(1)*, which is critical for large lists.

**Why not trial division per element?**  
For a list of 100 000 integers with values up to 10 000, trial division would
run up to ~100 checks per element (√10 000 = 100), totalling ~10 M operations.
The sieve builds a 10 K boolean array in ~23 K operations and then resolves
every element in *O(1)* — orders of magnitude faster.

### Run

```bash
# Install dependencies
pip install -r python/requirements.txt

# Smoke test
python -m python.prime_sum

# Unit tests with coverage report
pytest python/tests/ -v --cov=python --cov-report=term-missing
```

### Expected output

```
Input : [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
Output: 17
```

### Error handling

| Scenario | Behaviour |
|---|---|
| Non-iterable input (e.g. `42`) | `TypeError` with descriptive message |
| Non-integer element (e.g. `"two"`, `2.0`, `None`) | `TypeError` identifying index and type |
| Boolean element (`True`/`False`) | `TypeError` — booleans are semantically invalid |
| Negative integer | `ValueError` identifying index and value |
| Empty list | Returns `0` |

---

## Exercise 2 — C#: Palindrome Checker

### Approach

1. **Normalise** — a single O(n) pass filters out non-alphanumeric characters
   and converts to lower-case into a `Span<char>` buffer.  For strings ≤ 256
   characters the buffer is stack-allocated (`stackalloc`), producing **zero
   heap allocations** and no GC pressure.
2. **Two-pointer check** — left/right pointers advance toward the centre;
   short-circuits on the first mismatch.  Total: *O(n)* time, *O(n)* space.

### Run

```bash
# Run console application
cd csharp/PalindromeApp
dotnet run --project PalindromeApp/PalindromeApp.csproj

# Run unit tests
dotnet test PalindromeApp.Tests/PalindromeApp.Tests.csproj --logger "console;verbosity=normal"
```

### Expected output

```
Enter a string (or 'exit' to quit): A man a plan a canal Panama
Output: True

Enter a string (or 'exit' to quit): hello
Output: False
```

### Error handling

| Scenario | Behaviour |
|---|---|
| `null` input | `ArgumentNullException` |
| Input longer than 5 000 000 characters | `ArgumentException` with length info |
| Empty or whitespace-only string | Returns `false` |
| String with only punctuation/spaces | Returns `false` |

---

## AWS Services & DevOps (Questions 1–5)

Detailed written answers with architecture diagrams and code snippets:

**[aws/answers.md](aws/answers.md)**

Topics covered:

1. Amazon RDS vs DynamoDB — comparison table, developer use-case guidance
2. AWS Lambda & serverless — image thumbnail service with SAM template
3. DevOps concepts — CI/CD, IaC, CodeCommit / CodeBuild / CodeDeploy / CodePipeline
4. CI/CD pipeline setup — `buildspec.yml`, `appspec.yml`, CloudFormation pipeline stack
5. Amazon S3 — upload, download, pre-signed URLs, paginated listing (Python / boto3)

---

## Requirements

| Tool | Version |
|---|---|
| Python | 3.11+ |
| pytest | 8.x |
| .NET SDK | 8.0+ |
| AWS CLI (optional, for AWS examples) | 2.x |
