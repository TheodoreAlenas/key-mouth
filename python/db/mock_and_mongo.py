from dataclasses import dataclass


@dataclass
class LastPages:
    pages: list
    first_page_idx: int


@dataclass
class RoomRestartData:
    room_id: any
    name: str
    pages_n: int


@dataclass
class ReloadableState:
    last_id: any
    unsaved_pages: dict | None
