# main.py

import zipfile
import json
import os
from collections import defaultdict
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from Scripts.logistic_model import train_logistic_model
from Scripts.svm_model import train_svm_model
from Scripts.nn_model import train_nn_model
from Scripts.compare_models import compare_models

from Scripts.utils import (
    convert_token_amount_to_usd,
    parse_transaction,
    create_wallet_features,
    compute_credit_score
)

# Step 1: Unzip the dataset
zip_path = "Raw Data/user-wallet-transactions.json.zip"
json_filename = "user-wallet-transactions.json"
extracted_path = os.path.join("Data", json_filename)

with zipfile.ZipFile(zip_path, "r") as zip_ref:
    zip_ref.extractall("Data")
print("✅ Unzipped JSON dataset.")

# Step 2: Load and parse raw transactions
with open(extracted_path, "r") as f:
    raw_transactions = json.load(f)

print(f"✅ Loaded {len(raw_transactions)} transactions")

# Step 3: Fill missing USD values and group by wallet
wallet_data = defaultdict(list)

for txn in raw_transactions:
    parsed_txn = parse_transaction(txn)
    
    if parsed_txn["amountUSD"] is None:
        parsed_txn["amountUSD"] = convert_token_amount_to_usd(
            parsed_txn["amount"],
            parsed_txn["assetSymbol"],
            parsed_txn["assetPriceUSD"]
        )

    wallet_data[parsed_txn["userWallet"]].append(parsed_txn)

print(f"✅ Grouped transactions into {len(wallet_data)} wallets.")

# Step 4: Generate wallet-level features
wallet_features = []
for wallet, txns in wallet_data.items():
    features = create_wallet_features(wallet, txns)
    wallet_features.append(features)

# Step 5: Compute raw credit score for each wallet
for features in wallet_features:
    features["creditScore"] = compute_credit_score(features)

# Step 6: Normalize credit scores into 300–850 range
df = pd.DataFrame(wallet_features)

# Handle NaN and Inf
df["creditScore"].replace([np.inf, -np.inf], np.nan, inplace=True)
df["creditScore"].fillna(0, inplace=True)

# Optional: Clip extreme outliers (e.g., to 99th percentile)
upper_bound = df["creditScore"].quantile(0.99)
df["creditScore"] = np.clip(df["creditScore"], 0, upper_bound)

# Rescale to [300, 850]
min_score = df["creditScore"].min()
max_score = df["creditScore"].max()

if max_score > min_score:
    df["creditScore"] = 300 + ((df["creditScore"] - min_score) / (max_score - min_score)) * (850 - 300)
else:
    df["creditScore"] = 300  # fallback if all scores are same or zero

# Step 7: Save final dataset
output_path = "Data/final_dataset.csv"
df.to_csv(output_path, index=False)

print(f"✅ Final dataset saved at {output_path}")
print("🔎 Sample preview:")
print(df.head())

# Load the final dataset
df = pd.read_csv("Data/final_dataset.csv")

# Drop rows with missing target
df = df.dropna(subset=["creditScore"])

# Convert to binary classification problem (e.g., good credit = 1 if score > 600)
df["label"] = (df["creditScore"] > 600).astype(int)

# Drop columns that shouldn't be in features
features = df.drop(columns=["wallet", "creditScore", "label"])
target = df["label"]

# Fill missing values with mean
features = features.fillna(features.mean(numeric_only=True))

# Feature scaling
scaler = StandardScaler()
X_scaled = scaler.fit_transform(features)

# Split the data
X_train, X_test, y_train, y_test = train_test_split(X_scaled, target, test_size=0.2, random_state=42)

# Train models
log_model, log_pred = train_logistic_model(X_train, y_train, X_test, y_test)
svm_model, svm_pred = train_svm_model(X_train, y_train, X_test, y_test)
nn_model, nn_pred = train_nn_model(X_train, y_train, X_test, y_test)

# Compare
compare_models(y_test, {
    "Logistic Regression": log_pred,
    "SVM (Poly Kernel)": svm_pred,
    "Neural Network": nn_pred
})
