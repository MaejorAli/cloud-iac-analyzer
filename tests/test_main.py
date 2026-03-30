# tests/test_main.py
import json
import pytest
from unittest.mock import patch, MagicMock
from main import analyze, load_json, Config, upload_to_s3


# Integration Tests with Config Injection & S3 Mocking
@pytest.mark.integration
def test_analyze_end_to_end_with_mocked_s3(tmp_path, create_temp_file):
    """
    Full integration test: cloud and IaC match, S3 upload mocked
    """
    cloud_data = [{"id": "1", "name": "bucket"}]
    iac_data = [{"id": "1", "name": "bucket"}]

    cloud_file = tmp_path / "cloud.json"
    iac_file = tmp_path / "iac.json"

    create_temp_file(cloud_data, cloud_file)
    create_temp_file(iac_data, iac_file)

    # Inject custom Config
    test_config = Config(
        cloud_file=str(cloud_file),
        iac_file=str(iac_file),
        s3_bucket="test-bucket",
        s3_key="test-report.json"
    )

    # Mock S3 client
    with patch("main.boto3.client") as mock_boto:
        mock_s3 = MagicMock()
        mock_boto.return_value = mock_s3

        result = analyze(test_config.cloud_file, test_config.iac_file)
        upload_to_s3(result, test_config)

        # Verify S3 client called
        mock_s3.create_bucket.assert_called_with(Bucket="test-bucket")
        mock_s3.put_object.assert_called()

        # Analyzer assertions
        assert len(result) == 1
        assert result[0]["State"] == "Match"
        assert result[0]["ChangeLog"] == {}

@pytest.mark.integration
def test_analyze_missing_resource_with_mocked_s3(tmp_path, create_temp_file):
    """
    IaC missing, S3 mocked, config injection
    """
    cloud_data = [{"id": "1"}]
    iac_data = []

    cloud_file = tmp_path / "cloud.json"
    iac_file = tmp_path / "iac.json"

    create_temp_file(cloud_data, cloud_file)
    create_temp_file(iac_data, iac_file)

    test_config = Config(
        cloud_file=str(cloud_file),
        iac_file=str(iac_file),
        s3_bucket="test-bucket",
        s3_key="test-report.json"
    )

    with patch("main.boto3.client") as mock_boto:
        mock_s3 = MagicMock()
        mock_boto.return_value = mock_s3

        result = analyze(test_config.cloud_file, test_config.iac_file)
        upload_to_s3(result, test_config)

        mock_s3.create_bucket.assert_called_with(Bucket="test-bucket")
        mock_s3.put_object.assert_called()

        assert result[0]["State"] == "Missing"
        assert result[0]["ChangeLog"] == {}


# Edge tests
@pytest.mark.integration
def test_analyze_with_empty_inputs(tmp_path, create_temp_file):
    cloud_file = tmp_path / "cloud.json"
    iac_file = tmp_path / "iac.json"

    create_temp_file([], cloud_file)
    create_temp_file([], iac_file)

    result = analyze(str(cloud_file), str(iac_file))
    assert result == []

@pytest.mark.integration
def test_analyze_with_invalid_json(tmp_path, create_temp_file):
    cloud_file = tmp_path / "cloud.json"
    iac_file = tmp_path / "iac.json"

    cloud_file.write_text("{invalid_json}")
    create_temp_file([], iac_file)

    import json
    with pytest.raises(json.JSONDecodeError):
        analyze(str(cloud_file), str(iac_file))

@pytest.mark.integration
def test_analyze_with_missing_file(tmp_path, create_temp_file):
    cloud_file = tmp_path / "cloud.json"  # not created
    iac_file = tmp_path / "iac.json"
    create_temp_file([], iac_file)

    with pytest.raises(FileNotFoundError):
        analyze(str(cloud_file), str(iac_file))


# Unit Tests
@pytest.mark.unit
def test_invalid_json(tmp_path):
    invalid_file = tmp_path / "bad.json"
    invalid_file.write_text("{invalid}")
    with pytest.raises(json.JSONDecodeError):
        load_json(invalid_file)