#!/usr/bin/env python3
"""Shared-team HTTP API for the Beacon Archive quest.

Only task inputs are public.  A generated task catalogue and its exact
expected JSON live in this process; shared completion flags are persisted in
SQLite.  The implementation deliberately uses only the Python standard
library so it can be deployed without third-party dependencies.
"""
from __future__ import annotations

import json
import os
import sqlite3
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import unquote, urlsplit

from tasks import build_catalog


HOST = os.environ.get("TEAM_API_HOST", "127.0.0.1")
PORT = int(os.environ.get("TEAM_API_PORT", "8765"))
DB = Path(os.environ.get("TEAM_API_DB", Path(__file__).with_name("progress.sqlite3")))
MAX_BODY = 65_536


def canonical(value):
    """Canonical JSON makes names, nesting and value types part of equality."""
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False)


def connect_db(db_path):
    db_path.parent.mkdir(parents=True, exist_ok=True)
    return sqlite3.connect(db_path, timeout=10)


def init_db(db_path):
    with connect_db(db_path) as connection:
        connection.execute(
            "CREATE TABLE IF NOT EXISTS completed (task_id TEXT PRIMARY KEY, completed_at TEXT NOT NULL)"
        )


def completed_ids(server):
    with connect_db(server.db_path) as connection:
        rows = connection.execute("SELECT task_id FROM completed").fetchall()
    done = {row[0] for row in rows}
    return [task_id for task_id in server.catalog if task_id in done]


class QuestHandler(BaseHTTPRequestHandler):
    server_version, sys_version = "BeaconArchiveAPI/1.0", ""

    def log_message(self, fmt, *args):
        print("%s %s %s" % (self.log_date_time_string(), self.client_address[0], fmt % args), flush=True)

    def reply(self, status, value):
        payload = json.dumps(value, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(payload)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.end_headers()
        self.wfile.write(payload)

    def read_json(self):
        if self.headers.get_content_type() != "application/json":
            raise ValueError("Content-Type must be application/json")
        try:
            length = int(self.headers.get("Content-Length", "0"))
        except ValueError as error:
            raise ValueError("invalid Content-Length") from error
        if not 1 <= length <= MAX_BODY:
            raise ValueError("body must be 1..65536 bytes")
        try:
            return json.loads(self.rfile.read(length).decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as error:
            raise ValueError("body must be valid UTF-8 JSON") from error

    def do_GET(self):
        path = unquote(urlsplit(self.path).path)
        if path == "/health":
            return self.reply(200, {"status": "ok"})
        if path == "/api/tasks":
            return self.reply(200, {"tasks": [{"id": task_id} for task_id in self.server.catalog]})
        if path == "/api/progress":
            done = completed_ids(self.server)
            return self.reply(200, {"completed": done, "completed_count": len(done), "total_count": len(self.server.catalog)})
        prefix, suffix = "/api/tasks/", "/input"
        if path.startswith(prefix) and path.endswith(suffix):
            task_id = path[len(prefix):-len(suffix)].strip("/")
            task = self.server.catalog.get(task_id)
            if task is None:
                return self.reply(404, {"error": "unknown_task"})
            return self.reply(200, {
                "task_id": task_id,
                "input": task["input"],
                "completed": task_id in completed_ids(self.server),
            })
        return self.reply(404, {"error": "not_found"})

    def do_POST(self):
        if unquote(urlsplit(self.path).path) != "/api/submit":
            return self.reply(404, {"error": "not_found"})
        try:
            body = self.read_json()
        except ValueError as error:
            return self.reply(400, {"error": "invalid_request", "detail": str(error)})
        if not isinstance(body, dict) or set(body) != {"task_id", "answer"} or not isinstance(body["task_id"], str):
            return self.reply(400, {"error": "schema", "expected": {"task_id": "string", "answer": "JSON value"}})
        task = self.server.catalog.get(body["task_id"])
        if task is None:
            return self.reply(404, {"error": "unknown_task"})
        try:
            correct = canonical(body["answer"]) == canonical(task["expected"])
        except (TypeError, ValueError):
            return self.reply(400, {"error": "answer_not_json_value"})
        if not correct:
            return self.reply(200, {"correct": False})
        with connect_db(self.server.db_path) as connection:
            cursor = connection.execute(
                "INSERT OR IGNORE INTO completed(task_id, completed_at) VALUES (?, ?)",
                (body["task_id"], datetime.now(timezone.utc).isoformat()),
            )
        return self.reply(200, {
            "correct": True,
            "task_id": body["task_id"],
            "already_completed": cursor.rowcount == 0,
        })


def create_server(host=HOST, port=PORT, *, catalog=None, db_path=DB):
    """Build a server; exposed for tests and for embedding in a process manager."""
    init_db(Path(db_path))
    server = ThreadingHTTPServer((host, port), QuestHandler)
    server.catalog = build_catalog() if catalog is None else catalog
    server.db_path = Path(db_path)
    return server


def main():
    server = create_server()
    host, port = server.server_address[:2]
    print(f"Beacon Archive API listening on {host}:{port}", flush=True)
    server.serve_forever()


if __name__ == "__main__":
    main()
