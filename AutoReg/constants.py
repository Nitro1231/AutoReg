from enum import Enum


class Mode(Enum):
    ADD     = 'add'
    CHANGE  = 'change'
    DROP    = 'drop'
    LIST    = 'listOpen' # List Open Sections	


class GradeOption(Enum):
    GRADE   = 1
    PNP     = 2 # P/NP
