# 🦄 DeFi Wallet Credit Scoring with Machine Learning 💳


This project builds a **credit scoring system** for DeFi wallets using transaction-level data from the **Aave V2 protocol**. We extract key wallet-level features, handle missing values, engineer insights, and train multiple classification models — all to predict a wallet's creditworthiness.

---

## 🔍 What This Project Does

✅ Loads raw DeFi transaction data (JSON)

✅ Fills missing USD values using token price mapping

✅ Aggregates data into wallet-level summaries

✅ Builds features like total deposits, loan ratios, and token diversity

✅ Trains and compares 3 machine learning models:

* 🎯 Logistic Regression
* 🎩 SVM with Polynomial Kernel
* 🧠 Neural Network

✅ Scores wallets into custom credit score bands
✅ Compares model performance with precision, recall, F1
✅ Generates a cleaned CSV file ready for further analysis or integration!

---

## 📁 Project Structure

```bash
Zeru/
├── Data/
│ └── final_dataset.csv # Processed features + credit score
│
├── Scripts/
│ ├── parse_transactions.py # Extracts relevant fields from raw Aave V2 data
│ ├── load_raw_data.py # Loads JSON or raw dump into structured format
│ ├── fill_amount_usd.py # Fills missing USD values using static token prices
│ ├── aggregate_credit_data.py # Aggregates transactional data into wallet-level metrics
│ ├── compute_credit_scores.py # Calculates credit score from wallet features
│ ├── create_labels.py # Creates creditworthiness labels (e.g., binary classification)
│ ├── feature_engineering.py # Derived features, scaling, missing value imputation
│ ├── generate_features.py # Pipeline wrapper for all feature-related steps
│ ├── visualize.py # 📊 Distribution plots & trends (used in main.py too)
│ ├── utils.py # Shared functions (e.g., data loaders, scorers)
│ ├── logistic_model.py # Logistic Regression classifier
│ ├── svm_model.py # SVM with polynomial kernel
│ ├── nn_model.py # Neural Network classifier using sklearn MLP
│ ├── compare_models.py # Accuracy, F1, ROC-AUC comparison across models
│ └── __init__.py # Initializations
│
├── main.py # Orchestrates the full pipeline: ETL → Models → Viz
├── requirements.txt # Dependencies to install via pip
└── README.md # You’re reading it!
```

---

## 📊 Models & Results

| Model                   | Accuracy   | Precision | Recall    | F1 Score  |
| ----------------------- | ---------- | --------- | --------- | --------- |
| Logistic Regression     | 98.71%     | 0.00      | 0.00      | 0.00      |
| SVM (Polynomial Kernel) | 98.86%     | 0.00      | 0.00      | 0.00      |
| Neural Network          | **99.86%** | **1.00**  | **0.875** | **0.933** |

> 💡 Class imbalance is significant. The Neural Network handles minority class **far better**.

---

## 🧠 Credit Score Logic

Credit scores are calculated with a weighted formula (think secret DeFi sauce 🥫):

```python
score = base_score + (
    weight_deposit * totalDepositedUSD +
    weight_borrow * totalBorrowedUSD +
    weight_ratio * borrowToDepositRatio +
    weight_collateral * totalCollateralUSD +
    weight_txn * numTxns +
    weight_unique * uniqueTokens
)
```

Then the score is scaled into:

| Band      | Score Range |
| --------- | ----------- |
| Poor      | 0–300       |
| Fair      | 301–500     |
| Good      | 501–700     |
| Excellent | 701+        |

---

## 💻 How to Run

```bash
# Step 1: Install dependencies
pip install -r requirements.txt

# Step 2: Run the pipeline
python main.py
```

---

## 🔮 Future Enhancements

* ✅ Handle token price APIs (e.g., CoinGecko)
* ⏳ Time-decayed transaction weightage
* 📉 Credit score decay over inactivity
* 🧠 Hyperparameter tuning & advanced model selection (XGBoost, CatBoost)
* 🌐 Web dashboard for score visualization

---

## 👩‍💻✨ Made With Love By

* Vrushali Kadam 💙
* Python, pandas, sklearn, numpy, matplotlib
* Fueled by curiosity + a bit of caffeine ☕️
