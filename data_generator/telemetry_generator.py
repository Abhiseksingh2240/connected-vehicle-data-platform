from datetime import datetime, timedelta
from pathlib import Path
import random

import pandas as pd

# ----------------------------------
# Configuration
# ----------------------------------

DIAGNOSTIC_CODES = [
    None,
    None,
    None,
    None,
    "P1001",  # Battery issue
    "P2005",  # Brake issue
    "P3002",  # Tire issue
    "P4500"   # Engine issue
]

BRAKE_STATUS = [
    "NORMAL",
    "NORMAL",
    "NORMAL",
    "APPLIED",
    "ABS_ACTIVE"
]

# Approximate locations
FACTORY_LOCATIONS = {
    "Berlin": (52.5200, 13.4050),
    "Munich": (48.1351, 11.5820),
    "Austin": (30.2672, -97.7431),
    "Shanghai": (31.2304, 121.4737)
}

# ----------------------------------
# Helper Functions
# ----------------------------------

def generate_event_timestamp(start_time, sequence):
    return start_time + timedelta(minutes=sequence)


def generate_location(factory):
    base_lat, base_lon = FACTORY_LOCATIONS.get(
        factory,
        (52.5200, 13.4050)
    )

    return (
        round(base_lat + random.uniform(-0.05, 0.05), 6),
        round(base_lon + random.uniform(-0.05, 0.05), 6)
    )


def create_failure_scenario():
    """
    Randomly inject failure conditions.
    """

    scenario = random.choices(
        [
            "NORMAL",
            "LOW_BATTERY",
            "OVERHEAT",
            "LOW_TIRE",
            "BRAKE_FAULT"
        ],
        weights=[75, 8, 5, 7, 5],
        k=1
    )[0]

    return scenario


# ----------------------------------
# Telemetry Generator
# ----------------------------------

def generate_vehicle_events(
    vehicles_df,
    events_per_vehicle=1000
):

    records = []

    start_time = datetime.now() - timedelta(days=7)

    for _, vehicle in vehicles_df.iterrows():

        odometer = random.randint(
            5000,
            120000
        )

        for event_num in range(events_per_vehicle):

            scenario = create_failure_scenario()

            battery_level = random.uniform(
                20,
                100
            )

            engine_temperature = random.uniform(
                75,
                100
            )

            tire_pressure = random.uniform(
                30,
                38
            )

            brake_status = random.choice(
                BRAKE_STATUS
            )

            diagnostic_code = None

            # ------------------
            # Failure Simulation
            # ------------------

            if scenario == "LOW_BATTERY":
                battery_level = random.uniform(
                    1,
                    15
                )
                diagnostic_code = "P1001"

            elif scenario == "OVERHEAT":
                engine_temperature = random.uniform(
                    110,
                    140
                )
                diagnostic_code = "P4500"

            elif scenario == "LOW_TIRE":
                tire_pressure = random.uniform(
                    18,
                    28
                )
                diagnostic_code = "P3002"

            elif scenario == "BRAKE_FAULT":
                brake_status = "ABS_ACTIVE"
                diagnostic_code = "P2005"

            speed = round(
                random.uniform(0, 180),
                2
            )

            battery_temperature = round(
                random.uniform(15, 55),
                2
            )

            latitude, longitude = generate_location(
                vehicle["factory"]
            )

            event_timestamp = (
                generate_event_timestamp(
                    start_time,
                    event_num
                )
            )

            odometer += random.randint(
                0,
                3
            )

            records.append({
                "event_id":
                    f"E{vehicle['vehicle_id']}_{event_num}",
                "vehicle_id":
                    vehicle["vehicle_id"],
                "event_timestamp":
                    event_timestamp,

                "latitude":
                    latitude,

                "longitude":
                    longitude,

                "speed":
                    speed,

                "battery_level":
                    round(
                        battery_level,
                        2
                    ),

                "battery_temperature":
                    battery_temperature,

                "engine_temperature":
                    round(
                        engine_temperature,
                        2
                    ),

                "tire_pressure":
                    round(
                        tire_pressure,
                        2
                    ),

                "brake_status":
                    brake_status,

                "odometer":
                    odometer,

                "diagnostic_code":
                    diagnostic_code,

                "created_at":
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
        "Reading vehicle master data..."
    )

    vehicles_df = pd.read_parquet(
        vehicle_path
    )

    print(
        "Generating telemetry events..."
    )

    telemetry_df = generate_vehicle_events(
        vehicles_df,
        events_per_vehicle=1000
    )

    output_path = Path(
        "sample_data/vehicle_events.parquet"
    )

    telemetry_df.to_parquet(
        output_path,
        index=False
    )

    print(
        f"Generated {len(telemetry_df)} "
        f"telemetry events"
    )

    print(
        f"Output saved to: "
        f"{output_path.resolve()}"
    )

    print("\nSample Records:")
    print(
        telemetry_df.head()
    )


if __name__ == "__main__":
    main()