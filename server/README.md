# Сервер «Архива Маяка»

`app.py` сохраняет прежний публичный контракт: `GET /api/tasks`,
`GET /api/tasks/{task_id}/input`, `POST /api/submit` и `GET /api/progress`.
При каждом запуске он создаёт один набор случайных входных данных для всей
команды. Ожидаемые JSON-ответы не выдаются API и не записываются в репозиторий.

## Запуск

Нужен Python 3.10+ и больше никаких пакетов:

```sh
cd server
TEAM_API_HOST=0.0.0.0 TEAM_API_PORT=8765 python3 app.py
```

По умолчанию база общего прогресса — `server/progress.sqlite3`. Её путь можно
сменить переменной `TEAM_API_DB`. Чтобы начать новый раунд, остановите сервис и
переместите этот конкретный файл базы в резервную копию, затем запустите сервис
снова. Не добавляйте базу в Git.

Проверка после запуска:

```sh
curl http://127.0.0.1:8765/health
curl http://127.0.0.1:8765/api/tasks
```

## Отдельная служба рядом со старым квестом

Шаблон [deploy/beacon-archive-api.service](../deploy/beacon-archive-api.service)
настроен на порт `8766` и локальный адрес `127.0.0.1`, поэтому не меняет
существующий сервис на `8765`. На сервере установите его как пользовательскую
службу, затем обращайтесь к ней через reverse-proxy или SSH-туннель:

```sh
mkdir -p ~/.config/systemd/user
cp deploy/beacon-archive-api.service ~/.config/systemd/user/
systemctl --user daemon-reload
systemctl --user enable --now beacon-archive-api.service
curl http://127.0.0.1:8766/health
```

Не открывайте `8766` в интернет без явного решения по HTTPS и сетевым правилам.

Если сервис доступен в интернете, ограничьте доступ сетевым экраном или
reverse-proxy, используйте HTTPS и не принимайте личные данные: API рассчитан
только на учебные строки и JSON.
