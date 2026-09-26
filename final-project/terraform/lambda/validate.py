import json

def lambda_handler(event, context):
    print("Received event:", json.dumps(event))
    
    # Отримання параметрів запуску з події
    dataset_source = event.get("dataset_source", "s3://mlops-datasets/iris.csv")
    commit_sha = event.get("commit_sha", "unknown")
    
    print(f"Validating dataset from: {dataset_source}")
    print(f"Triggered by commit: {commit_sha}")
    
    # Імітація валідації даних
    validation_status = "PASSED"
    
    return {
        "statusCode": 200,
        "validation_status": validation_status,
        "dataset_source": dataset_source,
        "commit_sha": commit_sha,
        "features_count": 4,
        "records_count": 150
    }