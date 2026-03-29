# Development Docker Stack

This directory contains the Docker Compose setup for the PC-friendly development
stack.

The default stack is designed for local testing without Raspberry Pi hardware.
It starts:

- `center`
- `motor` using `MockMotorController`
- `display`
- `mock-override-button`
- `mock-sensor-1`
- `mock-sensor-2`
- `mock-sensor-3`

`mock-sensor-3` acts as the thermal-sensor stand-in for normal PC development.

The real thermal publisher is available as an optional profile because it
requires hardware access.

## Files

- `docker-compose.yml`
  - main development stack
- `dev_config/center.env`
  - selects the center runtime config
- `dev_config/motor.env`
  - selects the motor runtime config
- `dev_config/display.env`
  - selects the display runtime config
- `dev_config/thermal.env`
  - selects the thermal runtime config
- `dev_config/ports.env`
  - host-side port defaults used by the root stack

## Quick Start

Start the default stack:

```bash
docker compose -f Docker/development/docker-compose.yml up -d
```

Rebuild images first if needed:

```bash
docker compose -f Docker/development/docker-compose.yml up -d --build
```

Stop the stack:

```bash
docker compose -f Docker/development/docker-compose.yml down
```

## Center-First Startup

If you want to start `capstone-center` first and bring up the rest later:

```bash
docker compose -f Docker/development/docker-compose.yml up -d center
docker compose -f Docker/development/docker-compose.yml up -d \
  motor display mock-override-button mock-sensor-1 mock-sensor-2 mock-sensor-3
```

This matches the intended topology:

- `center` binds the ZMQ endpoints
- sensors connect to `center:5555`
- display subscribes to `center:5556`
- motor subscribes to `center:5557`

## Default Services and Ports

Default host ports:

- display: `http://localhost:8080/`
- display latest payload: `http://localhost:8080/state`
- mock-override-button HTTP API: `http://localhost:18084/`
- mock-sensor-1 HTTP API: `http://localhost:18081/`
- mock-sensor-2 HTTP API: `http://localhost:18082/`
- mock-sensor-3 HTTP API: `http://localhost:18083/`

Runtime component identities:

- center sender id: `capstone-center`
- motor component id: `motor-dev-001`
- mock-override-button device id: `override-button-001`
- mock-sensor-1 device id: `mock-sensor-001`
- mock-sensor-2 device id: `mock-sensor-002`
- mock-sensor-3 device id: `thermal-mock-001`

## Override Control

The override helper exposes a small HTTP API.

Check the current override state:

```bash
curl http://localhost:18084/state
```

Enable override mode:

```bash
curl -X POST http://localhost:18084/override \
  -H "Content-Type: application/json" \
  -d '{"value": true}'
```

Disable override mode:

```bash
curl -X POST http://localhost:18084/override \
  -H "Content-Type: application/json" \
  -d '{"value": false}'
```

## Mock Sensor Control

Each mock sensor exposes a small HTTP API.

Check current state:

```bash
curl http://localhost:18081/state
```

Mark a human as detected:

```bash
curl -X POST http://localhost:18081/human \
  -H "Content-Type: application/json" \
  -d '{"value": true}'
```

Clear human detection:

```bash
curl -X POST http://localhost:18081/human \
  -H "Content-Type: application/json" \
  -d '{"value": false}'
```

Disable publishing from a sensor:

```bash
curl -X POST http://localhost:18081/active \
  -H "Content-Type: application/json" \
  -d '{"value": false}'
```

Enable publishing again:

```bash
curl -X POST http://localhost:18081/active \
  -H "Content-Type: application/json" \
  -d '{"value": true}'
```

Use the matching port for each sensor:

- `18081` for `mock-sensor-1`
- `18082` for `mock-sensor-2`
- `18083` for `mock-sensor-3`
- `18084` for `mock-override-button`

Example: make only sensor 2 detect a human:

```bash
curl -X POST http://localhost:18081/human -H "Content-Type: application/json" -d '{"value": false}'
curl -X POST http://localhost:18082/human -H "Content-Type: application/json" -d '{"value": true}'
curl -X POST http://localhost:18083/human -H "Content-Type: application/json" -d '{"value": false}'
```

## Logs

Follow the main services:

```bash
docker compose -f Docker/development/docker-compose.yml logs -f \
  center motor display mock-override-button mock-sensor-1 mock-sensor-2 mock-sensor-3
```

Useful things to look for:

- `center` receiving sensor messages
- `motor` receiving motor orders
- `mock motor started order=...`
- display JSON updates

## Optional Profiles

### Real Thermal Publisher

The real thermal publisher is not part of the default PC stack.
It requires hardware access and is placed behind the `thermal-real` profile.

Start it explicitly:

```bash
docker compose -f Docker/development/docker-compose.yml \
  --profile thermal-real up -d publisher
```

### Thermal Visualizer

The thermal visualizer is optional and uses the `visual` profile.

Start it together with the real thermal publisher:

```bash
docker compose -f Docker/development/docker-compose.yml \
  --profile thermal-real --profile visual up -d publisher visualizer
```

Then open:

```text
http://localhost:8000/
```

## Port Overrides

You can override host ports at startup without editing files.

Example:

```bash
DISPLAY_HTTP_PORT=9080 \
MOCK_SENSOR_1_HTTP_PORT=19081 \
MOCK_SENSOR_2_HTTP_PORT=19082 \
MOCK_SENSOR_3_HTTP_PORT=19083 \
MOCK_OVERRIDE_HTTP_PORT=19084 \
docker compose -f Docker/development/docker-compose.yml up -d
```

The included component compose files still keep their own default values, so
they can be started independently for local testing.

## Troubleshooting

If a host port is already in use, override it on the command line:

```bash
MOCK_SENSOR_1_HTTP_PORT=19081 docker compose -f Docker/development/docker-compose.yml up -d
```

If the stack looks stale after config changes, recreate it:

```bash
docker compose -f Docker/development/docker-compose.yml up -d --build --force-recreate
```
