import json
import os
from main import analyze


def create_temp_file(data, filename):
    """
    Helper function to create temporary JSON files for testing
    """
    with open(filename, "w") as f:
        json.dump(data, f)


def test_analyze_end_to_end(tmp_path):
    """
    Full integration test of the analyzer
    """

    # create temporary test files
    cloud_data = [
        {"id": "1", "name": "bucket"}
    ]

    iac_data = [
        {"id": "1", "name": "bucket"}
    ]

    cloud_file = tmp_path / "cloud.json"
    iac_file = tmp_path / "iac.json"

    create_temp_file(cloud_data, cloud_file)
    create_temp_file(iac_data, iac_file)

    result = analyze(str(cloud_file), str(iac_file))

    assert len(result) == 1
    assert result[0]["State"] == "Match"


def test_analyze_missing_resource(tmp_path):
    """
    Test when IaC resource is missing
    """

    cloud_data = [{"id": "1"}]
    iac_data = []

    cloud_file = tmp_path / "cloud.json"
    iac_file = tmp_path / "iac.json"

    create_temp_file(cloud_data, cloud_file)
    create_temp_file(iac_data, iac_file)

    result = analyze(str(cloud_file), str(iac_file))

    assert result[0]["State"] == "Missing"