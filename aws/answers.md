# AWS Services & IT Development Concepts

---

## 1. Amazon RDS vs Amazon DynamoDB

### Key Differences

| Dimension | Amazon RDS | Amazon DynamoDB |
|---|---|---|
| **Data model** | Relational (tables, rows, joins, foreign keys) | NoSQL key-value / document |
| **Schema** | Fixed schema; migrations required | Schema-less; attributes defined per item |
| **Query language** | SQL (MySQL, PostgreSQL, etc.) | PartiQL or DynamoDB-specific API |
| **Scaling** | Vertical (instance size) + Read Replicas | Horizontal; truly serverless with on-demand capacity |
| **Consistency** | ACID transactions by default | Eventually consistent by default; strong consistency opt-in per read |
| **Latency** | Low (ms) | Single-digit millisecond at any scale |
| **Max item/row size** | No practical row limit | 400 KB per item |
| **Pricing model** | Per-hour instance + storage | Per read/write capacity unit + storage |

### When to choose RDS

- **Complex relational data**: e-commerce orders, inventory, financial ledgers — anything with multiple entity relationships and ad-hoc join queries.
- **Existing SQL knowledge**: team already writes complex SQL and needs stored procedures or views.
- **ACID compliance**: banking transactions, booking systems where double-booking must be impossible.
- **Reporting**: heavy analytical queries on normalised data (combine with Amazon Aurora for read replicas or Aurora Serverless v2 for auto-scaling).

```
Example: A multi-tenant SaaS billing system
Tables: tenants → subscriptions → invoices → line_items
Natural fit for relational FK constraints and JOIN queries.
```

### When to choose DynamoDB

- **Predictable, high-throughput access patterns**: shopping cart (PK=userId, SK=productId), user session store, IoT telemetry.
- **Massive scale with low latency**: millions of requests per second without pre-warming.
- **Serverless applications**: pairs naturally with AWS Lambda — no connection pooling issues.
- **Flexible / evolving attributes**: product catalog where each category has different attributes.

```
Example: A real-time gaming leaderboard
PK=gameId, SK=score#userId → GetItem / Query by score range in <5 ms at global scale.
```

### Developer Perspective Summary

> Reach for **RDS** when your queries drive the schema.  
> Reach for **DynamoDB** when your access patterns are known upfront and scale is non-negotiable.

---

## 2. AWS Lambda and Serverless Computing

### What is AWS Lambda?

AWS Lambda is a **Function-as-a-Service (FaaS)** offering that executes code in response to events without requiring you to provision or manage servers.  Key properties:

- **Event-driven**: triggers include API Gateway, S3, DynamoDB Streams, SQS, SNS, EventBridge, and more.
- **Auto-scaling**: Lambda scales from 0 to thousands of concurrent executions automatically.
- **Pay-per-use**: billed in 1-ms increments; zero cost when idle.
- **Ephemeral**: each invocation gets a fresh execution context (though containers may be reused — "warm starts").

### Serverless Application Example: Image Thumbnail Service

**Architecture**

```
User ──► S3 (uploads/*)
             │
             └── S3 Event ──► Lambda (generate_thumbnail)
                                    │
                                    └──► S3 (thumbnails/*)
                                    └──► DynamoDB (image metadata)
```

**Lambda function (Python 3.12)**

```python
import boto3
import os
from io import BytesIO
from PIL import Image          # packaged as a Lambda layer

s3 = boto3.client("s3")
dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(os.environ["METADATA_TABLE"])

THUMBNAIL_SIZE = (128, 128)


def handler(event: dict, context) -> dict:
    """Triggered by S3 ObjectCreated events."""
    for record in event["Records"]:
        bucket = record["s3"]["bucket"]["name"]
        key = record["s3"]["object"]["key"]

        # Download original
        response = s3.get_object(Bucket=bucket, Key=key)
        image_data = response["Body"].read()

        # Generate thumbnail
        with Image.open(BytesIO(image_data)) as img:
            img.thumbnail(THUMBNAIL_SIZE)
            buffer = BytesIO()
            img.save(buffer, format=img.format or "JPEG")
            buffer.seek(0)

        # Upload thumbnail
        thumb_key = key.replace("uploads/", "thumbnails/")
        s3.put_object(
            Bucket=bucket,
            Key=thumb_key,
            Body=buffer,
            ContentType=response["ContentType"],
        )

        # Store metadata
        table.put_item(Item={
            "imageId": key,
            "thumbnailKey": thumb_key,
            "originalSize": len(image_data),
        })

    return {"statusCode": 200}
```

