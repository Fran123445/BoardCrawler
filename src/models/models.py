from dataclasses import dataclass
from typing import Optional

@dataclass
class Board:
    board_name: str
    title: str
    id: Optional[int] = None

@dataclass
class Thread:
    board_id: int
    thread_number: int
    title: str

@dataclass
class Reply:
    board_id: int
    reply_id: int
    creation_time: str # DateTime de Python != DateTime de SQL
    content: str
    filename: Optional[str] = None
    anon_name: Optional[str] = None
    anon_id: Optional[str] = None
    anon_country: Optional[int] = None
    replies_mentioned: Optional[int] = None

@dataclass
class Countries:
    country_id: int
    country_name: str

@dataclass
class ReplyMentions:
    board_id: int
    reply_id: int
    mentioned_reply: int