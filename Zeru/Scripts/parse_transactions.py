# Scripts/parse_transactions.py

import json
import re
from pathlib import Path
from datetime import datetime, timezone

VALID_ACTIONS = ['deposit', 'borrow', 'repay', 'redeemunderlying', 'liquidationcall']

def parse_action_data(raw_str):
    try:
        if isinstance(raw_str, str):
            cleaned_str = re.sub(r"\\x[0-9a-fA-F]{2}", "", raw_str)
            cleaned_str = cleaned_str.replace("'", '"')
            cleaned_str = re.sub(r'(?<!\\)"', '"', cleaned_str)
            data = json.loads(cleaned_str)
        elif isinstance(raw_str, dict):
            data = raw_str
        else:
            return None, None, None

        symbol = data.get('assetSymbol')
        raw_amount = float(data.get('amount', 0))
        usd_price = float(data.get('assetPriceUSD', 1))

        decimals = 6 if symbol in ['USDC', 'USDT'] else 18
        amount_token = raw_amount / (10 ** decimals)
        amount_usd = amount_token * usd_price

        return symbol, amount_token, amount_usd
    except Exception:
        return None, None, None

def clean_transaction_data(input_path: str) -> list[dict]:
    with open(input_path, 'r') as f:
        transactions = json.load(f)

    cleaned = []

    for row in transactions:
        action = row.get('action', '').lower()
        if action not in VALID_ACTIONS:
            continue

        symbol, token_amt, usd_amt = parse_action_data(row.get('actionData'))
        timestamp = row.get('timestamp')

        try:
            timestamp = datetime.fromtimestamp(int(timestamp), tz=timezone.utc).isoformat()
        except Exception:
            timestamp = None

        cleaned.append({
            "userWallet": row.get("userWallet", "").lower().strip(),
            "action": action,
            "assetSymbol": symbol,
            "amount_token": token_amt,
            "amount_usd": usd_amt,
            "timestamp": timestamp
        })

    print(f"✅ Cleaned {len(cleaned)} transaction records.")
    return cleaned
