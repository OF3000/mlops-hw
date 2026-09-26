import sys
import json
import numpy as np
from sklearn.datasets import load_iris

def run_validation():
    print("Старт кроку: Валідація даних...")
    iris = load_iris()
    X, y = iris.data, iris.target
    
    # Перевірка форми даних та відсутності null
    if X.shape[0] == 0 or X.shape[1] != 4:
        raise ValueError(f"Некоректна розмірність ознак: {X.shape}")
    
    if np.isnan(X).any() or np.isnan(y).any():
        raise ValueError("Виявлено пропуски (NaN) у даних.")
        
    print(f"Дані валідні. Записів: {X.shape[0]}, ознак: {X.shape[1]}")
    return {"status": "VALID", "samples_count": X.shape[0]}

if __name__ == "__main__":
    result = run_validation()
    print(json.dumps(result))
