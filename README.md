# Итоговый проект DataOps

 Репозиторий содержит итоговое домашнее задание по DataOps

## Структура проекта

- `mlflow/` - MLflow с PostgreSQL
- `airflow/` - Airflow с PostgreSQL и примером DAG
- `lakefs/` - LakeFS с PostgreSQL и MinIO
- `jupyterhub/` - JupyterHub в Docker
- `ml-service/` - FastAPI ML-сервис с логированием, записью в базу и метриками
- `monitoring/` - Prometheus и Grafana
- `k8s/ml-service/` - Kubernetes-манифесты
- `helm/ml-service/` - Helm chart

## Основные адреса

- MLflow: `http://localhost:5001`
- Airflow: `http://localhost:8081`
- LakeFS: `http://localhost:8001`
- MinIO: `http://localhost:9001`
- JupyterHub: `http://localhost:8002`
- ML-сервис: `http://localhost:8000`
- Prometheus: `http://localhost:9090`
- Grafana: `http://localhost:3000`

## Запуск

Запуск всех сервисов:

```bash
docker compose up -d --build
```

Проверка статуса:

```bash
docker compose ps
```

Просмотр логов сервиса:

```bash
docker compose logs -f ml-service
```

## Проверка ML-сервиса

Проверка health endpoint:

```bash
curl http://localhost:8000/health
```

Тестовый запрос на предсказание:

```bash
curl -X POST http://localhost:8000/api/v1/predict \
  -H 'Content-Type: application/json' \
  -d '{"features":[1,2,3]}'
```

Проверка метрик:

```bash
curl http://localhost:8000/metrics
```

## PromptStorage

Примеры команд для создания нескольких версий промптов в MLflow находятся в файле:

- `mlflow/prompt_storage_examples.md`
