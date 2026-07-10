from datetime import datetime, timedelta
from pathlib import Path
import random
import uuid

import pandas as pd

# ----------------------------
# Configuration
# ----------------------------

NUM_VEHICLES = 100

MODELS = [
    "EV-X",
    "EV-S",
    "EV-PRO",
    "EV-ULTRA"
]

BATTERY_TYPES = [
    "LFP",
    "NMC"
]

FACTORIES = [
    "Berlin",
    "Munich",
    "Austin",
    "Shanghai"
]

VEHICLE_STATUSES = (
    ["ACTIVE"] * 90
    + ["SERVICE"] * 8
    + ["INACTIVE"] * 2
)

COLORS = [
    "Black",
    "White",
    "Blue",
    "Silver",
    "Red",
    "Gray"
]

COUNTRIES = [
    "Germany",
    "USA",
    "France",
    "Netherlands",
    "Sweden",
    "Norway"
]


# ----------------------------
# Helper Functions
# ----------------------------

def generate_vehicle_id(index: int) -> str:
    return f"VH{index:06d}"


def generate_vin() -> str:
    """
    Simplified VIN generator.
    """
    return str(uuid.uuid4()).replace("-", "").upper()[:17]


def generate_production_date():
    start_date = datetime(2023, 1, 1)
    end_date = datetime(2026, 1, 1)

    delta = end_date - start_date

    return (
        start_date +
        timedelta(days=random.randint(0, delta.days))
    ).date()


# ----------------------------
# Data Generation
# ----------------------------

def generate_vehicle_data(
        num_vehicles: int = NUM_VEHICLES
) -> pd.DataFrame:

    records = []

    used_vins = set()

    for i in range(1, num_vehicles + 1):

        vin = generate_vin()

        while vin in used_vins:
            vin = generate_vin()

        used_vins.add(vin)

        production_date = generate_production_date()

        record = {
            "vehicle_id": generate_vehicle_id(i),
            "vin": vin,
            "model": random.choice(MODELS),
            "model_year": production_date.year,
            "battery_type": random.choice(BATTERY_TYPES),
            "factory": random.choice(FACTORIES),
            "production_date": production_date,
            "vehicle_status": random.choice(VEHICLE_STATUSES),
            "color": random.choice(COLORS),
            "country": random.choice(COUNTRIES),
            "created_at": datetime.utcnow()
        }

        records.append(record)

    return pd.DataFrame(records)


# ----------------------------
# Main
# ----------------------------

def main():

    print("Generating vehicle master data...")

    df = generate_vehicle_data(NUM_VEHICLES)

    output_dir = Path("sample_data")
    output_dir.mkdir(exist_ok=True)

    output_path = output_dir / "vehicles.parquet"

    df.to_parquet(
        output_path,
        index=False
    )

    print(f"Generated {len(df)} vehicles")
    print(f"Output: {output_path.resolve()}")

    print("\nSample Data:")
    print(df.head())


if __name__ == "__main__":
    main()
