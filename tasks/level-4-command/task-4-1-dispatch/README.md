# 4.1 · Диспетчерский пакет

Собери f-строку строго в формате:

```text
TO:{callsign} | sector={sector:02d} | channel={channel} | priority={priority.upper()}
```

Значения возьми из `input` и отправь строку в поле `packet`:

```json
{"packet":"TO:NORTH-07 | sector=03 | channel=18 | priority=HIGH"}
```

## Шаблон GET и POST

```python
# GET /api/tasks/4.1/input → i = task["input"]
# answer = {"packet": f"TO:{i['callsign']} | sector={i['sector']:02d} | channel={i['channel']} | priority={i['priority'].upper()}"}
# POST /api/submit: {"task_id":"4.1", "answer":answer, "participant_token":"ТОКЕН"}
```
