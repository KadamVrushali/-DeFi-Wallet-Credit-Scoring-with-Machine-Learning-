from sklearn.neural_network import MLPClassifier
from sklearn.metrics import classification_report

def train_nn_model(X_train, y_train, X_test, y_test):
    model = MLPClassifier(hidden_layer_sizes=(64, 32), max_iter=300, random_state=42)
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    print("Neural Network Performance:")
    print(classification_report(y_test, y_pred))
    return model, y_pred
