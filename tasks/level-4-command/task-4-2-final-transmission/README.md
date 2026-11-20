# 4.2 · Финальная передача

Вырежи из `message` фрагмент от `start` длиной `length`, переведи его в верхний
регистр и собери f-строку `ФРАГМЕНТ:ДЛИНА_ИСХОДНОЙ_СТРОКИ`. Отправь:

```json
{"transmission":"ДИО:14"}
```

Подсказка: конец среза равен `start + length`, а длина строки — `len(message)`.

## Шаблон GET и POST

```python
# GET /api/tasks/4.2/input → i = task["input"]; fragment = i["message"][i["start"]:i["start"] + i["length"]].upper()
# answer = {"transmission": f"{fragment}:{len(i['message'])}"}
# POST /api/submit: {"task_id":"4.2", "answer":answer, "participant_token":"ТОКЕН"}
```
