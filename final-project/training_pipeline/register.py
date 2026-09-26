import json

def lambda_handler(event, context):
    print("Received payload from previous step:", json.dumps(event))
    
    commit_sha = event.get("commit_sha", "unknown")
    validation_status = event.get("validation_status", "UNKNOWN")
    
    # Фіксація результатів та імітація передачі в MLflow / Registry
    metrics = {
        "accuracy": 0.96,
        "loss": 0.08
    }
    
    print(f"Logged metrics for commit {commit_sha}: {metrics}")
    
    return {
        "statusCode": 200,
        "execution_status": "SUCCESS",
        "validation_status": validation_status,
        "commit_sha": commit_sha,
        "metrics": metrics
    }