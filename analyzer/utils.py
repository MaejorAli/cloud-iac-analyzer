# This function converts a nested dictionary into a flat dictionary
# Example:
# {"tags": {"size": "10kb"}} → {"tags.size": "10kb"}

def flatten_dict(data, parent_key='', separator='.'):
    """
    Recursively flattens a nested dictionary.

    Args:
        data (dict): The dictionary to flatten
        parent_key (str): The base key string for recursion
        separator (str): Separator between keys

    Returns:
        dict: Flattened dictionary
    """

    items = []  # store the flattened key-value pairs

    for key, value in data.items():
        # create new key path
        new_key = f"{parent_key}{separator}{key}" if parent_key else key

        # If value is another dictionary then recurse
        if isinstance(value, dict):
            items.extend(flatten_dict(value, new_key, separator).items())
        else:
            # base case 
            items.append((new_key, value))

    return dict(items)