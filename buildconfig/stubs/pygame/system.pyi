from typing import List, Optional, final

from typing_extensions import TypedDict

class _InstructionSets(TypedDict):
    RDTSC: bool
    ALTIVEC: bool
    MMX: bool
    SSE: bool
    SSE2: bool
    SSE3: bool
    SSE41: bool
    SSE42: bool
    AVX: bool
    AVX2: bool
    AVX512F: bool
    NEON: bool
    ARMSIMD: bool
    LSX: bool
    LASX: bool

# dict at runtime, TypedDict exists solely for the typechecking benefits
class _Locale(TypedDict):
    language: str
    country: Optional[str]

def get_cpu_instruction_sets() -> _InstructionSets: ...
def get_total_ram() -> int: ...
@final
class _PowerState:
    battery_seconds: Optional[int]
    battery_percent: Optional[int]
    on_battery: bool
    no_battery: bool
    charging: bool
    charged: bool
    plugged_in: bool
    has_battery: bool

def get_pref_path(org: str, app: str) -> str: ...
def get_pref_locales() -> List[_Locale]: ...
def get_power_state() -> Optional[_PowerState]: ...
