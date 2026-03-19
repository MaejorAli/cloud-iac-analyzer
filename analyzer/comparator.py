from analyzer.utils import flatten_dict


def compare_resources(cloud_resource, iac_resource):
    """
    Compare a cloud resource with its corresponding IaC resource.

    Args:
        cloud_resource (dict): Resource from cloud
        iac_resource (dict or None): Matching resource from IaC

    Returns:
        dict: Analysis result
    """

    # case 1: no matching IaC resource - MISSING
    if not iac_resource:
        return {
            "CloudResourceItem": cloud_resource,
            "IacResourceItem": {},
            "State": "Missing",
            "ChangeLog": []
        }

    # simplify comparison - flatten both resourses
    cloud_flat = flatten_dict(cloud_resource)
    iac_flat = flatten_dict(iac_resource)

    changes = []  # store differences

    # combine all keys from both dictionaries
    all_keys = set(cloud_flat.keys()).union(set(iac_flat.keys()))

    # compare values for each key
    for key in all_keys:
        cloud_value = cloud_flat.get(key)
        iac_value = iac_flat.get(key)

        # if values differ log the change
        if cloud_value != iac_value:
            changes.append({
                "KeyName": key,
                "CloudValue": cloud_value,
                "IacValue": iac_value
            })

    # Determine the state
    if not changes:
        state = "Match"
    else:
        state = "Modified"

    return {
        "CloudResourceItem": cloud_resource,
        "IacResourceItem": iac_resource,
        "State": state,
        "ChangeLog": changes
    }