# 1.2 · Лента координат

Вырежи из `message` срез от `start` включительно до `end` не включительно.
Отправь:

```json
{"fragment":"вер"}
```

Пример `input`: `{"message":"северныймаяк","start":2,"end":5}`. Обе
границы сервер генерирует как числа.

## JSON API

```json
{"task_id":"1.2","completed":false,"input":{"message":"лунныймаяк","start":1,"end":5}}
```

```json
{"task_id":"1.2","answer":{"fragment":"унны"},"participant_token":"MAK-ВАШ_ТОКЕН"}
```
