import json
import pytest
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


def test_analyze_with_empty_inputs(tmp_path):
    """
    Should return empty report when both cloud and IaC inputs are empty
    """

    cloud_file = tmp_path / "cloud.json"
    iac_file = tmp_path / "iac.json"

    cloud_file.write_text("[]")
    iac_file.write_text("[]")

    result = analyze(str(cloud_file), str(iac_file))

    assert result == []  


def test_analyze_with_invalid_json(tmp_path):
    """
    Should raise JSONDecodeError when file contains invalid JSON
    """

    cloud_file = tmp_path / "cloud.json"
    iac_file = tmp_path / "iac.json"

    cloud_file.write_text("{invalid_json}")  # broken JSON
    iac_file.write_text("[]")

    with pytest.raises(Exception):
        analyze(str(cloud_file), str(iac_file))


def test_analyze_with_missing_file(tmp_path):
    """
    Should raise FileNotFoundError when input file is missing
    """

    cloud_file = tmp_path / "cloud.json"  # not created
    iac_file = tmp_path / "iac.json"

    iac_file.write_text("[]")

    import pytest
    with pytest.raises(FileNotFoundError):
        analyze(str(cloud_file), str(iac_file))