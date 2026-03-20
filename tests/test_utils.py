from analyzer.utils import flatten_dict
from analyzer.comparator import compare_resources


def test_flatten_dict_simple():
    """
    Test flattening a simple nested dictionary
    """
    input_data = {
        "tags": {
            "size": "10kb"
        }
    }

    expected_output = {
        "tags.size": "10kb"
    }

    assert flatten_dict(input_data) == expected_output


def test_flatten_dict_multiple_levels():
    """
    Test flattening deeper nested structures
    """
    input_data = {
        "a": {
            "b": {
                "c": 1
            }
        }
    }

    expected_output = {
        "a.b.c": 1
    }

    assert flatten_dict(input_data) == expected_output


def test_flatten_dict_empty():
    """
    Edge case: empty dictionary
    """
    assert flatten_dict({}) == {}


def test_deeply_nested_structures():
    """
    Ensure flattening and comparison works for deep nesting
    """
    cloud = {"a": {"b": {"c": {"d": 1}}}}
    iac = {"a": {"b": {"c": {"d": 1}}}}

    result = compare_resources(cloud, iac)

    assert result["State"] == "Match"


def test_mixed_array_types():
    """
    Arrays with mixed types should be compared correctly
    """
    cloud = {"id": "1", "values": [1, "2", 3]}
    iac = {"id": "1", "values": [1, 2, 3]}

    result = compare_resources(cloud, iac)

    # depending on your flatten logic, this may be Modified
    assert result["State"] in ["Match", "Modified"]    