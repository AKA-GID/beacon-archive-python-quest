# 3.1 · Окно сигнала

Найди индекс первого появления `marker` в `message` методом `.find()`. Маркер
точно существует. Отправь:

```json
{"position":6}
```

## Шаблон GET и POST

```python
# GET /api/tasks/3.1/input → answer = {"position": task["input"]["message"].find(task["input"]["marker"])}
# POST /api/submit: {"task_id":"3.1", "answer":answer, "participant_token":"ТОКЕН"}
```
