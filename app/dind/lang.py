from enum import Enum


class Language(Enum):
    def __str__(self):
        return str(self.name)

    def get_tag(self):
        return f"{str(self.name)}-image"

    javascript = 1
    java = 2
    python = 3
    c = 4
    cpp = 5