**Infrastructure as Code (AWS SAM)**

```yaml
# template.yaml
AWSTemplateFormatVersion: "2010-09-09"
Transform: AWS::Serverless-2016-10-31

Globals:
  Function:
    Runtime: python3.12
    Timeout: 30
    MemorySize: 512
    Environment:
      Variables:
        METADATA_TABLE: !Ref MetadataTable

Resources:
  ThumbnailFunction:
    Type: AWS::Serverless::Function
    Properties:
      CodeUri: src/
      Handler: thumbnail.handler
      Events:
        S3Upload:
          Type: S3
          Properties:
            Bucket: !Ref ImageBucket
            Events: s3:ObjectCreated:*
            Filter:
              S3Key:
                Rules:
                  - Name: prefix
                    Value: uploads/

  ImageBucket:
    Type: AWS::S3::Bucket

  MetadataTable:
    Type: AWS::DynamoDB::Table
    Properties:
      BillingMode: PAY_PER_REQUEST
      AttributeDefinitions:
        - AttributeName: imageId
          AttributeType: S
      KeySchema:
        - AttributeName: imageId
          KeyType: HASH
```

---

## 3. DevOps and AWS Developer Tools

### What is DevOps?

DevOps is a cultural and engineering philosophy that **eliminates the wall between Development and Operations** by unifying processes, tools, and responsibilities throughout the software lifecycle.

**Core practices**

| Practice | Description |
|---|---|
| **Continuous Integration (CI)** | Developers merge code frequently; every commit triggers an automated build and test suite |
| **Continuous Delivery (CD)** | Artifacts are always in a releasable state; deployment to production is a one-click (or automatic) operation |
| **Infrastructure as Code (IaC)** | Infrastructure is defined in version-controlled templates (CloudFormation, Terraform, CDK) |
| **Monitoring & Observability** | Metrics, logs, and traces feed back into the development cycle (CloudWatch, X-Ray) |
| **Security as Code (DevSecOps)** | Security scans and compliance checks are gates in the pipeline, not afterthoughts |

### AWS Developer Tools

```
Developer                AWS CodeCommit             AWS CodeBuild
(git push) ─────────────► (source repository) ──────► (build & test)
                                                           │
                                                           ▼
                                               AWS CodeDeploy
                                               (EC2 / ECS / Lambda)
                                                           ▲
                          AWS CodePipeline ───────────────┘
                          (orchestrates the above stages)
```

**AWS CodeCommit** – Fully managed private Git repository; IAM-integrated, no separate user management needed. Ideal when you must keep source code inside your AWS account (compliance).

**AWS CodeBuild** – Managed build service that compiles code, runs tests, and produces artifacts. Scales automatically; no build servers to maintain. Uses `buildspec.yml` to declare build steps.

**AWS CodeDeploy** – Automates deployments to EC2 fleets, ECS tasks, and Lambda functions. Supports rolling, blue/green, and canary strategies.

**AWS CodePipeline** – Orchestration layer that connects source → build → test → deploy stages. Integrates with third-party tools (GitHub, Bitbucket, Jenkins).

---

## 4. CI/CD Pipeline with CodePipeline + CodeBuild

### Architecture

```
GitHub / CodeCommit
        │
        │ (webhook on push to main)
        ▼
 ┌─────────────────────────────────────────────────────────┐
 │                  AWS CodePipeline                        │
 │                                                          │
 │  Stage 1: Source  ──►  Stage 2: Build  ──►  Stage 3: Deploy │
 │  (CodeCommit)          (CodeBuild)           (CodeDeploy /   │
 │                                               ECS / Lambda)  │
 └─────────────────────────────────────────────────────────┘
```

