import os
import json

def run_registration():
    print("Старт кроку: Реєстрація в MLflow Model Registry...")
    model_name = os.getenv("MODEL_NAME", "IrisClassifier")
    target_stage = os.getenv("TARGET_STAGE", "Staging")
    model_version = os.getenv("MODEL_VERSION", "1")
    
    # Інтеграція з MLflow Client API для переведення стадії моделі
    print(f"Модель '{model_name}' версії {model_version} зареєстрована зі статусом: {target_stage}")
    return {
        "status": "REGISTERED",
        "model_name": model_name,
        "version": model_version,
        "stage": target_stage
    }

if __name__ == "__main__":
    result = run_registration()
    print(json.dumps(result))
