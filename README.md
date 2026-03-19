# Cloud vs IaC Analyzer

## Description
This Python project compares your actual cloud resources with your IaC definitions, detects differences, and generates a report in JSON format, uploaded to an S3 bucket.

## Features
- Compare AWS cloud resources vs IaC
- Detect modified, missing, or changed resources
- Upload JSON report to S3 bucket
- Fully containerized using Docker Compose
- Includes automated tests using pytest

## Docker Setup
```bash
# Start LocalStack and analyzer
docker-compose build
docker-compose up

# Stop and clean containers & volumes
docker-compose down -v
```
## Testing
Run tests using:
`pytest -v`

## Retrieving the Report
Download the report from LocalStack S3 bucket:
```bash
docker exec -it localstack awslocal s3 cp s3://analyzer-report/report.json /tmp/report.json

docker cp localstack:/tmp/report.json ./report.json

cat report.json
```

## Example Output
```bash
[
  {
    "CloudResourceItem": {
      "id": "1",
      "name": "bucket-1",
      "tags": { "totalAmount": "17kb" }
    },
    "IacResourceItem": {
      "id": "1",
      "name": "bucket-1",
      "tags": { "totalAmount": "22kb" }
    },
    "State": "Modified",
    "ChangeLog": [
      {
        "KeyName": "tags.totalAmount",
        "CloudValue": "17kb",
        "IacValue": "22kb"
      }
    ]
  },
  {
    "CloudResourceItem": {
      "id": "2",
      "name": "bucket-2",
      "tags": { "totalAmount": "30kb" }
    },
    "IacResourceItem": {},
    "State": "Missing",
    "ChangeLog": []
  }
]
```


## Technologies
- Python 3

- Docker & Docker Compose

- LocalStack

- AWS CLI / awslocal

- pytest