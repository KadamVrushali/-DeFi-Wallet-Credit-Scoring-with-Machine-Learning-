import pandas as pd

def generate_features(filled_df: pd.DataFrame) -> pd.DataFrame:
    """
    Generate user-level features from filled wallet transactions.

    Args:
        filled_df (pd.DataFrame): DataFrame with filled 'amount_usd' and other transaction details.

    Returns:
        pd.DataFrame: Feature DataFrame grouped by 'userWallet'.
    """
    df = filled_df.copy()
    df["userWallet"] = df["userWallet"].str.lower().str.strip()

    features = pd.DataFrame()
    features["userWallet"] = df["userWallet"].unique()

    borrow = df[df["action"] == "borrow"].groupby("userWallet")["amount_usd"].sum().rename("total_borrowed_usd")
    repay = df[df["action"] == "repay"].groupby("userWallet")["amount_usd"].sum().rename("total_repaid_usd")
    borrow_count = df[df["action"] == "borrow"].groupby("userWallet")["amount_usd"].count().rename("borrow_count")
    repay_count = df[df["action"] == "repay"].groupby("userWallet")["amount_usd"].count().rename("repay_count")
    avg_borrow = df[df["action"] == "borrow"].groupby("userWallet")["amount_usd"].mean().rename("avg_borrow_usd")

    features = features.set_index("userWallet")
    features = features.join([borrow, repay, borrow_count, repay_count, avg_borrow])
    features = features.fillna(0).reset_index()

    print("✅ Features generated for", len(features), "wallets.")
    return features
