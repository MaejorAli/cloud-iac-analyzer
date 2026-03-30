import pytest
from analyzer.comparator import compare_resources


# Core scenarios (Missing, Match, Modified)
@pytest.mark.unit
@pytest.mark.parametrize(
    "cloud,iac,expected_state,expected_changelog",
    [
        # IaC missing
        ({"id": "1"}, None, "Missing", {}),
        # Identical
        ({"id": "1", "name": "bucket"}, {"id": "1", "name": "bucket"}, "Match", {}),
        # Simple modification
        ({"id": "1", "tags": {"size": "10kb"}}, {"id": "1", "tags": {"size": "20kb"}}, "Modified", [{"KeyName": "tags.size", "CloudValue": "10kb", "IacValue": "20kb"}]),
        # Partial missing key
        ({"id": "1", "region": "us-east-1"}, {"id": "1"}, "Modified", [{"KeyName": "region", "CloudValue": "us-east-1", "IacValue": None}]),
    ]
)
def test_compare_resources_core(cloud, iac, expected_state, expected_changelog):
    result = compare_resources(cloud, iac)
    assert result["State"] == expected_state
    assert result["ChangeLog"] == expected_changelog


# Edge cases
@pytest.mark.unit
@pytest.mark.parametrize(
    "cloud,iac,expected_state",
    [
        ({}, {}, "Match"),  # empty
        ({"id": "1", "size": None}, {"id": "1", "size": None}, "Match"),  # nulls
        ({"a": {"b": {"c": {"d": 1}}}}, {"a": {"b": {"c": {"d": 1}}}}, "Match"),  # deep nesting
        ({"id": "1", "values": [1, "2", 3]}, {"id": "1", "values": [1, 2, 3]}, "Match"),  # mixed arrays
        ({"name": "Bucket "}, {"name": "bucket"}, "Match"),  # string normalization
    ]
)
def test_compare_resources_edge_cases(cloud, iac, expected_state):
    result = compare_resources(cloud, iac)
    assert result["State"] == expected_state
    assert result["ChangeLog"] == {}