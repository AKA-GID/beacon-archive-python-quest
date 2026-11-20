import json
import sys
import tempfile
import threading
import unittest
from pathlib import Path
from urllib.error import HTTPError
from urllib.request import Request, urlopen

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "server"))
from app import create_server  # noqa: E402
from tasks import build_catalog  # noqa: E402


class QuestApiTests(unittest.TestCase):
    def test_generated_catalog_matches_documented_task_ids(self):
        catalog = build_catalog()
        self.assertEqual(
            list(catalog),
            ["1.1", "1.2", "1.3", "2.1", "2.2", "2.3", "3.1", "3.2", "3.3", "4.1", "4.2"],
        )
        for task in catalog.values():
            self.assertIsInstance(task["input"], dict)
            self.assertIsInstance(task["expected"], dict)

    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.catalog = {"1.1": {"input": {"word": "маяк", "index": 1}, "expected": {"symbol": "а"}}}
        self.server = create_server("127.0.0.1", 0, catalog=self.catalog, db_path=Path(self.temporary.name) / "progress.sqlite3")
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()
        self.base_url = f"http://127.0.0.1:{self.server.server_address[1]}"

    def tearDown(self):
        self.server.shutdown()
        self.thread.join()
        self.server.server_close()
        self.temporary.cleanup()

    def request_json(self, path, body=None):
        request = Request(f"{self.base_url}{path}")
        if body is not None:
            request = Request(
                f"{self.base_url}{path}",
                data=json.dumps(body).encode("utf-8"),
                headers={"Content-Type": "application/json"},
                method="POST",
            )
        with urlopen(request) as response:
            return response.status, json.load(response)

    def test_input_is_public_but_expected_answer_is_not(self):
        status, payload = self.request_json("/api/tasks/1.1/input")
        self.assertEqual(status, 200)
        self.assertEqual(payload, {"task_id": "1.1", "input": {"word": "маяк", "index": 1}, "completed": False})

    def test_exact_answer_marks_shared_progress(self):
        _, wrong = self.request_json("/api/submit", {"task_id": "1.1", "answer": {"symbol": 1}})
        self.assertEqual(wrong, {"correct": False})
        _, accepted = self.request_json("/api/submit", {"task_id": "1.1", "answer": {"symbol": "а"}})
        self.assertEqual(accepted, {"correct": True, "task_id": "1.1", "already_completed": False})
        _, progress = self.request_json("/api/progress")
        self.assertEqual(progress, {"completed": ["1.1"], "completed_count": 1, "total_count": 1})
        _, input_after = self.request_json("/api/tasks/1.1/input")
        self.assertTrue(input_after["completed"])

    def test_unknown_task_returns_404(self):
        with self.assertRaises(HTTPError) as error:
            self.request_json("/api/tasks/nope/input")
        self.assertEqual(error.exception.code, 404)
        error.exception.close()
