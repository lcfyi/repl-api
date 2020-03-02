from enum import Enum


class Language(Enum):
    def __str__(self):
        return str(self.name)

    javascript = 1
    java = 2
    python = 3
    c = 4
    cpp = 5
