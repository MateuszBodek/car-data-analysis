"""SQL queries for creating table and inserting data, meant for use in the first,
preliminary data exploration after web scraping."""

import sqlite3
import pandas as pd

technical_data_table_create_query = """
CREATE TABLE IF NOT EXISTS car_tech_specs (
    car_id INTEGER NOT NULL PRIMARY KEY,
    brand TEXT NOT NULL,
    model TEXT NOT NULL,
    generation TEXT NOT NULL,
    body_type TEXT NOT NULL,
    engine TEXT NOT NULL,
    number_of_doors INTEGER,
    number_of_seats INTEGER,
    turning_diameter_m REAL,
    turning_radius_m REAL,
    length REAL,
    width_with_mirrors REAL,
    height REAL,
    wheelbase REAL,
    front_track_width REAL,
    rear_track_width REAL,
    front_overhang REAL,
    rear_overhang REAL,
    ground_clearance REAL,
    front_seat_to_roof_distance REAL,
    rear_seat_to_roof_distance REAL,
    front_width_above_armrests REAL,
    rear_width_above_armrests REAL,
    max_trunk_capacity_folded REAL,
    min_trunk_capacity_unfolded REAL,
    engine_displacement REAL,
    engine_type TEXT,
    max_torque REAL,
    engine_mounting TEXT,
    turbocharging TEXT,
    camshaft_location TEXT,
    number_of_cylinders INTEGER,
    cylinder_layout TEXT,
    number_of_valves INTEGER,
    compression_ratio_to_1 REAL,
    ignition_type TEXT,
    fuel_injection_type TEXT,
    steering_system_type TEXT,
    front_brake_type TEXT,
    rear_brake_type TEXT,
    front_suspension_type TEXT,
    rear_suspension_type TEXT,
    shock_absorbers TEXT,
    automatic_gear_count INTEGER,
    drive_type TEXT,
    gearbox_name TEXT,
    top_speed REAL,
    acceleration_0_100 REAL,
    avg_fuel_consumption_combined REAL,
    fuel_consumption_highway REAL,
    fuel_consumption_city REAL,
    fuel_tank_capacity REAL,
    range_combined REAL,
    range_highway REAL,
    range_city REAL,
    co2_emissions_g_per_km REAL,
    emission_standard TEXT,
    curb_weight_min REAL,
    start_stop_system BOOLEAN,
    front_brake_disc_diameter REAL,
    rear_brake_disc_diameter REAL,
    manual_gear_count INTEGER,
    clutch_type TEXT,
    width REAL,
    gross_vehicle_weight REAL,
    roof_load_limit REAL,
    max_trailer_weight_braked REAL,
    max_trailer_weight_unbraked REAL,
    engine_code TEXT,
    bolt_pattern TEXT,
    max_towbar_load REAL,
    approach_angle_deg REAL,
    departure_angle_deg REAL,
    front_armrest_width REAL,
    rear_armrest_width REAL,
    width_between_wheel_arches REAL,
    cargo_length_to_rear_seat REAL,
    loading_sill_height REAL,
    trunk_width REAL,
    trunk_height REAL,
    cargo_length_with_rear_seats_folded REAL,
    distance_front_seat_to_engine_bay REAL,
    front_seat_cushion_length REAL,
    distance_between_front_and_rear_seats REAL,
    rear_seat_cushion_length REAL,
    total_cabin_length REAL,
    width_with_folded_mirrors REAL,
    battery_capacity_ah REAL,
    length_with_towbar REAL,
    height_with_roof_rails REAL,
    ground_clearance_4x4 REAL,
    wading_depth REAL,
    height_with_tailgate_open REAL,
    breakover_angle_deg REAL,
    max_payload REAL,
    front_seatback_to_steering_wheel_distance REAL,
    cargo_bay_length REAL,
    cargo_bay_width REAL,
    cargo_bay_height REAL,
    manual_gearbox_available BOOLEAN,
    automatic_gearbox_available BOOLEAN,
    production_start_year INTEGER,
    production_end_year INTEGER,
    max_hp REAL,
    max_hp_rpm REAL,
    piston_bore_mm REAL,
    piston_stroke_mm REAL
);
"""

tire_specs_data_create_query = """
CREATE TABLE IF NOT EXISTS tire_specs (
    tire_id INTEGER PRIMARY KEY AUTOINCREMENT,
    car_id INTEGER NOT NULL,
    brand TEXT NOT NULL,
    model TEXT NOT NULL,
    generation TEXT NOT NULL,
    body_type TEXT NOT NULL,
    engine TEXT NOT NULL,
    tire_width REAL,
    side_profile REAL,
    wheel_size REAL,
    is_standard BOOLEAN,
    FOREIGN KEY (car_id)
        REFERENCES car_specs (car_id)
        ON UPDATE CASCADE
        ON DELETE CASCADE
);
"""

wheel_specs_data_create_query = """
CREATE TABLE IF NOT EXISTS wheel_specs (
    wheel_id INTEGER PRIMARY KEY AUTOINCREMENT,
    car_id INTEGER NOT NULL,
    brand TEXT NOT NULL,
    model TEXT NOT NULL,
    generation TEXT NOT NULL,
    body_type TEXT NOT NULL,
    engine TEXT NOT NULL,
    bolt_pattern TEXT,
    rim_width TEXT,
    rim_size TEXT,
    is_standard BOOLEAN,
    FOREIGN KEY (car_id)
        REFERENCES car_specs (car_id)
        ON UPDATE CASCADE
        ON DELETE CASCADE
);
"""

ratings_data_create_query = """
CREATE TABLE IF NOT EXISTS car_ratings (
    brand TEXT NOT NULL,
    model TEXT NOT NULL,
    generation TEXT NOT NULL,
    new_price REAL,
    avg_rating REAL,
    buy_again REAL,
    overall_rating REAL,
    engine REAL,
    gearbox REAL,
    drivetrain REAL,
    body REAL,
    visibility REAL,
    ergonomy REAL,
    climate_control REAL,
    sound_insulation REAL,
    interior_space REAL,
    maintenance_costs REAL,
    quality_price_ratio REAL,
    reliability_small_repairs REAL,
    reliability_major_repairs REAL,
    PRIMARY KEY (brand, model, generation),
    FOREIGN KEY (brand, model, generation)
        REFERENCES car_specs (brand, model, generation)
        ON UPDATE CASCADE
        ON DELETE CASCADE
);
"""

def connect() -> sqlite3.Connection | sqlite3.Cursor:
    conn = sqlite3.connect('../data/cars.db')
    cur = conn.cursor()
    return conn, cur


def create_table(cur: sqlite3.Cursor, create_table_query: str) -> None:
    cur.execute(create_table_query)
    print("Table created successfully")


def insert_data(conn: sqlite3.Connection, df: pd.DataFrame, table_name: str) -> None:
        df.to_sql(table_name, conn, if_exists='append', index=False)
        print(f"Inserted {len(df)} records into {table_name} table")
