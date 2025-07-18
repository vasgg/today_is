from enum import IntEnum, StrEnum, auto
from aiogram.fsm.state import State, StatesGroup


class States(StatesGroup):
    COUNTER = State()
    CALCULATOR = State()
    FIRST_DATE = State()
    SECOND_DATE = State()
    EVENT_NAME = State()
    EVENT_DATE = State()


class Stage(StrEnum):
    PROD = auto()
    DEV = auto()


class MenuSection(IntEnum):
    RECORDS = auto()


class MenuAction(IntEnum):
    CANCEL = auto()


class RecordAction(IntEnum):
    ADD_RECORD = auto()
    DELETE_RECORD = auto()
