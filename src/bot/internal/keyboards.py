from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder

from bot.internal.callbacks import (
    ChooseRecordCallbackFactory,
    DeleteRecordCallbackFactory,
    MenuActionsCallbackFactory,
    MenuSectionCallbackFactory,
    RecordActionCallbackFactory,
)
from bot.internal.enums import MenuAction, MenuSection, RecordAction
from database.models import Record


tools = InlineKeyboardMarkup(
    row_width=2,
    inline_keyboard=[
        [
            InlineKeyboardButton(text="days counter", callback_data="days_counter"),
            InlineKeyboardButton(text="date calculator", callback_data="date_calculator"),
        ]
    ],
)


def provide_location_kb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.add(KeyboardButton(text="update location", request_location=True))
    return kb.as_markup(resize_keyboard=True, one_time_keyboard=True)


def add_record_kb(with_delete: bool = False) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.add(
        InlineKeyboardButton(
            text="add record", callback_data=RecordActionCallbackFactory(action=RecordAction.ADD_RECORD).pack()
        )
    )
    if with_delete:
        kb.add(
            InlineKeyboardButton(
                text="delete record",
                callback_data=RecordActionCallbackFactory(action=RecordAction.DELETE_RECORD).pack(),
            )
        )
    return kb.as_markup()


def delete_record_kb(records: list[Record]) -> InlineKeyboardMarkup:
    count = len(records)
    kb = InlineKeyboardBuilder()
    for i, record in enumerate(records, start=1):
        kb.add(
            InlineKeyboardButton(text=f"{i}", callback_data=ChooseRecordCallbackFactory(record_id=record.id).pack())
        )
    kb.add(
        InlineKeyboardButton(text="cancel", callback_data=MenuActionsCallbackFactory(action=MenuAction.CANCEL).pack())
    )
    kb.adjust(*([4] * (count // 4)) + ([count % 4] if count % 4 else []), 1)
    return kb.as_markup()


def delete_record_confirm_kb(record_id: int) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.add(InlineKeyboardButton(text="yes", callback_data=DeleteRecordCallbackFactory(record_id=record_id).pack()))
    kb.add(
        InlineKeyboardButton(text="no", callback_data=MenuSectionCallbackFactory(section=MenuSection.RECORDS).pack())
    )
    return kb.as_markup()
