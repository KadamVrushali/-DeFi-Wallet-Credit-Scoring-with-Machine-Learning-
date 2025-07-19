import pandas as pd

def engineer_features(transactions: list) -> pd.DataFrame:
    """
    Creates wallet-level features from enriched transaction data.

    Args:
        transactions (list): List of transaction dictionaries with 'amountUSD' field.

    Returns:
        pd.DataFrame: A dataframe with aggregated features for each userWallet.
    """
    df = pd.DataFrame(transactions)

    # Basic sanity check
    if df.empty or "userWallet" not in df.columns:
        raise ValueError("Invalid or empty transaction data.")

    # Convert amountUSD safely
    df["amountUSD"] = pd.to_numeric(df["amountUSD"], errors="coerce")

    # Group by userWallet and compute aggregate features
    agg_df = df.groupby("userWallet").agg(
        total_tx_count=("hash", "count"),
        total_usd_amount=("amountUSD", "sum"),
        avg_usd_tx=("amountUSD", "mean"),
        max_usd_tx=("amountUSD", "max"),
        min_usd_tx=("amountUSD", "min")
    ).reset_index()

    print(f"✅ Engineered features for {len(agg_df)} wallets.")
    return agg_df
