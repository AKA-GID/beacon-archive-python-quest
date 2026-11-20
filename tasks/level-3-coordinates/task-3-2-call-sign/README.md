# 3.2 · Позывной сектора

Собери f-строку из `name` и `sector` в формате `ИМЯ-07`: имя нужно привести к
верхнему регистру, а номер сектора дополнить нулём до двух знаков (`:02d`).
Отправь:

```json
{"callsign":"NORTH-07"}
```

## JSON API

```json
{"task_id":"3.2","completed":false,"input":{"name":"luna","sector":8}}
```
```json
{"task_id":"3.2","answer":{"callsign":"LUNA-08"},"participant_token":"MAK-ВАШ_ТОКЕН"}
```
