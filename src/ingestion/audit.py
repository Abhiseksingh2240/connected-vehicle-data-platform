from datetime import datetime, timezone
import uuid


def add_audit_columns(
    dataframe,
    source_file: str
):

    dataframe["ingestion_timestamp"] = \
        datetime.now(timezone.utc)

    dataframe["source_file"] = source_file

    dataframe["batch_id"] = \
        str(uuid.uuid4())

    return dataframe