from dataclasses import dataclass
from typing import Optional, List

@dataclass
class Board:
    board_name: str
    title: str

@dataclass
class Reply:
    reply_id: int
    creation_time: str # DateTime on Python != DateTime on SQL
    content: str
    replies_metioned: Optional[List[int]] = None
    filename: Optional[str] = None
    anon_name: Optional[str] = None
    anon_id: Optional[str] = None
    anon_country: Optional[str] = None

@dataclass
class Thread:
    board_name: str
    thread_number: int
    title: str
    replies: List[Reply]