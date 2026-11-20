# 2.3 · Сколько эхо

Посчитай, сколько раз однобуквенный `symbol` встречается в `signal`, не
различая регистр. Можно привести строку к нижнему регистру и вызвать `.count()`.
Отправь число:

```json
{"count":3}
```

## Шаблон GET и POST

```python
# GET /api/tasks/2.3/input → answer = {"count": task["input"]["signal"].lower().count(task["input"]["symbol"])}
# POST /api/submit: {"task_id":"2.3", "answer":answer, "participant_token":"ТОКЕН"}
```
