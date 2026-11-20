# 4.1 · Диспетчерский пакет

Собери f-строку строго в формате:

```text
TO:{callsign} | sector={sector:02d} | channel={channel} | priority={priority.upper()}
```

Значения возьми из `input` и отправь строку в поле `packet`:

```json
{"packet":"TO:NORTH-07 | sector=03 | channel=18 | priority=HIGH"}
```
