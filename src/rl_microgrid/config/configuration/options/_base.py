from enum import Enum


class IOptions(Enum):
    def __str__(self):
        return self.value
