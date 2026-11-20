# 1.3 · Зеркало маяка

Маяк прислал слово задом наперёд. Разверни `word` срезом `[::-1]` и отправь:

```json
{"reflection":"кяам"}
```

## Шаблон GET и POST

```python
# GET /api/tasks/1.3/input → answer = {"reflection": task["input"]["word"][::-1]}
# POST /api/submit: {"task_id":"1.3", "answer":answer, "participant_token":"ТОКЕН"}
```
