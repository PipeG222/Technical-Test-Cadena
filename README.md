# Technical Test — Cadena

> Componente Práctico (50%) + Conceptos AWS & DevOps (50%)

---

## Estructura del Repositorio

```
Technical-Test-Cadena/
├── python/
│   ├── prime_sum.py          # Ejercicio 1 — Suma de primos
│   ├── requirements.txt
│   └── tests/
│       └── test_prime_sum.py # 24 pruebas unitarias
│
├── csharp/
│   └── PalindromeApp/
│       ├── PalindromeApp.sln
│       ├── PalindromeApp/
│       │   ├── PalindromeChecker.cs   # Ejercicio 2 — Verificador de palíndromos
│       │   └── Program.cs
│       └── PalindromeApp.Tests/
│           └── PalindromeCheckerTests.cs  # 19 pruebas unitarias
│
├── aws/
│   └── answers.md            # Respuestas escritas AWS & DevOps (preguntas 1–5)
│
└── docs/
    └── architecture.md       # Diagramas de algoritmos y arquitectura
```

---

## Por qué este enfoque

En lugar de entregar código aislado, esta solución aplica las mismas prácticas que se usan en equipos de desarrollo profesionales:

| Práctica | Aplicación en esta prueba |
|---|---|
| **Algoritmos eficientes** | Sieve of Eratosthenes O(M log log M) en Python; two-pointer O(n) en C# |
| **Manejo de errores explícito** | Excepciones con mensajes descriptivos que identifican índice y tipo del valor inválido |
| **Pruebas unitarias** | 24 tests en Python (pytest) y 19 en C# (xUnit) cubriendo casos felices, borde y errores |
| **Cobertura de casos borde** | Listas vacías, booleanos, floats, negativos, strings de 1 M de caracteres |
| **Zero heap allocations (C#)** | `stackalloc` + `Span<char>` para strings cortos — sin presión al GC |
| **Separación de responsabilidades** | Lógica de negocio (`PalindromeChecker`) desacoplada del punto de entrada (`Program.cs`) |
| **Infraestructura como código** | Ejemplos AWS con CloudFormation / SAM listos para desplegarse |

---

## Ejercicio 1 — Python: Suma de Números Primos

### Algoritmo

Se utiliza la **Criba de Eratóstenes** en lugar de verificar cada número individualmente (división por prueba).

**¿Por qué?**  
Para una lista de 100 000 enteros con valores hasta 10 000, la división por prueba ejecuta hasta ~100 operaciones por elemento (√10 000), totalizando ~10 M operaciones. La criba construye un arreglo booleano de 10 K posiciones en ~23 K operaciones y resuelve cada elemento en O(1) — órdenes de magnitud más rápido.

```
Complejidad temporal:  O(n + M log log M)   donde M = max(lista)
Complejidad espacial:  O(n + M)
```

### Correr el ejercicio

```bash
# Desde la raíz del repositorio
git clone https://github.com/PipeG222/Technical-Test-Cadena.git
cd Technical-Test-Cadena

# 1. Instalar dependencias
pip install -r python/requirements.txt

# 2. Prueba rápida (caso del enunciado)
python -m python.prime_sum
```

**Salida esperada:**
```
Input : [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
Output: 17
```

### Correr las pruebas unitarias

```bash
# Ejecutar las 24 pruebas con detalle
pytest python/tests/ -v

# Con reporte de cobertura de código
pytest python/tests/ -v --cov=python --cov-report=term-missing
```

**Salida esperada:**
```
python/tests/test_prime_sum.py::TestIsPrime::test_zero_is_not_prime         PASSED
python/tests/test_prime_sum.py::TestIsPrime::test_large_prime               PASSED
python/tests/test_prime_sum.py::TestSumOfPrimesHappyPath::test_example_from_spec PASSED
python/tests/test_prime_sum.py::TestSumOfPrimesHappyPath::test_large_list   PASSED
...
24 passed in 0.10s
```

**Qué cubren las pruebas:**

| Grupo | Casos |
|---|---|
| `TestIsPrime` | 0, 1, 2, 3, números compuestos, primo grande (7 919) |
| `TestSumOfPrimesHappyPath` | Ejemplo del enunciado, lista vacía, sin primos, todos primos, duplicados, generadores, lista de 10 000 elementos |
| `TestSumOfPrimesErrors` | No iterable, float, string, None, bool, entero negativo |

### Manejo de errores

| Escenario | Comportamiento |
|---|---|
| Entrada no iterable (ej. `42`) | `TypeError` con mensaje descriptivo |
| Elemento no entero (ej. `"dos"`, `2.0`, `None`) | `TypeError` indicando índice y tipo |
| Elemento booleano (`True`/`False`) | `TypeError` — booleanos son semánticamente inválidos |
| Entero negativo | `ValueError` indicando índice y valor |
| Lista vacía | Retorna `0` |

---

## Ejercicio 2 — C#: Verificador de Palíndromos

### Algoritmo

1. **Normalización** — un único recorrido O(n) filtra caracteres no alfanuméricos y convierte a minúsculas en un buffer `Span<char>`. Para strings ≤ 256 caracteres el buffer se aloja en el **stack** (`stackalloc`), produciendo **cero allocations en el heap** y sin presión al GC.
2. **Verificación two-pointer** — punteros izquierdo/derecho avanzan hacia el centro; cortocircuita en el primer mismatch.

```
Complejidad temporal:  O(n)
Complejidad espacial:  O(n)  — un único buffer, sin copias adicionales
```

### Correr el ejercicio

```bash
# Desde la raíz del repositorio
cd csharp/PalindromeApp
dotnet run --project PalindromeApp/PalindromeApp.csproj
```

**Salida esperada:**
```
=== Palindrome Checker ===

Enter a string (or 'exit' to quit): A man a plan a canal Panama
Output: True

Enter a string (or 'exit' to quit): hello
Output: False

Enter a string (or 'exit' to quit): exit
```

### Correr las pruebas unitarias

```bash
# Desde la raíz del repositorio
dotnet test csharp/PalindromeApp/PalindromeApp.Tests/PalindromeApp.Tests.csproj --logger "console;verbosity=minimal"
```

**Salida esperada:**
```
Correctas! - Con error: 0, Superado: 19, Omitido: 0, Total: 19, Duración: 35 ms
```

**Qué cubren las pruebas:**

| Grupo | Casos |
|---|---|
| Casos del enunciado | "A man a plan a canal Panama" → `true` |
| Palíndromos válidos | racecar, Madam, No lemon no melon, numéricos (12321) |
| No palíndromos | hello, world, frases normales |
| Casos borde | carácter único, solo puntuación, solo espacios, string vacío |
| Rendimiento | String de 1 000 000 de caracteres (palíndromo y no palíndromo) |
| Errores | `null` → `ArgumentNullException`, input > 5 M chars → `ArgumentException` |

### Manejo de errores

| Escenario | Comportamiento |
|---|---|
| `null` | `ArgumentNullException` |
| Input mayor a 5 000 000 caracteres | `ArgumentException` con detalle de longitud |
| String vacío o solo espacios | Retorna `false` |
| Solo puntuación/símbolos | Retorna `false` |

---

## AWS Services & DevOps (Preguntas 1–5)

Respuestas detalladas con diagramas de arquitectura y fragmentos de código en:

**[aws/answers.md](aws/answers.md)**

| # | Tema |
|---|---|
| 1 | Amazon RDS vs DynamoDB — tabla comparativa y casos de uso desde perspectiva del desarrollador |
| 2 | AWS Lambda & serverless — servicio de thumbnails con función Lambda y template SAM completo |
| 3 | DevOps — CI/CD, IaC, CodeCommit / CodeBuild / CodeDeploy / CodePipeline |
| 4 | Pipeline CI/CD — `buildspec.yml`, `appspec.yml`, stack CloudFormation completo |
| 5 | Amazon S3 — upload, download, pre-signed URLs y listado paginado con boto3 |

### Sobre los fragmentos de código AWS

Los fragmentos en `aws/answers.md` son ejemplos funcionales diseñados para ejecutarse dentro del ecosistema AWS, no como scripts locales. Cada uno se ejecuta en su contexto correspondiente:

| Fragmento | Cómo se ejecuta |
|---|---|
| **Función Lambda (Python)** | Desplegada con AWS SAM CLI: `sam build && sam deploy --guided` |
| **boto3 — S3 upload/download** | Localmente con credenciales configuradas: `aws configure && python script.py` |
| **CloudFormation pipeline** | `aws cloudformation deploy --template-file pipeline.yaml --stack-name my-pipeline --capabilities CAPABILITY_IAM` |
| **buildspec.yml / appspec.yml** | Los lee CodeBuild/CodeDeploy automáticamente al ejecutarse el pipeline — no requieren invocación manual |

---

## Requisitos

| Herramienta | Versión |
|---|---|
| Python | 3.11+ |
| pytest + pytest-cov | 8.x |
| .NET SDK | 8.0+ |
| AWS CLI *(opcional, para ejemplos AWS)* | 2.x |
| AWS SAM CLI *(opcional, para Lambda)* | 1.x |
