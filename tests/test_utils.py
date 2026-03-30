import pytest
from analyzer.utils import flatten_dict
from analyzer.comparator import compare_resources


# Flatten dict tests
@pytest.mark.unit
@pytest.mark.parametrize(
    "input_data,expected_output",
    [
        ({"tags": {"size": "10kb"}}, {"tags.size": "10kb"}),
        ({"a": {"b": {"c": 1}}}, {"a.b.c": 1}),
        ({}, {}),  # empty dict
        ({"a": {"b": {"c": {"d": 1}}}}, {"a.b.c.d": 1}),
    ]
)
def test_flatten_dict(input_data, expected_output):
    assert flatten_dict(input_data) == expected_output


# compare_resources tests
@pytest.mark.unit
@pytest.mark.parametrize(
    "cloud,iac,expected_state",
    [
        ({"a": {"b": {"c": {"d": 1}}}}, {"a": {"b": {"c": {"d": 1}}}}, "Match"),
        ({"id": "1", "values": [1, "2", 3]}, {"id": "1", "values": [1, 2, 3]}, "Match"),
        ({"id": "1"}, {"id": "1", "name": "bucket"}, "Modified"),
        ({"id": "1"}, None, "Missing"),
    ]
)
def test_compare_resources_parametrized(cloud, iac, expected_state):
    result = compare_resources(cloud, iac)
    assert result["State"] == expected_state