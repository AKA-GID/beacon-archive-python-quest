# 3.3 · Код канала

Возьми из `word` каждый `step`-й символ срезом `word[::step]`. `step` —
случайное число из входных данных. Отправь:

```json
{"code":"прдтчк"}
```

## Шаблон GET и POST

```python
# GET /api/tasks/3.3/input → i = task["input"]; answer = {"code": i["word"][::i["step"]]}
# POST /api/submit: {"task_id":"3.3", "answer":answer, "participant_token":"ТОКЕН"}
```
