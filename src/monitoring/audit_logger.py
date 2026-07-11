from pathlib import Path
from datetime import datetime, timezone
import pandas as pd


def log_ingestion_audit(
    table_name,
    source_path,
    record_count,
    status,
    start_time,
    end_time):

    duration_seconds = (
        end_time - start_time
    ).total_seconds()

    audit_record = {
        "run_id":
            datetime.now(timezone.utc)
            .strftime("%Y%m%d%H%M%S"),

        "table_name":
            table_name,

        "source_path":
            source_path,

        "record_count":
            record_count,

        "status":
            status,

        "start_time":
            start_time,

        "end_time":
            end_time,

        "duration_seconds":
            duration_seconds
    }

    audit_file = Path(
        "data/bronze/ingestion_audit.parquet"
    )

    if audit_file.exists():

        existing = pd.read_parquet(
            audit_file
        )

        updated = pd.concat(
            [
                existing,
                pd.DataFrame([audit_record])
            ],
            ignore_index=True
        )

    else:

        updated = pd.DataFrame(
            [audit_record]
        )

    updated.to_parquet(
        audit_file,
        index=False
    )