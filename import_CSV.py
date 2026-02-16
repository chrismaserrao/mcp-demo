import pandas as pd
from database import init_db, insert_transaction

# Change this if your file has a different name
CSV_FILE = r"C:\Users\chris\Downloads\archive\aug_personal_transactions_with_UserId.csv"
USER_ID = "user1"  

def import_csv():
    init_db()

    df = pd.read_csv(CSV_FILE)

    # Ensure column names match your dataset
    required_columns = [
        "User ID",
        "Date",
        "Description",
        "Amount",
        "Transaction Type",
        "Category",
        "Account Name"
    ]

    for col in required_columns:
        if col not in df.columns:
            raise Exception(f"Missing column: {col}")

    for _, row in df.iterrows():
        insert_transaction(
            user_id=str(row["User ID"]),
            date=str(row["Date"]),
            description=str(row["Description"]),
            amount=float(row["Amount"]),
            transaction_type=str(row["Transaction Type"]).lower(),
            category=str(row["Category"]),
            account_name=str(row["Account Name"])
        )

    print("CSV import complete.")


if __name__ == "__main__":
    import_csv()
