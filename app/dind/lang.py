from enum import Enum


class Language(Enum):
    def __str__(self):
        return str(self.name)

    def getTagname(self):
        return f"{str(self.name)}-image"

    javascript = 1
    java = 2
    python = 3
