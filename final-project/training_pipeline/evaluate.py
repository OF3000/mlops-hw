import json
import joblib
from sklearn.metrics import accuracy_score, f1_score

ACCURACY_THRESHOLD = 0.85

def run_evaluation():
    print("Старт кроку: Оцінка якості моделі...")
    model = joblib.load("models/model.joblib")
    X_test, y_test = joblib.load("models/test_data.joblib")
    
    preds = model.predict(X_test)
    acc = accuracy_score(y_test, preds)
    f1 = f1_score(y_test, preds, average="weighted")
    
    print(f"Accuracy: {acc:.4f}, F1-score: {f1:.4f}")
    
    if acc < ACCURACY_THRESHOLD:
        raise ValueError(f"Якість моделі нижче порогу: {acc:.4f} < {ACCURACY_THRESHOLD}")
        
    return {
        "status": "EVALUATED",
        "metrics": {"accuracy": acc, "f1_score": f1},
        "passed_threshold": True
    }

if __name__ == "__main__":
    result = run_evaluation()
    print(json.dumps(result))
