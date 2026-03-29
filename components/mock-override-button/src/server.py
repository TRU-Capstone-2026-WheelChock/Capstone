import json
from http.server import BaseHTTPRequestHandler, HTTPServer

from state import OverrideState


class MockOverrideButtonServer(HTTPServer):
    def __init__(self, *args, state: OverrideState, **kwargs):
        super().__init__(*args, **kwargs)
        self.state = state


class OverrideControlHandler(BaseHTTPRequestHandler):

    def log_message(self, format, *args):
        print(f"[{self.address_string()}] {format % args}")

    def _send_json(self, status: int, data: dict) -> None:
        body = json.dumps(data).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _read_body(self) -> dict | None:
        length = int(self.headers.get("Content-Length", 0))
        if length == 0:
            return None
        try:
            return json.loads(self.rfile.read(length))
        except json.JSONDecodeError:
            return None

    def do_GET(self):
        if self.path == "/state":
            self._send_json(200, self.server.state.get_state())
        else:
            self._send_json(404, {"error": "not found"})

    def do_POST(self):
        if self.path == "/override":
            body = self._read_body()
            if body is None or "value" not in body or not isinstance(body["value"], bool):
                self._send_json(400, {"error": "'value' (bool) is required"})
                return

            self.server.state.set_override_enabled(body["value"])
            self._send_json(200, self.server.state.get_state())
        else:
            self._send_json(404, {"error": "not found"})
