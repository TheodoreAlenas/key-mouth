from dataclasses import dataclass


@dataclass
class NewPage:
    conn_id = 0
    first_moment_idx: int


@dataclass
class NewMoment:
    conn_id = 0
    time: float


@dataclass
class Write:
    conn_id: int
    text: str


@dataclass
class Delete:
    conn_id: int
    text: str


@dataclass
class Note:
    conn_id: int
    text: str
