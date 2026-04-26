import pandas as pd


def load_and_clean(filepath: str) -> pd.DataFrame:
    df = pd.read_csv(filepath)

    # Fix column names
    df.columns = [c.strip().lower().replace("-", "_") for c in df.columns]

    # Print columns for debugging
    print("Columns:", df.columns.tolist())

    # Rename target column — handle all possible spellings
    rename_map = {}
    for col in df.columns:
        if "show" in col.lower():
            rename_map[col] = "no_show"
        if col == "hipertension":
            rename_map[col] = "hypertension"
        if col == "handcap":
            rename_map[col] = "handicap"
        if col == "scheduledday":
            rename_map[col] = "scheduled_day"
        if col == "appointmentday":
            rename_map[col] = "appointment_day"
        if col == "patientid":
            rename_map[col] = "patient_id"
        if col == "appointmentid":
            rename_map[col] = "appointment_id"

    df = df.rename(columns=rename_map)

    # Fix target column
    df["no_show"] = df["no_show"].map({"Yes": 1, "No": 0})

    # Fix bad ages
    df = df[df["age"] >= 0]
    df = df[df["age"] <= 115]

    # Convert dates
    df["scheduled_day"] = pd.to_datetime(df["scheduled_day"], utc=True)
    df["appointment_day"] = pd.to_datetime(df["appointment_day"], utc=True)

    # Feature 1: days in advance
    df["days_in_advance"] = (
        df["appointment_day"] - df["scheduled_day"]
    ).dt.days

    # Remove negative days
    df = df[df["days_in_advance"] >= 0]

    # Feature 2: appointment day of week
    df["appt_day_of_week"] = df["appointment_day"].dt.dayofweek

    return df


def get_features_and_target(df: pd.DataFrame):
    feature_cols = [
        "age",
        "scholarship",
        "hypertension",
        "diabetes",
        "alcoholism",
        "handicap",
        "sms_received",
        "days_in_advance",
        "appt_day_of_week",
    ]
    X = df[feature_cols]
    y = df["no_show"]
    return X, y