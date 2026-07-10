import pandas as pd

from data_generator.telemetry_generator import (
    generate_vehicle_events,
    generate_location,
    create_failure_scenario
)


# ----------------------------------
# Fixtures
# ----------------------------------

def sample_vehicle_df():
    return pd.DataFrame([
        {
            "vehicle_id": "VH000001",
            "factory": "Berlin"
        },
        {
            "vehicle_id": "VH000002",
            "factory": "Munich"
        }
    ])


# ----------------------------------
# Location Tests
# ----------------------------------

def test_generate_location_returns_coordinates():

    lat, lon = generate_location("Berlin")

    assert isinstance(lat, float)
    assert isinstance(lon, float)

    assert -90 <= lat <= 90
    assert -180 <= lon <= 180


# ----------------------------------
# Failure Scenario Tests
# ----------------------------------

def test_failure_scenario_returns_valid_value():

    valid_scenarios = {
        "NORMAL",
        "LOW_BATTERY",
        "OVERHEAT",
        "LOW_TIRE",
        "BRAKE_FAULT"
    }

    scenario = create_failure_scenario()

    assert scenario in valid_scenarios


# ----------------------------------
# Telemetry Generation Tests
# ----------------------------------

def test_generate_vehicle_events_row_count():

    vehicles_df = sample_vehicle_df()

    events_per_vehicle = 100

    telemetry_df = generate_vehicle_events(
        vehicles_df,
        events_per_vehicle=events_per_vehicle
    )

    expected_rows = (
        len(vehicles_df) * events_per_vehicle
    )

    assert len(telemetry_df) == expected_rows


def test_required_columns_exist():

    vehicles_df = sample_vehicle_df()

    telemetry_df = generate_vehicle_events(
        vehicles_df,
        events_per_vehicle=10
    )

    expected_columns = {
        "event_id",
        "vehicle_id",
        "event_timestamp",
        "latitude",
        "longitude",
        "speed",
        "battery_level",
        "battery_temperature",
        "engine_temperature",
        "tire_pressure",
        "brake_status",
        "odometer",
        "diagnostic_code",
        "created_at"
    }

    assert expected_columns.issubset(
        telemetry_df.columns
    )


def test_vehicle_ids_are_preserved():

    vehicles_df = sample_vehicle_df()

    telemetry_df = generate_vehicle_events(
        vehicles_df,
        events_per_vehicle=10
    )

    generated_vehicle_ids = set(
        telemetry_df["vehicle_id"].unique()
    )

    expected_vehicle_ids = set(
        vehicles_df["vehicle_id"]
    )

    assert generated_vehicle_ids == expected_vehicle_ids


def test_event_ids_are_unique():

    vehicles_df = sample_vehicle_df()

    telemetry_df = generate_vehicle_events(
        vehicles_df,
        events_per_vehicle=100
    )

    assert telemetry_df["event_id"].is_unique


def test_battery_level_range():

    vehicles_df = sample_vehicle_df()

    telemetry_df = generate_vehicle_events(
        vehicles_df,
        events_per_vehicle=100
    )

    assert (
        telemetry_df["battery_level"] >= 0
    ).all()

    assert (
        telemetry_df["battery_level"] <= 100
    ).all()


def test_speed_range():

    vehicles_df = sample_vehicle_df()

    telemetry_df = generate_vehicle_events(
        vehicles_df,
        events_per_vehicle=100
    )

    assert (
        telemetry_df["speed"] >= 0
    ).all()

    assert (
        telemetry_df["speed"] <= 180
    ).all()


def test_positive_tire_pressure():

    vehicles_df = sample_vehicle_df()

    telemetry_df = generate_vehicle_events(
        vehicles_df,
        events_per_vehicle=100
    )

    assert (
        telemetry_df["tire_pressure"] > 0
    ).all()


def test_odometer_non_negative():

    vehicles_df = sample_vehicle_df()

    telemetry_df = generate_vehicle_events(
        vehicles_df,
        events_per_vehicle=100
    )

    assert (
        telemetry_df["odometer"] >= 0
    ).all()


def test_timestamps_not_null():

    vehicles_df = sample_vehicle_df()

    telemetry_df = generate_vehicle_events(
        vehicles_df,
        events_per_vehicle=100
    )

    assert telemetry_df[
        "event_timestamp"
    ].notna().all()


def test_created_at_not_null():

    vehicles_df = sample_vehicle_df()

    telemetry_df = generate_vehicle_events(
        vehicles_df,
        events_per_vehicle=100
    )

    assert telemetry_df[
        "created_at"
    ].notna().all()