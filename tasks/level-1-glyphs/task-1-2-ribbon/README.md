# 1.2 · Лента координат

Вырежи из `message` срез от `start` включительно до `end` не включительно.
Отправь:

```json
{"fragment":"вер"}
```

Пример `input`: `{"message":"северныймаяк","start":2,"end":5}`. Обе
границы сервер генерирует как числа.

## Шаблон GET и POST

```python
# После GET /api/tasks/1.2/input: answer = {"fragment": task["input"]["message"][task["input"]["start"]:task["input"]["end"]]}
# Отправьте POST /api/submit с {"task_id":"1.2", "answer":answer, "participant_token":"ТОКЕН"}.
```
