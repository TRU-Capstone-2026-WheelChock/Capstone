import os
import threading
import time

import msg_handler
from msg_handler import ZmqPubOptions, get_publisher
import msg_handler.schemas as mschema

from state import OverrideState

CENTER_ENDPOINT = os.environ.get("CENTER_ENDPOINT", "tcp://127.0.0.1:5555")
DEVICE_ID = os.environ.get("DEVICE_ID", "override-button-001")
DEVICE_NAME = os.environ.get("DEVICE_NAME", "mock-override-button")
PUBLISH_INTERVAL = float(os.environ.get("PUBLISH_INTERVAL_SEC", "1.0"))

_generic_data_types = getattr(msg_handler, "GenericMessageDatatype", None)
OVERRIDE_DATA_TYPE = getattr(_generic_data_types, "OVERRIDE_BUTTON", None)
if OVERRIDE_DATA_TYPE is None:
    OVERRIDE_DATA_TYPE = getattr(mschema.GenericMessageDatatype, "OVERRIDE_BUTTON", "override_button")


def _run(state: OverrideState) -> None:
    options = ZmqPubOptions(endpoint=CENTER_ENDPOINT)
    with get_publisher(options) as pub:
        print(f"[pub] connected to {CENTER_ENDPOINT}", flush=True)
        while True:
            current = state.get_state()
            msg = mschema.SensorMessage(
                sender_id=DEVICE_ID,
                sender_name=DEVICE_NAME,
                data_type=OVERRIDE_DATA_TYPE,
                payload=mschema.HeartBeatPayload(
                    status=current["status"],
                    status_code=200,
                ),
            )
            pub.send(msg)
            print(
                f"[pub] seq={msg.sequence_no} override={current['override']} status={current['status']}",
                flush=True,
            )
            time.sleep(PUBLISH_INTERVAL)


def start_publisher(state: OverrideState) -> threading.Thread:
    t = threading.Thread(target=_run, args=(state,), daemon=True)
    t.start()
    return t
