from pathlib import Path


def write_bronze(
    dataframe,
    target_table: str
):

    output_dir = Path("data/bronze")

    output_dir.mkdir(
        parents=True,
        exist_ok=True
    )

    output_path = output_dir / f"{target_table}.parquet"

    dataframe.to_parquet(
        output_path,
        index=False
    )

    return output_path