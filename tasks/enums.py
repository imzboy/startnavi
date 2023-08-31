from enum import StrEnum



class ContentTypes(StrEnum):
    MP4 = "video/mp4"


class Statuses(StrEnum):
    PENDING = "pending"
    IN_PROGRESS = "in progress"
    FINNISHED = "finnished"
    FAILED = "failed"
