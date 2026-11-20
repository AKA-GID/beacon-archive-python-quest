# 2.1 · Очистить позывной

У `phrase` есть лишние пробельные символы по краям и случайный регистр.
Примени `.strip().lower()` и отправь результат:

```json
{"clean":"север-7"}
```

## Шаблон GET и POST

```python
# GET /api/tasks/2.1/input → answer = {"clean": task["input"]["phrase"].strip().lower()}
# POST /api/submit: {"task_id":"2.1", "answer":answer, "participant_token":"ТОКЕН"}
```
