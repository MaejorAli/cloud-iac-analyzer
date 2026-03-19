from analyzer.comparator import compare_resources


def test_missing_iac_resource():
    """
    Should return 'Missing' when IaC resource is not found
    """
    cloud_resource = {"id": "1", "name": "bucket"}

    result = compare_resources(cloud_resource, None)

    assert result["State"] == "Missing"
    assert result["ChangeLog"] == []


def test_match_resources():
    """
    Should return 'Match' when resources are identical
    """
    cloud_resource = {"id": "1", "name": "bucket"}
    iac_resource = {"id": "1", "name": "bucket"}

    result = compare_resources(cloud_resource, iac_resource)

    assert result["State"] == "Match"
    assert result["ChangeLog"] == []


def test_modified_resources():
    """
    Should detect differences and return 'Modified'
    """
    cloud_resource = {
        "id": "1",
        "tags": {"size": "10kb"}
    }

    iac_resource = {
        "id": "1",
        "tags": {"size": "20kb"}
    }

    result = compare_resources(cloud_resource, iac_resource)

    assert result["State"] == "Modified"
    assert len(result["ChangeLog"]) == 1

    change = result["ChangeLog"][0]

    assert change["KeyName"] == "tags.size"
    assert change["CloudValue"] == "10kb"
    assert change["IacValue"] == "20kb"


def test_partial_missing_key():
    """
    Edge case: key exists in cloud but not in IaC
    """
    cloud_resource = {"id": "1", "region": "us-east-1"}
    iac_resource = {"id": "1"}

    result = compare_resources(cloud_resource, iac_resource)

    assert result["State"] == "Modified"
    assert result["ChangeLog"][0]["KeyName"] == "region"