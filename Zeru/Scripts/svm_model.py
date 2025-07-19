from sklearn.svm import SVC
from sklearn.metrics import classification_report

def train_svm_model(X_train, y_train, X_test, y_test):
    model = SVC(kernel='poly', degree=3)
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    print("SVM with Polynomial Kernel Performance:")
    print(classification_report(y_test, y_pred))
    return model, y_pred
