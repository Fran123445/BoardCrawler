from dataclasses import dataclass, field
from typing import Optional, List

@dataclass
class Board:
    board_name: str
    title: str

@dataclass
class AttachedFile:
    filename: str
    file_timestamp: int
    extension: str
    size: int
    width: int
    height: int

@dataclass
class Post:
    post_id: int
    creation_time: int # timestamp
    content: str
    posts_metioned: Optional[List[int]] = None
    file: Optional[AttachedFile] = None
    anon_name: Optional[str] = None
    anon_id: Optional[str] = None
    anon_country: Optional[str] = None

@dataclass
class Thread:
    board_name: str
    thread_number: int
    title: Optional[str] = None
    posts: List[Post] = field(default_factory=list)