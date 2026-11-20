# 4.2 · Финальная передача

Вырежи из `message` фрагмент от `start` длиной `length`, переведи его в верхний
регистр и собери f-строку `ФРАГМЕНТ:ДЛИНА_ИСХОДНОЙ_СТРОКИ`. Отправь:

```json
{"transmission":"ДИО:14"}
```

Подсказка: конец среза равен `start + length`, а длина строки — `len(message)`.

## JSON API

```json
{"task_id":"4.2","completed":false,"input":{"message":"орбитачистая","start":2,"length":4}}
```
```json
{"task_id":"4.2","answer":{"transmission":"БИТА:13"},"participant_token":"MAK-ВАШ_ТОКЕН"}
```
