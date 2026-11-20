# 1.1 · Символ разведчика

Из строки `word` возьми символ с индексом `index`. Индексация начинается с
нуля. Отправь:

```json
{"symbol":"а"}
```

Пример `input`: `{"word":"маяк","index":1}`. Число `index` сервер каждый
раз выбирает случайно.

## JSON API

`GET /api/tasks/1.1/input` возвращает:

```json
{"task_id":"1.1","completed":false,"input":{"word":"радар","index":3}}
```

Тело `POST /api/submit`:

```json
{"task_id":"1.1","answer":{"symbol":"а"},"participant_token":"MAK-ВАШ_ТОКЕН"}
```
