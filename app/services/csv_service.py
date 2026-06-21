import pandas as pd


def load_csv(file_path):

    df = pd.read_csv(file_path)

    return df

def normalize_dates(df):

    df["date"] = pd.to_datetime(
        df["date"],
        errors="coerce"
    )

    df["date"] = df["date"].dt.strftime(
        "%Y-%m-%d"
    )

    return df

def clean_amounts(df):

    df["amount"] = (
        df["amount"]
        .astype(str)
        .str.replace(
            r"[^\d.]",
            "",
            regex=True
        )
    )

    df["amount"] = df["amount"].astype(float)

    return df

def normalize_status(df):

    df["status"] = (
        df["status"]
        .astype(str)
        .str.upper()
    )

    return df

def fill_missing_category(df):

    df["category"] = (
        df["category"]
        .fillna("Uncategorised")
    )

    return df

def remove_duplicates(df):

    df = df.drop_duplicates()

    return df

def clean_csv(file_path):

    df = load_csv(file_path)

    raw_count = len(df)

    df = normalize_dates(df)

    df = clean_amounts(df)

    df = normalize_status(df)

    df = fill_missing_category(df)

    df = remove_duplicates(df)

    clean_count = len(df)

    return (
        df,
        raw_count,
        clean_count
    )