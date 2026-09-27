import json
import numpy as np
import pandas as pd
from sklearn.datasets import load_iris
try:
    from evidently.report import Report
    from evidently.metric_preset import DataDriftPreset
except ModuleNotFoundError:
    from evidently.legacy.report import Report
    from evidently.legacy.metric_preset import DataDriftPreset

def check_data_drift():
    print("Запуск перевірки на Data Drift через Evidently AI...")
    
    # 1. Завантажуємо еталонний датасет (Reference)
    iris = load_iris(as_frame=True)
    reference_data = iris.frame
    
    # 2. Емулюємо поточний потік даних з невеликим дрейфом (Current)
    current_data = reference_data.copy()
    current_data["sepal length (cm)"] = current_data["sepal length (cm)"] + np.random.normal(0.5, 0.2, size=len(current_data))
    
    # 3. Генеруємо звіт Evidently
    report = Report(metrics=[DataDriftPreset()])
    report.run(reference_data=reference_data, current_data=current_data)
    
    report_dict = report.as_dict()
    metrics = report_dict["metrics"][0]["result"]
    
    dataset_drift = metrics["dataset_drift"]
    number_of_drifted_columns = metrics["number_of_drifted_columns"]
    
    print(f"Результат перевірки: Dataset Drift = {dataset_drift}, Дрейфуючих колонок = {number_of_drifted_columns}")
    
    # Зберігаємо звіт у JSON та HTML для перегляду
    with open("final-project/monitoring/drift_report.json", "w") as f:
        json.dump(report_dict, f, indent=2)
    report.save_html("final-project/monitoring/drift_report.html")
    
    return {"dataset_drift": dataset_drift, "drifted_columns": number_of_drifted_columns}

if __name__ == "__main__":
    result = check_data_drift()
    print(json.dumps(result, indent=2))
