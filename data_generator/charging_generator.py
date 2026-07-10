from datetime import datetime, timedelta
from pathlib import Path
import random

import pandas as pd

# ----------------------------------
# Configuration
# ----------------------------------

CHARGING_STATIONS = [
    "BERLIN-001",
    "BERLIN-002",
    "MUNICH-001",
    "AMSTERDAM-001",
    "PARIS-001",
    "AUSTIN-001",
    "SHANGHAI-001"
]

CHARGER_TYPES = [
    "AC",
    "DC Fast",
    "Super Charger"
]

FAILURE_REASONS = [
    None,
    None,
    None,
    None,
    None,
    "Connector Failure",
    "Power Loss",
    "Payment Error",
    "Communication Timeout"
]


# ----------------------------------
# Helper Functions
# ----------------------------------

def generate_charging_session_id(index: int) -> str:
    return f"CHG{index:08d}"


def generate_session_time():
    start_date = datetime(2024, 1, 1)
    end_date = datetime.now()

    total_days = (end_date - start_date).days

    session_start = (
        start_date +
        timedelta(
            days=random.randint(0, total_days),
            hours=random.randint(0, 23),
            minutes=random.randint(0, 59)
        )
    )

    duration_minutes = random.randint(15, 180)

    session_end = session_start + timedelta(
        minutes=duration_minutes
    )

    return (
        session_start,
        session_end,
        duration_minutes
    )


# ----------------------------------
# Charging Generator
# ----------------------------------

def generate_charging_sessions(
    vehicles_df: pd.DataFrame
) -> pd.DataFrame:

    records = []

    session_counter = 1

    for _, vehicle in vehicles_df.iterrows():

        number_of_sessions = random.randint(
            5,
            50
        )

        for _ in range(number_of_sessions):

            (
                start_time,
                end_time,
                duration_minutes
            ) = generate_session_time()

            failure_reason = random.choice(
                FAILURE_REASONS
            )

            charging_failure = (
                failure_reason is not None
            )

            energy_used = round(
                random.uniform(5, 90),
                2
            )

            records.append({
                "charging_session_id":
                    generate_charging_session_id(
                        session_counter
                    ),
                "vehicle_id":
                    vehicle["vehicle_id"],
                "station_id":
                    random.choice(
                        CHARGING_STATIONS
                    ),
                "charger_type":
                    random.choice(
                        CHARGER_TYPES
                    ),
                "start_time":
                    start_time,
                "end_time":
                    end_time,
                "session_duration_minutes":
                    duration_minutes,
                "energy_used_kwh":
                    energy_used,
                "charging_failure_flag":
                    charging_failure,
                "failure_reason":
                    failure_reason,
                "created_at":
                    datetime.utcnow()
            })

            session_counter += 1

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
        "Generating charging sessions..."
    )

    charging_df = generate_charging_sessions(
        vehicles_df
    )

    output_path = Path(
        "sample_data/charging_sessions.parquet"
    )

    charging_df.to_parquet(
        output_path,
        index=False
    )

    print(
        f"Generated {len(charging_df)} "
        f"charging sessions"
    )

    print(
        f"Output saved to: "
        f"{output_path.resolve()}"
    )

    print("\nSample Records:")
    print(charging_df.head())


if __name__ == "__main__":
    main()