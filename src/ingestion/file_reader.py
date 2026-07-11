import pandas as pd


def read_file(config):

    fmt = config["file_format"]

    path = config["source_path"]

    if fmt == "parquet":
        return pd.read_parquet(path)

    if fmt == "csv":
        return pd.read_csv(path)

    raise ValueError(
        f"Unsupported format: {fmt}"
    )