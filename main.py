import json
import os
import boto3
from analyzer.comparator import compare_resources
from dataclasses import dataclass, field


# CONFIGURATION 
@dataclass
class Config:
    s3_endpoint: str = field(default_factory=lambda: os.getenv("S3_ENDPOINT_URL", "http://localstack:4566"))
    aws_region: str = field(default_factory=lambda: os.getenv("AWS_DEFAULT_REGION", "us-east-1"))
    cloud_file: str = field(default_factory=lambda: os.getenv("CLOUD_RESOURCES_FILE", "data/cloud_resources.json"))
    iac_file: str = field(default_factory=lambda: os.getenv("IAC_RESOURCES_FILE", "data/iac_resources.json"))
    s3_bucket: str = field(default_factory=lambda: os.getenv("S3_BUCKET_NAME", "analyzer-report"))
    s3_key: str = field(default_factory=lambda: os.getenv("S3_OBJECT_KEY", "report.json"))

    @classmethod
    def from_env(cls):
        return cls()


def load_json(file_path):
    
    try:
        with open(file_path, 'r') as file:
            return json.load(file)

    except FileNotFoundError:
        raise FileNotFoundError(f"File not found: {file_path}")

    except json.JSONDecodeError as e:
        raise json.JSONDecodeError(f"Invalid JSON in {file_path}: {e.msg}", e.doc, e.pos)

    except Exception as e:
        raise Exception(f"Unexpected error while reading '{file_path}': {e}")
       


def index_iac_resources(iac_resources):
    return {resource["id"]: resource for resource in iac_resources}


def analyze(cloud_file, iac_file):
    cloud_resources = load_json(cloud_file)
    iac_resources = load_json(iac_file)
    iac_index = index_iac_resources(iac_resources)

    report = []

    for cloud_resource in cloud_resources:
        resource_id = cloud_resource.get("id")
        if resource_id is None:
            raise ValueError(f"Cloud resource missing 'id': {cloud_resource}")
        iac_resource = iac_index.get(resource_id)
        result = compare_resources(cloud_resource, iac_resource)
        report.append(result)

    return report


def upload_to_s3(report, config: Config):
    """
    Upload the analyzer report to S3 (LocalStack or AWS).
    """

    s3 = boto3.client(
        "s3",
        endpoint_url=config.s3_endpoint,
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID", "test"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY", "test"),
        region_name=config.aws_region
    )

    try:
        s3.create_bucket(Bucket=config.s3_bucket)
    except s3.exceptions.BucketAlreadyOwnedByYou:
        pass
    except s3.exceptions.BucketAlreadyExists:
        raise

    s3.put_object(
        Bucket=config.s3_bucket,
        Key=config.s3_key,
        Body=json.dumps(report, indent=2)
    )

    print(f"Report uploaded to S3 bucket '{config.s3_bucket}' with key '{config.s3_key}'.")


def main():
    config = Config.from_env()
    report = analyze(config.cloud_file, config.iac_file)
    print(json.dumps(report, indent=2))
    upload_to_s3(report, config)

if __name__ == "__main__":
    main()