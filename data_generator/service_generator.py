from datetime import datetime, timedelta
from pathlib import Path
import random

import pandas as pd

# ----------------------------------
# Configuration
# ----------------------------------

SERVICE_TYPES = [
    "Preventive Maintenance",
    "Battery Inspection",
    "Software Upgrade",
    "Brake Replacement",
    "Tire Replacement",
    "Cooling System Repair",
    "Diagnostic Check",
    "Motor Inspection"
]

SERVICE_CENTERS = [
    "Berlin Service Center",
    "Munich Service Center",
    "Austin Service Center",
    "Shanghai Service Center",
    "Amsterdam Service Center",
    "Paris Service Center"
]

PARTS = [
    "Brake Pads",
    "Battery Module",
    "Tire",
    "Coolant Pump",
    "Control Unit",
    "Charging Port",
    "Motor Assembly",
    "Temperature Sensor"
]


# ----------------------------------
# Helper Functions
# ----------------------------------

def generate_service_id(index: int) -> str:
    return f"SRV{index:08d}"


def generate_service_date():
    start_date = datetime(2023, 1, 1)
    end_date = datetime.now()

    delta = end_date - start_date

    return (
        start_date +
        timedelta(days=random.randint(0, delta.days))
    ).date()


# ----------------------------------
# Service Generator
# ----------------------------------

def generate_service_history(
    vehicles_df: pd.DataFrame
) -> pd.DataFrame:

    records = []

    service_counter = 1

    for _, vehicle in vehicles_df.iterrows():

        # Generate between 0 and 5 service visits
        number_of_services = random.randint(0, 5)

        for _ in range(number_of_services):

            service_type = random.choice(
                SERVICE_TYPES
            )

            repair_cost = round(
                random.uniform(50, 3500),
                2
            )

            warranty_claim = random.choices(
                [True, False],
                weights=[20, 80],
                k=1
            )[0]

            parts_replaced = ", ".join(
                random.sample(
                    PARTS,
                    k=random.randint(1, 3)
                )
            )

            service_date = generate_service_date()

            records.append({
                "service_id":
                    generate_service_id(
                        service_counter
                    ),
                "vehicle_id":
                    vehicle["vehicle_id"],
                "service_date":
                    service_date,
                "service_type":
                    service_type,
                "service_center":
                    random.choice(
                        SERVICE_CENTERS
                    ),
                "repair_cost":
                    repair_cost,
                "parts_replaced":
                    parts_replaced,
                "warranty_claim":
                    warranty_claim,
                "service_duration_hours":
                    round(
                        random.uniform(
                            0.5,
                            10.0
                        ),
                        1
                    ),
                "technician_id":
                    f"TECH{random.randint(1000,9999)}",
                "created_at":
                    datetime.utcnow()
            })

            service_counter += 1

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
        "Reading vehicle master data..."
    )

    vehicles_df = pd.read_parquet(
        vehicle_path
    )

    print(
        "Generating service history..."
    )

    service_df = generate_service_history(
        vehicles_df
    )

    output_path = Path(
        "sample_data/service_history.parquet"
    )

    service_df.to_parquet(
        output_path,
        index=False
    )

    print(
        f"Generated "
        f"{len(service_df)} service records"
    )

    print(
        f"Output saved to: "
        f"{output_path.resolve()}"
    )

    print("\nSample Records:")
    print(
        service_df.head()
    )


if __name__ == "__main__":
    main()