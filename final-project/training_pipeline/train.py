import os
import json
import joblib
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

def run_train():
    print("Старт кроку: Навчання моделі...")
    iris = load_iris()
    X_train, X_test, y_train, y_test = train_test_split(
        iris.data, iris.target, test_size=0.2, random_state=42
    )
    
    model = RandomForestClassifier(n_estimators=50, max_depth=3, random_state=42)
    model.fit(X_train, y_train)
    
    os.makedirs("models", exist_ok=True)
    model_path = "models/model.joblib"
    joblib.dump(model, model_path)
    
    # Зберігаємо тестові дані для кроку оцінки (eval)
    joblib.dump((X_test, y_test), "models/test_data.joblib")
    
    print(f"Модель успішно натренована та збережена: {model_path}")
    return {"status": "TRAINED", "model_path": model_path}

if __name__ == "__main__":
    result = run_train()
    print(json.dumps(result))
