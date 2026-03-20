from analyzer.utils import flatten_dict


def normalize_value(value):
    if isinstance(value, str):
        try:
            return int(value) if '.' not in value else float(value)
        except ValueError:
            return value.strip().lower()
    return value


def compare_resources(cloud_resource, iac_resource):
    """
    Compare a cloud resource with its corresponding IaC resource.
    """

    # case 1: no matching IaC resource - MISSING
    if iac_resource is None:
        return {
            "CloudResourceItem": cloud_resource,
            "IacResourceItem": {},
            "State": "Missing",
            "ChangeLog": {} 
        }

    cloud_flat = flatten_dict(cloud_resource)
    iac_flat = flatten_dict(iac_resource)

    changes = []

    all_keys = set(cloud_flat.keys()).union(set(iac_flat.keys()))

    for key in all_keys:
        cloud_value = cloud_flat.get(key)
        iac_value = iac_flat.get(key)

        if normalize_value(cloud_value) != normalize_value(iac_value):
            changes.append({
                "KeyName": key,
                "CloudValue": cloud_value,
                "IacValue": iac_value
            })

    # determine state
    if not changes:
        return {
            "CloudResourceItem": cloud_resource,
            "IacResourceItem": iac_resource,
            "State": "Match",
            "ChangeLog": {} 
        }

    # only Modified returns list
    return {
        "CloudResourceItem": cloud_resource,
        "IacResourceItem": iac_resource,
        "State": "Modified",
        "ChangeLog": changes
    }