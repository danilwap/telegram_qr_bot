from dataclasses import dataclass

@dataclass(frozen=True)
class Config:
    dev_check: bool
    channel_id: int
    admins: list[int]
