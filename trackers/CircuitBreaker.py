
from dataclasses import dataclass,field
import time

@dataclass
class CircuitBreaker:
    failure_threshold: int = 5
    reset_timeout: float = 60.0  # seconds
    failures: int = 0
    state: str = "closed"  # "closed" | "open" | "half-open"
    last_failure_time: float = field(default_factory=time.time)

    def allow_request(self) -> bool:
        if self.state == "open":
            if time.time() - self.last_failure_time > self.reset_timeout:
                self.state = "half-open"
                return True  # allow one trial request
            return False
        return True
    
    def record_success(self) -> None:
        self.failures = 0
        self.state = "closed"

    def record_failure(self) -> None:
        self.failures += 1
        if self.failures >= self.failure_threshold:
            self.state = "open"
            self.last_failure_time = time.time()