import pandas as pd

def create_wallet_labels(transactions: list) -> pd.DataFrame:
    """
    Generates wallet-level labels (repayment_ratio and binary label) from transactions.

    Args:
        transactions (list): List of dicts, each representing a transaction.

    Returns:
        pd.DataFrame: DataFrame with columns: userWallet, repayment_ratio, label
    """
    df = pd.DataFrame(transactions)

    if df.empty or "userWallet" not in df.columns or "repayAmountUSD" not in df.columns:
        raise ValueError("Invalid transaction data. 'userWallet' and 'repayAmountUSD' required.")

    df["amountUSD"] = pd.to_numeric(df["amountUSD"], errors="coerce")
    df["repayAmountUSD"] = pd.to_numeric(df["repayAmountUSD"], errors="coerce")

    grouped = df.groupby("userWallet").agg(
        total_amount=("amountUSD", "sum"),
        total_repaid=("repayAmountUSD", "sum")
    )

    grouped["repayment_ratio"] = grouped["total_repaid"] / grouped["total_amount"]
    grouped["repayment_ratio"] = grouped["repayment_ratio"].fillna(0)

    grouped["label"] = (grouped["repayment_ratio"] >= 1.0).astype(int)

    result = grouped[["repayment_ratio", "label"]].reset_index()

    print(f"✅ Created labels for {len(result)} wallets.")
    return result
