import json
import boto3
from analyzer.comparator import compare_resources


def load_json(file_path):
    """
    Load JSON data from a file.

    Args:
        file_path (str): Path to JSON file

    Returns:
        list: Parsed JSON data
    """
    with open(file_path, 'r') as file:
        return json.load(file)


def index_iac_resources(iac_resources):
    """
    Convert IaC list into a dictionary for fast lookup by 'id'.

    Example:
        [{"id": "1"}] → {"1": {...}}

    Args:
        iac_resources (list)

    Returns:
        dict
    """
    return {resource["id"]: resource for resource in iac_resources}


def analyze(cloud_file, iac_file):
    """
    Main function to analyze cloud vs IaC resources.

    Args:
        cloud_file (str)
        iac_file (str)

    Returns:
        list: Analysis report
    """
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


def upload_to_s3(report, bucket_name="analyzer-report", key="report.json"):
    """
    Upload the analyzer report to LocalStack S3.

    Args:
        report (list): Analyzer report
        bucket_name (str): Name of S3 bucket
        key (str): Object key in S3
    """
    # initialize S3 client for LocalStack
    s3 = boto3.client(
        "s3",
        endpoint_url="http://localstack:4566",  # localStack default endpoint
        aws_access_key_id="test",
        aws_secret_access_key="test",
        region_name="us-east-1"
    )

    # create bucket if it doesn't exist
    try:
        s3.create_bucket(Bucket=bucket_name)
    except s3.exceptions.BucketAlreadyOwnedByYou:
        pass  # if bucket already exists

    # upload report
    s3.put_object(
        Bucket=bucket_name,
        Key=key,
        Body=json.dumps(report, indent=2)
    )

    print(f"Report uploaded to S3 bucket '{bucket_name}' with key '{key}'.")


if __name__ == "__main__":
    # run analysis
    report = analyze(
        "data/cloud_resources.json",
        "data/iac_resources.json"
    )

    # print report to console
    print(json.dumps(report, indent=2))

    # upload report to S3
    upload_to_s3(report)