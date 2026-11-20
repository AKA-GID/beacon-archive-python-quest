# Шаблон работы с сервером

В каждом условии указан формат поля `answer`. Подставьте ID текущей задачи и
соберите ответ по фактическому `input`.

```python
import json
from urllib.request import Request, urlopen

BASE_URL = "http://192.144.13.123:8766"
TASK_ID = "1.1"
PARTICIPANT_TOKEN = "ТОКЕН_ОТ_ПРЕПОДАВАТЕЛЯ"

with urlopen(f"{BASE_URL}/api/tasks/{TASK_ID}/input") as response:
    task = json.load(response)

print(task["input"])

# Формат зависит от условия. Например, для 1.1:
answer = {"symbol": task["input"]["word"][task["input"]["index"]]}

payload = json.dumps({
    "task_id": TASK_ID,
    "answer": answer,
    "participant_token": PARTICIPANT_TOKEN,
}).encode("utf-8")
request = Request(
    f"{BASE_URL}/api/submit",
    data=payload,
    headers={"Content-Type": "application/json"},
    method="POST",
)
with urlopen(request) as response:
    print(json.load(response))
```

Прогресс всей команды: `GET /api/progress`.

Не публикуйте свой токен в коде, скриншотах или общем чате: он нужен серверу,
чтобы посчитать личное прохождение задач.
