import pandas as pd

DOMESTIC_MERCHANTS = [
    "SWIGGY",
    "OLA",
    "IRCTC",
    "ZOMATO",
    "BIGBASKET"
]


def detect_amount_anomalies(df):

    grouped = df.groupby(
        "account_id"
    )

    for account_id, group in grouped:

        median_amount = (
            group["amount"]
            .median()
        )

        threshold = (
            median_amount * 3
        )

        anomalies = group[
            group["amount"] > threshold
        ]

        for idx in anomalies.index:

            df.loc[
                idx,
                "is_anomaly"
            ] = True

            existing_reason = (
                df.loc[
                    idx,
                    "anomaly_reason"
                ]
            )

            if pd.isna(
                existing_reason
            ):
                df.loc[
                    idx,
                    "anomaly_reason"
                ] = (
                    "Amount exceeds 3x median"
                )
            else:
                df.loc[
                    idx,
                    "anomaly_reason"
                ] = (
                    existing_reason
                    + " | "
                    + "Amount exceeds 3x median"
                )

    return df


def detect_currency_anomalies(df):

    for idx, row in df.iterrows():

        merchant = str(
            row["merchant"]
        ).upper()

        currency = str(
            row["currency"]
        ).upper()

        if (
            merchant in DOMESTIC_MERCHANTS
            and
            currency == "USD"
        ):

            df.loc[
                idx,
                "is_anomaly"
            ] = True

            if pd.isna(
                df.loc[idx, "anomaly_reason"]
            ):
                df.loc[
                    idx,
                    "anomaly_reason"
                ] = (
                    "Domestic merchant using USD"
                )
            else:
                df.loc[
                    idx,
                    "anomaly_reason"
                ] += (
                    "; Domestic merchant using USD"
                )

    return df


def detect_anomalies(df):

    required_columns = {
        "account_id",
        "amount",
        "merchant",
        "currency"
    }

    missing_columns = (
        required_columns
        - set(df.columns)
    )

    if missing_columns:
        raise ValueError(
            f"Missing columns: {missing_columns}"
        )

    df["is_anomaly"] = False

    df["anomaly_reason"] = None

    df = detect_amount_anomalies(
        df
    )

    df = detect_currency_anomalies(
        df
    )

    return df

