def fill_usd_amounts(transactions: list, token_prices: dict) -> list:
    """
    Adds 'amountUSD' to each transaction using static token prices.

    Args:
        transactions (list): List of transaction dictionaries.
        token_prices (dict): Dictionary of token prices. Example: {"DAI": 1.0, "WBTC": 30000.0}

    Returns:
        list: Transactions with 'amountUSD' field added where possible.
    """
    for tx in transactions:
        token = tx.get("tokenSymbol")
        amount = tx.get("amount")

        try:
            if token and amount is not None and token in token_prices:
                tx["amountUSD"] = float(amount) * token_prices[token]
            else:
                tx["amountUSD"] = None
        except Exception as e:
            print(f"❌ Error processing tx: {tx.get('hash', '')[:8]}... → {e}")
            tx["amountUSD"] = None

    print(f"✅ Filled USD amounts in {len(transactions)} transactions.")
    return transactions
