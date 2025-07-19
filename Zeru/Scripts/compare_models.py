from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

def compare_models(y_test, preds_dict):
    print("Model Comparison:\n")
    for model_name, y_pred in preds_dict.items():
        print(f"--- {model_name} ---")
        print(f"Accuracy : {accuracy_score(y_test, y_pred):.4f}")
        print(f"Precision: {precision_score(y_test, y_pred):.4f}")
        print(f"Recall   : {recall_score(y_test, y_pred):.4f}")
        print(f"F1 Score : {f1_score(y_test, y_pred):.4f}")
        print()
