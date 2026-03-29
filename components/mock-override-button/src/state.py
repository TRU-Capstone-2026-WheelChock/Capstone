import threading
from dataclasses import dataclass, field


@dataclass
class OverrideState:
    override_enabled: bool = False
    _lock: threading.Lock = field(default_factory=threading.Lock, repr=False, compare=False)

    def set_override_enabled(self, value: bool) -> None:
        with self._lock:
            self.override_enabled = value

    def get_state(self) -> dict:
        with self._lock:
            status = "override" if self.override_enabled else "active"
            return {"override": self.override_enabled, "status": status}
