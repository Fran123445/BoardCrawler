from dataclasses import dataclass, field
from typing import Optional, List

@dataclass
class Board:
    board_name: str
    title: str

@dataclass
class AttachedFile:
    file_id: int
    filename: str
    extension: str
    size: int
    height: int
    width: int

@dataclass
class Reply:
    reply_id: int
    creation_time: int # timestamp
    content: str
    replies_metioned: Optional[List[int]] = None
    file: Optional[AttachedFile] = None
    anon_name: Optional[str] = None
    anon_id: Optional[str] = None
    anon_country: Optional[str] = None

@dataclass
class Thread:
    board_name: str
    thread_number: int
    title: Optional[str] = None
    replies: List[Reply] = field(default_factory=list)