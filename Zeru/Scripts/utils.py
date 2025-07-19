# scripts/utils.py

from decimal import Decimal
import numpy as np

def convert_token_amount_to_usd(amount_str, symbol, price_str):
    try:
        amount = Decimal(amount_str)
        price = Decimal(price_str)
        if symbol.lower() in ["usdc", "usdt", "dai"]:
            return float(amount) / 1e6 * float(price)
        else:
            return float(amount) / 1e18 * float(price)
    except:
        return None

def parse_transaction(txn):
    return {
        "userWallet": txn["userWallet"],
        "timestamp": txn["timestamp"],
        "action": txn["action"],
        "amount": txn["actionData"].get("amount"),
        "assetSymbol": txn["actionData"].get("assetSymbol"),
        "assetPriceUSD": txn["actionData"].get("assetPriceUSD"),
        "amountUSD": None  # Will be filled later
    }

def create_wallet_features(wallet_address, txns):
    deposits = [tx for tx in txns if tx["action"] == "deposit"]
    borrows = [tx for tx in txns if tx["action"] == "borrow"]
    repays = [tx for tx in txns if tx["action"] == "repay"]
    withdrawals = [tx for tx in txns if tx["action"] == "withdraw"]

    deposit_sum = sum(tx["amountUSD"] for tx in deposits if tx["amountUSD"] is not None)
    borrow_sum = sum(tx["amountUSD"] for tx in borrows if tx["amountUSD"] is not None)
    repay_sum = sum(tx["amountUSD"] for tx in repays if tx["amountUSD"] is not None)
    withdrawal_sum = sum(tx["amountUSD"] for tx in withdrawals if tx["amountUSD"] is not None)

    activity_count = len(txns)
    unique_tokens = len(set(tx["assetSymbol"] for tx in txns if tx["assetSymbol"]))

    return {
        "wallet": wallet_address,
        "totalDepositedUSD": deposit_sum,
        "totalBorrowedUSD": borrow_sum,
        "totalRepaidUSD": repay_sum,
        "totalWithdrawnUSD": withdrawal_sum,
        "activityCount": activity_count,
        "uniqueTokens": unique_tokens
    }

def compute_credit_score(features):
    # Simple score: 1000 - borrowed + repaid + deposit weight - withdrawal penalty
    score = (
        0.5 * features["totalDepositedUSD"] -
        0.7 * features["totalBorrowedUSD"] +
        0.6 * features["totalRepaidUSD"] -
        0.3 * features["totalWithdrawnUSD"]
    )
    score += 2 * features["uniqueTokens"]
    score += 0.1 * features["activityCount"]
    return max(0, round(score, 2))  # Ensure non-negative
