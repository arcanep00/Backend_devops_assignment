from app.models.Transaction import Transaction

def save_transactions(
        db,
        job_id,
        df
):
    for _, row in df.iterrows():
        txn = Transaction(
            job_id=job_id,

            txn_id=row["txn_id"],

            date=row["date"],

            merchant=row["merchant"],

            amount=row["amount"],

            currency=row["currency"],

            status=row["status"],

            category=row["category"],

            account_id=row["account_id"],

            is_anomaly=row["is_anomaly"],

            anomaly_reason=row[
                "anomaly_reason"
            ]
        )

        db.add(txn)

    db.commit()