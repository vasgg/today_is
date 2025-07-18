from aiogram.filters.callback_data import CallbackData

from bot.internal.enums import MenuAction, MenuSection, RecordAction


class MenuActionsCallbackFactory(CallbackData, prefix="menu_action"):
    action: MenuAction


class RecordActionCallbackFactory(CallbackData, prefix="record_action"):
    action: RecordAction


class ChooseRecordCallbackFactory(CallbackData, prefix="choose_record"):
    record_id: int


class DeleteRecordCallbackFactory(CallbackData, prefix="delete_record"):
    record_id: int


class MenuSectionCallbackFactory(CallbackData, prefix="menu_section"):
    section: MenuSection
