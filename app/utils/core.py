import functools


def collect_data_and_exclude_fields(data, fields_to_exclude):
    """
    Collect data from a dictionary while excluding specified fields.

    Args:
        data (dict): The dictionary containing data.
        fields_to_exclude (list): A list of fields to exclude from the collected data.

    Returns:
        dict: A dictionary containing the collected data with specified fields excluded.
    """
    def collect_data(data, fields_to_exclude):
        return {key: value for key, value in data.items() if key not in fields_to_exclude}

    exclude_fields = functools.partial(
        collect_data, fields_to_exclude=fields_to_exclude)
    filtered_data = exclude_fields(data)
    return filtered_data
