# visualize.py

import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Create Plots directory if not present
os.makedirs("Plots", exist_ok=True)

# Load dataset
df = pd.read_csv("Data/final_dataset.csv")

# Set plot style
sns.set(style="whitegrid")

# Clean or clip credit score if needed
df["creditScore"] = df["creditScore"].clip(lower=300, upper=850)

# Plot 1: Credit Score Distribution
plt.figure(figsize=(10, 5))
sns.histplot(df["creditScore"].dropna(), bins=50, kde=True, color="steelblue")
plt.title("Distribution of Credit Scores")
plt.xlabel("Credit Score")
plt.ylabel("Number of Wallets")
plt.tight_layout()
plt.savefig("Plots/credit_score_distribution.png")
plt.show()

# Plot 2: Deposits vs Credit Score
plt.figure(figsize=(10, 6))
sns.scatterplot(
    x="totalDepositedUSD", y="creditScore", data=df,
    alpha=0.6, edgecolor=None
)
plt.xscale("log")  # Log scale for better visibility
plt.title("Total Deposits vs Credit Score")
plt.xlabel("Total Deposits (USD, log scale)")
plt.ylabel("Credit Score")
plt.tight_layout()
plt.savefig("Plots/deposits_vs_score.png")
plt.show()
