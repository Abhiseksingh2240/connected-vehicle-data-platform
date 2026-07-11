REQUIRED_FIELDS = [
    "table_name",
    "source_path",
    "file_format",
    "load_type",
    "primary_key",
    "target_table"
]


def validate_config(config):

    if config is None:
        raise ValueError(
            "Configuration cannot be None"
        )

    missing_fields = []

    for field in REQUIRED_FIELDS:
        if field not in config:
            missing_fields.append(field)

    if missing_fields:
        raise ValueError(
            f"Missing fields: {missing_fields}"
        )

    return True