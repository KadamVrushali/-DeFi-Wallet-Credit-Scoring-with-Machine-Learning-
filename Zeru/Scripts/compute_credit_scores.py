import pandas as pd
import numpy as np

def compute_credit_scores(final_df: pd.DataFrame) -> pd.DataFrame:
    """
    Computes a credit score for each wallet based on repayment ratio and transaction features.

    Args:
        final_df (pd.DataFrame): DataFrame with features + 'repayment_ratio'

    Returns:
        pd.DataFrame: DataFrame with additional 'credit_score' column
    """
    if 'repayment_ratio' not in final_df.columns:
        raise ValueError("Input DataFrame must include 'repayment_ratio'.")

    # Normalize repayment ratio to be between 0 and 1
    repayment = final_df['repayment_ratio'].clip(0, 1)

    # Optionally scale features
    tx_count = np.log1p(final_df['total_tx_count'])
    avg_tx = np.log1p(final_df['avg_usd_tx'])

    # Compute score: base + weighted sum
    final_df['credit_score'] = (
        300 +                 # base
        400 * repayment +     # repayment impact
        100 * tx_count / tx_count.max() +   # tx activity
        100 * avg_tx / avg_tx.max()         # avg tx size
    ).round(2)

    print("✅ Credit scores computed for all wallets.")
    return final_df
