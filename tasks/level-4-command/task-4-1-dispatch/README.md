# 4.1 · Диспетчерский пакет

Собери f-строку строго в формате:

```text
TO:{callsign} | sector={sector:02d} | channel={channel} | priority={priority.upper()}
```

Значения возьми из `input` и отправь строку в поле `packet`:

```json
{"packet":"TO:NORTH-07 | sector=03 | channel=18 | priority=HIGH"}
```

## JSON API

```json
{"task_id":"4.1","completed":false,"input":{"callsign":"LUNA-12","sector":4,"channel":55,"priority":"normal"}}
```
```json
{"task_id":"4.1","answer":{"packet":"TO:LUNA-12 | sector=04 | channel=55 | priority=NORMAL"},"participant_token":"MAK-ВАШ_ТОКЕН"}
```