### buildspec.yml (Node.js web app)

```yaml
# buildspec.yml — placed at the root of the repository
version: 0.2

phases:
  install:
    runtime-versions:
      nodejs: 20
    commands:
      - npm ci                          # deterministic install from package-lock.json

  pre_build:
    commands:
      - echo "Running unit tests..."
      - npm test -- --ci --coverage
      - echo "Security audit..."
      - npm audit --audit-level=high

  build:
    commands:
      - echo "Building production bundle..."
      - npm run build                   # outputs to ./dist

  post_build:
    commands:
      - echo "Packaging application..."
      - cp appspec.yml dist/
      - cp -r scripts dist/

artifacts:
  files:
    - "dist/**/*"
  discard-paths: no

cache:
  paths:
    - node_modules/**/*                 # speeds up subsequent builds
```

### appspec.yml (CodeDeploy to EC2)

```yaml
version: 0.0
os: linux
files:
  - source: /
    destination: /var/www/myapp

hooks:
  BeforeInstall:
    - location: scripts/stop_server.sh
      timeout: 30
  AfterInstall:
    - location: scripts/install_dependencies.sh
      timeout: 120
  ApplicationStart:
    - location: scripts/start_server.sh
      timeout: 30
  ValidateService:
    - location: scripts/health_check.sh
      timeout: 60
      runas: root
```

### CloudFormation — Pipeline definition

```yaml
# pipeline.yaml
AWSTemplateFormatVersion: "2010-09-09"
Description: CI/CD pipeline for web application

Parameters:
  RepositoryName:
    Type: String
    Default: my-web-app
  BranchName:
    Type: String
    Default: main

Resources:
  ArtifactBucket:
    Type: AWS::S3::Bucket
    Properties:
      VersioningConfiguration:
        Status: Enabled

  CodeBuildProject:
    Type: AWS::CodeBuild::Project
    Properties:
      Name: !Sub "${RepositoryName}-build"
      ServiceRole: !GetAtt CodeBuildRole.Arn
      Artifacts:
        Type: CODEPIPELINE
      Environment:
        Type: LINUX_CONTAINER
        ComputeType: BUILD_GENERAL1_SMALL
        Image: aws/codebuild/standard:7.0
      Source:
        Type: CODEPIPELINE
        BuildSpec: buildspec.yml

  Pipeline:
    Type: AWS::CodePipeline::Pipeline
    Properties:
      Name: !Sub "${RepositoryName}-pipeline"
      RoleArn: !GetAtt PipelineRole.Arn
      ArtifactStore:
        Type: S3
        Location: !Ref ArtifactBucket
      Stages:
        - Name: Source
          Actions:
            - Name: SourceAction
              ActionTypeId:
                Category: Source
                Owner: AWS
                Provider: CodeCommit
                Version: "1"
              Configuration:
                RepositoryName: !Ref RepositoryName
                BranchName: !Ref BranchName
                PollForSourceChanges: false   # use EventBridge rule instead
              OutputArtifacts:
                - Name: SourceOutput

        - Name: Build
          Actions:
            - Name: BuildAction
              ActionTypeId:
                Category: Build
                Owner: AWS
                Provider: CodeBuild
                Version: "1"
              Configuration:
                ProjectName: !Ref CodeBuildProject
              InputArtifacts:
                - Name: SourceOutput
              OutputArtifacts:
                - Name: BuildOutput

        - Name: Deploy
          Actions:
            - Name: DeployAction
              ActionTypeId:
                Category: Deploy
                Owner: AWS
                Provider: CodeDeploy
                Version: "1"
              Configuration:
                ApplicationName: !Ref CodeDeployApplication
                DeploymentGroupName: !Ref DeploymentGroup
              InputArtifacts:
                - Name: BuildOutput
```

### Key best practices demonstrated

- **No polling** — EventBridge rule triggers the pipeline on CodeCommit push (lower latency, no wasted API calls).
- **Artifact bucket with versioning** — allows rollback to any previous build.
- **Separation of concerns** — build logic lives in `buildspec.yml` (owned by developers), deployment logic in `appspec.yml` (owned by ops/platform team).
- **Blue/Green deployment** — CodeDeploy can shift traffic gradually, enabling instant rollback.

