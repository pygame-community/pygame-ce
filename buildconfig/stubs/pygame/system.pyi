from typing import List, Optional

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
def get_pref_path(org: str, app: str) -> str: ...
def get_pref_locales() -> List[_Locale]: ...
