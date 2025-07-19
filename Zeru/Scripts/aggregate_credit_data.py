import json
from collections import defaultdict
import pandas as pd

# Load JSON file (cleaned transaction data with USD values)
with open("Data/wallet_transactions_with_usd.json", "r") as f:
    transactions = json.load(f)

# Aggregate credit data at user level
user_stats = defaultdict(lambda: {
    "total_deposit_usd": 0.0,
    "total_borrow_usd": 0.0,
    "total_repay_usd": 0.0,
    "total_redeem_usd": 0.0,
    "tx_count": 0
})

for tx in transactions:
    wallet = tx.get("userWallet")
    action = tx.get("action", "").lower()
    usd = tx.get("amount_usd", 0.0) or 0.0

    if action == "deposit":
        user_stats[wallet]["total_deposit_usd"] += usd
    elif action == "borrow":
        user_stats[wallet]["total_borrow_usd"] += usd
    elif action == "repay":
        user_stats[wallet]["total_repay_usd"] += usd
    elif action in ["redeemunderlying", "withdraw"]:
        user_stats[wallet]["total_redeem_usd"] += usd

    user_stats[wallet]["tx_count"] += 1

# Convert to list of records for DataFrame export
aggregated_data = [
    {"userWallet": wallet, **stats} for wallet, stats in user_stats.items()
]

# Save aggregated stats as JSON
with open("Data/aggregated_credit_data.json", "w") as f:
    json.dump(aggregated_data, f, indent=2)

# Optional: Also convert to DataFrame for manual inspection or future CSV output
df = pd.DataFrame(aggregated_data)
print(df.head())
