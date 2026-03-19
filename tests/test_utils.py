from analyzer.utils import flatten_dict


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