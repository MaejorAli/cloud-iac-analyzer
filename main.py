import json
import os
import boto3
from analyzer.comparator import compare_resources


# CONFIGURATION 
S3_ENDPOINT = os.getenv("S3_ENDPOINT_URL", "http://localstack:4566")
AWS_REGION = os.getenv("AWS_DEFAULT_REGION", "us-east-1")

CLOUD_FILE = os.getenv("CLOUD_RESOURCES_FILE", "data/cloud_resources.json")
IAC_FILE = os.getenv("IAC_RESOURCES_FILE", "data/iac_resources.json")

S3_BUCKET = os.getenv("S3_BUCKET_NAME", "analyzer-report")
S3_KEY = os.getenv("S3_OBJECT_KEY", "report.json")


def load_json(file_path):
    
    try:
        with open(file_path, 'r') as file:
            return json.load(file)

    except FileNotFoundError:
        print(f"ERROR: File not found: {file_path}")
        raise

    except json.JSONDecodeError as e:
        print(f"ERROR: Invalid JSON in file '{file_path}': {e}")
        raise

    except Exception as e:
        print(f"ERROR: Unexpected error while reading '{file_path}': {e}")
        raise


def index_iac_resources(iac_resources):
    return {resource["id"]: resource for resource in iac_resources}


def analyze(cloud_file, iac_file):
    cloud_resources = load_json(cloud_file)
    iac_resources = load_json(iac_file)
    iac_index = index_iac_resources(iac_resources)

    report = []

    for cloud_resource in cloud_resources:
        resource_id = cloud_resource.get("id")
        iac_resource = iac_index.get(resource_id)
        result = compare_resources(cloud_resource, iac_resource)
        report.append(result)

    return report


def upload_to_s3(report, bucket_name=S3_BUCKET, key=S3_KEY):
    """
    Upload the analyzer report to S3 (LocalStack or AWS).
    """

    s3 = boto3.client(
        "s3",
        endpoint_url=S3_ENDPOINT, 
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID", "test"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY", "test"),
        region_name=AWS_REGION
    )

    try:
        s3.create_bucket(Bucket=bucket_name)
    except s3.exceptions.BucketAlreadyOwnedByYou:
        pass

    s3.put_object(
        Bucket=bucket_name,
        Key=key,
        Body=json.dumps(report, indent=2)
    )

    print(f"Report uploaded to S3 bucket '{bucket_name}' with key '{key}'.")


if __name__ == "__main__":
    # run analysis with configurable files
    report = analyze(CLOUD_FILE, IAC_FILE)

    print(json.dumps(report, indent=2))

    upload_to_s3(report)