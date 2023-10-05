from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class PowerState:
    battery_percent: Optional[int]
    battery_seconds: Optional[int]
    on_battery: bool
    no_battery: bool
    charging: bool
    charged: bool
    plugged_in: bool
    has_battery: bool
