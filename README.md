# 🚀 ArgoCD & GitOps Deployment (goit-argo)

Цей репозиторій містить конфігурацію для розгортання інфраструктури та застосунків за допомогою **ArgoCD** та **Helm** у кластері Kubernetes (EKS).

---

## 🛠 1. Запуск інфраструктури (Terraform)
Для підготовки середовища та встановлення ArgoCD, перейдіть у відповідну директорію та виконайте команди:

```bash
cd leson7/argocd

# Ініціалізація та завантаження провайдерів
terraform init

# Створення ресурсів у AWS
terraform apply -auto-approve

🔍 2. Перевірка статусу ArgoCD
Переконайтеся, що всі компоненти ArgoCD успішно запустилися в окремому namespace:

Bash:
kubectl get pods -n infra-tools

Усі поди повинні мати статус Running.

🌐 3. Доступ до інтерфейсу (ArgoCD UI)
Оскільки ArgoCD працює всередині кластера, використовуйте port-forward для доступу через браузер:

Створіть тунель:

Bash:
kubectl port-forward svc/argocd-server -n infra-tools 8080:443

Відкрийте браузер: https://localhost:8080

Логін: admin

Отримання пароля:

Bash:
kubectl -n infra-tools get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 --decode

📦 4. Перевірка деплою застосунку (MLflow)
Ми використовуємо Multiple Sources в ArgoCD: офіційний Helm-чарт та кастомні values.yaml з цього репозиторію.

Як перевірити в терміналі:
Bash
# Перевірка статусу Application в ArgoCD
kubectl get application mlflow -n infra-tools

# Перевірка запущених подів застосунку
kubectl get pods -n application

Як перевірити в UI:
Знайдіть плитку mlflow. Вона повинна бути Synced (зелена галочка) та Healthy (зелене серце).

Видалення ресурсів:

cd leson7/argocd

# Запуск процесу видалення
terraform destroy -auto-approve

## 🔗 5. Корисні посилання
* **GitOps Репозиторій з application.yaml:** [https://github.com/OF3000/goit-argo](https://github.com/OF3000/goit-argo)