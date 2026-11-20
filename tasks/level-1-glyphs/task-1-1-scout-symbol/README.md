# 1.1 · Символ разведчика

Из строки `word` возьми символ с индексом `index`. Индексация начинается с
нуля. Отправь:

```json
{"symbol":"а"}
```

Пример `input`: `{"word":"маяк","index":1}`. Число `index` сервер каждый
раз выбирает случайно.

## Шаблон GET и POST

```python
import json
from urllib.request import Request, urlopen
BASE_URL, TASK_ID, PARTICIPANT_TOKEN = "http://192.144.13.123:8766", "1.1", "ТОКЕН_ОТ_ПРЕПОДАВАТЕЛЯ"
with urlopen(f"{BASE_URL}/api/tasks/{TASK_ID}/input") as r: task = json.load(r)
answer = {"symbol": task["input"]["word"][task["input"]["index"]]}
request = Request(f"{BASE_URL}/api/submit", data=json.dumps({"task_id": TASK_ID, "answer": answer, "participant_token": PARTICIPANT_TOKEN}).encode(), headers={"Content-Type": "application/json"}, method="POST")
with urlopen(request) as r: print(json.load(r))
```
