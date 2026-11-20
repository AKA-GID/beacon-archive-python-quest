# 2.2 · Табличка маяка

Из `callsign` сделай табличку: сначала `.title()`, затем замени пробелы на
дефисы с `.replace(" ", "-")`. Отправь:

```json
{"label":"Тихий-Маяк"}
```

## Шаблон GET и POST

```python
# GET /api/tasks/2.2/input → answer = {"label": task["input"]["callsign"].title().replace(" ", "-")}
# POST /api/submit: {"task_id":"2.2", "answer":answer, "participant_token":"ТОКЕН"}
```
