from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report

def train_logistic_model(X_train, y_train, X_test, y_test):
    model = LogisticRegression(max_iter=1000)
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    print("Logistic Regression Performance:")
    print(classification_report(y_test, y_pred))
    return model, y_pred
