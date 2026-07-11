from datetime import datetime
import sys

from src.metadata.config_loader import (
    load_config
)

from src.metadata.config_validator import (
    validate_config
)

from src.ingestion.file_reader import (
    read_file
)

from src.ingestion.audit import (
    add_audit_columns
)

from src.bronze.bronze_writer import (
    write_bronze
)

from src.monitoring.audit_logger import (
    log_ingestion_audit
)


def run_ingestion(
    config_path
):

    start_time = datetime.utcnow()

    try:

        config = load_config(
            config_path
        )

        validate_config(
            config
        )

        df = read_file(config)

        df = add_audit_columns(
            df,
            config["source_path"]
        )

        write_bronze(
            df,
            config["target_table"]
        )

        end_time = datetime.utcnow()

        log_ingestion_audit(
            table_name=config[
                "table_name"
            ],
            source_path=config[
                "source_path"
            ],
            record_count=len(df),
            status="SUCCESS",
            start_time=start_time,
            end_time=end_time
        )

        print(
            f"Successfully ingested "
            f"{config['table_name']}"
        )

    except Exception as ex:

        end_time = datetime.utcnow()

        log_ingestion_audit(
            table_name="UNKNOWN",
            source_path=config_path,
            record_count=0,
            status=f"FAILED: {ex}",
            start_time=start_time,
            end_time=end_time
        )

        raise


if __name__ == "__main__":

    if len(sys.argv) != 2:

        raise ValueError(
            "Usage: python ingest.py "
            "<yaml_config>"
        )

    run_ingestion(sys.argv[1])