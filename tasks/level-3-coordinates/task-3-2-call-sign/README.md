# 3.2 · Позывной сектора

Собери f-строку из `name` и `sector` в формате `ИМЯ-07`: имя нужно привести к
верхнему регистру, а номер сектора дополнить нулём до двух знаков (`:02d`).
Отправь:

```json
{"callsign":"NORTH-07"}
```

## Шаблон GET и POST

```python
# GET /api/tasks/3.2/input → i = task["input"]; answer = {"callsign": f"{i['name'].upper()}-{i['sector']:02d}"}
# POST /api/submit: {"task_id":"3.2", "answer":answer, "participant_token":"ТОКЕН"}
```
