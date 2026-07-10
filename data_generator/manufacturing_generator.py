from datetime import datetime
from pathlib import Path
import random

import pandas as pd

# ----------------------------------
# Configuration
# ----------------------------------

SUPPLIERS = [
    "Bosch",
    "Continental",
    "Magna",
    "ZF",
    "Denso"
]

BATTERY_SUPPLIERS = [
    "CATL",
    "LG Energy",
    "Samsung SDI",
    "Panasonic",
    "Northvolt"
]

DEFECT_CODES = [
    None,
    None,
    None,
    None,
    None,
    "D001",
    "D002",
    "D003",
    "D004"
]

INSPECTION_STATUSES = [
    "PASS",
    "PASS",
    "PASS",
    "PASS",
    "PASS",
    "REWORK",
    "FAIL"
]

# ----------------------------------
# Manufacturing Data Generator
# ----------------------------------

def generate_manufacturing_data(
    vehicles_df: pd.DataFrame
) -> pd.DataFrame:

    records = []

    for _, vehicle in vehicles_df.iterrows():

        inspection_score = round(
            random.uniform(80, 100),
            2
        )

        defect_code = random.choice(
            DEFECT_CODES
        )

        inspection_status = random.choice(
            INSPECTION_STATUSES
        )

        records.append({
            "vehicle_id": vehicle["vehicle_id"],
            "vin": vehicle["vin"],
            "factory": vehicle["factory"],
            "production_date": vehicle["production_date"],
            "supplier": random.choice(SUPPLIERS),
            "battery_supplier": random.choice(
                BATTERY_SUPPLIERS
            ),
            "inspection_score": inspection_score,
            "inspection_status": inspection_status,
            "defect_code": defect_code,
            "manufacturing_timestamp":
                datetime.utcnow()
        })

    return pd.DataFrame(records)


# ----------------------------------
# Main
# ----------------------------------

def main():

    vehicle_path = Path(
        "sample_data/vehicles.parquet"
    )

    if not vehicle_path.exists():
        raise FileNotFoundError(
            "vehicles.parquet not found. "
            "Run vehicle_generator.py first."
        )

    print(
        "Reading vehicle master dataset..."
    )

    vehicles_df = pd.read_parquet(
        vehicle_path
    )

    print(
        f"Generating manufacturing records for "
        f"{len(vehicles_df)} vehicles..."
    )

    manufacturing_df = (
        generate_manufacturing_data(
            vehicles_df
        )
    )

    output_path = Path(
        "sample_data/manufacturing.parquet"
    )

    manufacturing_df.to_parquet(
        output_path,
        index=False
    )

    print(
        f"Generated "
        f"{len(manufacturing_df)} "
        f"manufacturing records"
    )

    print(
        f"Output saved: "
        f"{output_path.resolve()}"
    )

    print("\nSample Records:")
    print(
        manufacturing_df.head()
    )


if __name__ == "__main__":
    main()