from typing import List, Optional
from collections.abc import ByteString
from typing_extensions import deprecated

def init() -> None:"""Deprecated since 2.2.0. Use the new API instead"""
def get_init() -> bool:"""Deprecated since 2.2.0. Use the new API instead"""
def get(data_type: str, /) -> Optional[bytes]:"""Deprecated since 2.2.0. Use the new API instead"""
def get_types() -> List[str]:"""Deprecated since 2.2.0. Use the new API instead"""
def put(data_type: str, data: ByteString, /) -> None:"""Deprecated since 2.2.0. Use the new API instead"""
def contains(data_type: str, /) -> bool:"""Deprecated since 2.2.0. Use the new API instead"""
def lost() -> bool:"""Deprecated since 2.2.0. Use the new API instead"""
def set_mode(mode: int, /) -> None:"""Deprecated since 2.2.0. Use the new API instead"""
def put_text(text: str, /) -> None: ...
def get_text() -> str: ...
def has_text() -> bool: ...
