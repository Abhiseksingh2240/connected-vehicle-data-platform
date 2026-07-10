from datetime import datetime, timedelta
from pathlib import Path
import random

import pandas as pd
from faker import Faker

fake = Faker()

# ----------------------------
# Configuration
# ----------------------------

COUNTRIES = [
    "Germany",
    "USA",
    "France",
    "Netherlands",
    "Sweden",
    "Norway"
]

OWNERSHIP_STATUS = [
    "ACTIVE",
    "TRANSFERRED",
    "LEASED"
]


# ----------------------------
# Helper Functions
# ----------------------------

def generate_customer_id(index: int) -> str:
    return f"CU{index:06d}"


def generate_purchase_date():
    start_date = datetime(2023, 1, 1)
    end_date = datetime.now()

    delta = end_date - start_date

    return (
        start_date +
        timedelta(days=random.randint(0, delta.days))
    ).date()


# ----------------------------
# Customer Generation
# ----------------------------

def generate_customers(vehicle_df: pd.DataFrame) -> pd.DataFrame:

    customers = []

    for idx, vehicle in vehicle_df.iterrows():

        customers.append({
            "customer_id": generate_customer_id(idx + 1),
            "vehicle_id": vehicle["vehicle_id"],
            "first_name": fake.first_name(),
            "last_name": fake.last_name(),
            "email": fake.email(),
            "phone_number": fake.phone_number(),
            "country": random.choice(COUNTRIES),
            "purchase_date": generate_purchase_date(),
            "ownership_status": random.choices(
                OWNERSHIP_STATUS,
                weights=[85, 5, 10],
                k=1
            )[0],
            "created_at": datetime.utcnow()
        })

    return pd.DataFrame(customers)


# ----------------------------
# Main
# ----------------------------

def main():

    vehicle_file = Path("sample_data/vehicles.parquet")

    if not vehicle_file.exists():
        raise FileNotFoundError(
            "vehicles.parquet not found. "
            "Run vehicle_generator.py first."
        )

    print("Reading vehicles dataset...")

    vehicle_df = pd.read_parquet(vehicle_file)

    print(
        f"Generating customers for "
        f"{len(vehicle_df)} vehicles..."
    )

    customer_df = generate_customers(vehicle_df)

    output_file = Path(
        "sample_data/customers.parquet"
    )

    customer_df.to_parquet(
        output_file,
        index=False
    )

    print(
        f"Generated {len(customer_df)} customers"
    )

    print(
        f"Output saved to: {output_file.resolve()}"
    )

    print("\nSample Records:")
    print(customer_df.head())


if __name__ == "__main__":
    main()

