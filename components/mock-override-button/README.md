# Mock Override Button

`mock-override-button` is a small development helper that exposes an HTTP API
for toggling `capstone-center` override mode and publishes the corresponding
override message to the center ZMQ input.

## Running

### Locally

```bash
poetry install --no-root
poetry run python src/main.py
```

### With Docker

```bash
docker compose -f docker-compose.dev.yml up --build
```

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `PORT` | `8080` | HTTP control API port |
| `CENTER_ENDPOINT` | `tcp://127.0.0.1:5555` | ZMQ endpoint to publish to |
| `DEVICE_ID` | `override-button-001` | `sender_id` in published messages |
| `DEVICE_NAME` | `mock-override-button` | `sender_name` in published messages |
| `PUBLISH_INTERVAL_SEC` | `1.0` | Publish interval in seconds |

## HTTP API

### `GET /state`

Returns the current override state.

```bash
curl http://localhost:8080/state
```

```json
{"override": false, "status": "active"}
```

### `POST /override`

Enable override:

```bash
curl -X POST http://localhost:8080/override \
  -H "Content-Type: application/json" \
  -d '{"value": true}'
```

Disable override:

```bash
curl -X POST http://localhost:8080/override \
  -H "Content-Type: application/json" \
  -d '{"value": false}'
```

## Published Message Format

Messages follow the `SensorMessage` schema used by `capstone-center` for
override input:

```json
{
  "sender_id": "override-button-001",
  "sender_name": "mock-override-button",
  "data_type": "override_button",
  "payload": {
    "status": "override",
    "status_code": 200
  }
}
```
