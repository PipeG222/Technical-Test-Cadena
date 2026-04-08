# Architecture Notes

## Python — Sum of Primes

### Algorithm: Sieve of Eratosthenes

```
Input list: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

Step 1 — Validation: all items must be non-negative integers.

Step 2 — Find max value: max = 10

Step 3 — Build sieve up to 10:
  Index:   0  1  2  3  4  5  6  7  8  9  10
  Prime?:  F  F  T  T  F  T  F  T  F  F   F

Step 4 — Scan input, accumulate primes:
  2 → prime → total = 2
  3 → prime → total = 5
  5 → prime → total = 10
  7 → prime → total = 17

Output: 17
```

**Complexity**

| Step | Time | Space |
|---|---|---|
| Validation | O(n) | O(n) |
| Sieve construction | O(M log log M) where M = max(input) | O(M) |
| Accumulation | O(n) | O(1) |
| **Total** | **O(n + M log log M)** | **O(n + M)** |

For a list of 10 000 integers with max value 10 000, the sieve is ~78 KB and runs in microseconds.

---

## C# — Palindrome Checker

### Algorithm: Two-pointer on normalised span

```
Input: "A man a plan a canal Panama"

Step 1 — Normalise (filter alphanumeric, to lower-case):
  "amanaplanacanalpanama"
   ^                   ^  left=0, right=19

Step 2 — Two-pointer comparison:
  [0]='a' == [19]='a'  ✓ → left++, right--
  [1]='m' == [18]='m'  ✓ → ...
  ...
  left >= right        → palindrome confirmed

Output: True
```

**Complexity**

| Step | Time | Space |
|---|---|---|
| Normalisation | O(n) | O(n) — single pass, one buffer |
| Two-pointer check | O(n/2) = O(n) | O(1) |
| **Total** | **O(n)** | **O(n)** |

For small strings (≤ 256 chars) the buffer is allocated on the **stack** via `stackalloc`, completely avoiding GC pressure.

---

## Serverless Architecture — Image Thumbnail Service (AWS)

```
┌──────────────────────────────────────────────────────────────┐
│  AWS Region (us-east-1)                                      │
│                                                              │
│  ┌────────────┐    S3 Event      ┌─────────────────────┐     │
│  │  S3 Bucket │ ───────────────► │  Lambda Function    │     │
│  │  (uploads/)│                  │  generate_thumbnail │    │
│  └────────────┘                  └────────┬────────────┘     │
│                                           │                  │
│                            ┌──────────────┴──────────────┐   │
│                            │                             │   │
│                   ┌────────▼──────┐          ┌──────────▼─┐  │
│                   │  S3 Bucket    │          │  DynamoDB  │  │
│                   │ (thumbnails/) │          │  (metadata)│  │
│                   └───────────────┘          └────────────┘  │
└──────────────────────────────────────────────────────────────┘
```

## CI/CD Pipeline Architecture

```
Developer Workstation
        │
        │ git push origin main
        ▼
 ┌─────────────┐
 │ CodeCommit  │  ← source of truth
 └──────┬──────┘
        │ EventBridge rule (immediate, no polling)
        ▼
 ┌─────────────────────────────────────────────┐
 │              CodePipeline                   │
 │                                             │
 │  ┌──────────┐  ┌──────────┐  ┌───────────┐  │
 │  │  Source  │→ │  Build   │→ │  Deploy   │  │
 │  │(Commit)  │  │(CodeBuild│  │(CodeDeploy│  │
 │  └──────────┘  │buildspec)│  │appspec)   │  │
 │                └────┬─────┘  └─────┬─────┘  │
 └─────────────────────┼──────────────┼───────┘
                        │              │
                 ┌──────▼──────┐  ┌───▼───────────┐
                 │  S3 Artifact│  │  EC2 Fleet /  │
                 │  Bucket     │  │  ECS / Lambda │
                 └─────────────┘  └───────────────┘
```
