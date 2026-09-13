# MLOps Training Automation: GitLab CI & AWS Step Functions

Реалізація автоматизованого тренувального пайплайну на базі AWS Step Functions та GitLab CI з розгортанням інфраструктури через Terraform.

---

## 🏗 Архітектура

* **GitLab CI** — тригер запуску, який передає Git-контекст (`commit_sha`, `branch`, користувача) у Step Functions.
* **AWS Step Functions** — оркестратор послідовного виконання завдань.
* **AWS Lambda (Validate)** — перевірка наявності та коректності вхідних даних датасету.
* **AWS Lambda (Log Metrics)** — фіксація фінальних метрик та реєстрація результатів.
* **Terraform** — декларативний опис та розгортання всіх AWS-ресурсів (IAM, Lambda, Step Functions).

---

## 📦 Створення архівів для Lambda

Перед застосуванням Terraform необхідно запакувати код функцій:

```bash
cd terraform/lambda
zip validate.zip validate.py
zip log_metrics.zip log_metrics.py
cd ../..

## ▶️ Запуск та перевірка Step Function

### Спосіб 1. Через AWS CLI (Ручний запуск із передачею JSON)

Для запуску пайплайну вручну передайте ARN створеної State Machine та вхідні параметри у форматі JSON:

```bash
aws stepfunctions start-execution \
  --state-machine-arn "<STATE_MACHINE_ARN>" \
  --name "manual-test-run-$(date +%s)" \
  --input '{
    "commit_sha": "manual-test-12345",
    "branch": "lesson10",
    "dataset_source": "s3://mlops-datasets/iris.csv",
    "triggered_by": "developer"
  }'

## Щоб перевірити статус виконання кроків (ValidateData ➔ LogMetrics):
  aws stepfunctions describe-execution \
  --execution-arn "<EXECUTION_ARN_З_ПОПЕРЕДНЬОЇ_КОМАНДИ>"