---

## 5. Amazon S3 — Concepts and Code Examples

### What is Amazon S3?

Amazon Simple Storage Service (S3) is an **object storage** service designed for 99.999999999% (11 nines) durability.  Objects are stored in **buckets** (globally unique namespace) and addressed by a **key** (path-like string).

### Common use cases

| Use case | S3 feature |
|---|---|
| Static website / SPA hosting | S3 static website hosting + CloudFront CDN |
| Application asset storage (images, PDFs) | Pre-signed URLs for secure upload/download |
| Data lake / analytics | S3 + Athena / AWS Glue |
| Backup and archival | S3 Glacier storage classes, Lifecycle rules |
| CI/CD artifact store | CodePipeline artifact bucket |
| Log aggregation | S3 + CloudWatch / Athena querying |

### Code examples (Python — boto3)

#### Upload a file

```python
import boto3
from botocore.exceptions import ClientError
import logging

logger = logging.getLogger(__name__)
s3 = boto3.client("s3")


def upload_file(
    local_path: str,
    bucket: str,
    s3_key: str,
    content_type: str = "application/octet-stream",
) -> bool:
    """Upload a local file to S3.

    Returns True on success, False on failure.
    """
    try:
        s3.upload_file(
            Filename=local_path,
            Bucket=bucket,
            Key=s3_key,
            ExtraArgs={"ContentType": content_type},
        )
        logger.info("Uploaded %s → s3://%s/%s", local_path, bucket, s3_key)
        return True
    except FileNotFoundError:
        logger.error("Local file not found: %s", local_path)
        return False
    except ClientError as exc:
        logger.error("S3 upload failed: %s", exc)
        return False
```

#### Download a file

```python
def download_file(bucket: str, s3_key: str, local_path: str) -> bool:
    """Download an object from S3 to a local path."""
    try:
        s3.download_file(Bucket=bucket, Key=s3_key, Filename=local_path)
        logger.info("Downloaded s3://%s/%s → %s", bucket, s3_key, local_path)
        return True
    except ClientError as exc:
        error_code = exc.response["Error"]["Code"]
        if error_code == "404":
            logger.error("Object not found: s3://%s/%s", bucket, s3_key)
        else:
            logger.error("S3 download failed: %s", exc)
        return False
```

#### Generate a pre-signed URL (time-limited access without AWS credentials)

```python
from datetime import timedelta


def generate_presigned_url(
    bucket: str,
    s3_key: str,
    expiry: timedelta = timedelta(hours=1),
    operation: str = "get_object",
) -> str | None:
    """Return a pre-signed URL valid for *expiry* duration.

    The URL grants temporary access to the object without requiring
    the caller to have AWS credentials.
    """
    try:
        url = s3.generate_presigned_url(
            ClientMethod=operation,
            Params={"Bucket": bucket, "Key": s3_key},
            ExpiresIn=int(expiry.total_seconds()),
        )
        return url
    except ClientError as exc:
        logger.error("Could not generate pre-signed URL: %s", exc)
        return None
```

#### List objects with pagination

```python
from collections.abc import Iterator


def list_objects(bucket: str, prefix: str = "") -> Iterator[dict]:
    """Yield every object metadata dict under *prefix* using automatic pagination."""
    paginator = s3.get_paginator("list_objects_v2")
    for page in paginator.paginate(Bucket=bucket, Prefix=prefix):
        yield from page.get("Contents", [])


# Usage
for obj in list_objects("my-bucket", prefix="uploads/2024/"):
    print(obj["Key"], obj["Size"])
```

### Security best practices highlighted in the examples

1. **No public ACLs** — objects are private by default; pre-signed URLs grant scoped, time-bounded access.
2. **Error handling** — `ClientError` is caught and logged rather than letting exceptions propagate silently.
3. **Pagination** — `list_objects_v2` returns at most 1 000 keys per page; the paginator handles continuation tokens automatically.
4. **IAM least-privilege** — the application should only hold `s3:GetObject`, `s3:PutObject` on the specific bucket ARN, not `s3:*`.
