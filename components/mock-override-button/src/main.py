import os

from publisher import start_publisher
from server import MockOverrideButtonServer, OverrideControlHandler
from state import OverrideState

PORT = int(os.environ.get("PORT", 8080))


def main():
    state = OverrideState()

    start_publisher(state)

    server = MockOverrideButtonServer(("0.0.0.0", PORT), OverrideControlHandler, state=state)
    print(f"MockOverrideButton listening on port {PORT}")
    print("Endpoints:")
    print("  GET  /state")
    print("  POST /override  {\"value\": true|false}")
    server.serve_forever()


if __name__ == "__main__":
    main()
