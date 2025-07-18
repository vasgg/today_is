from datetime import timedelta, timezone
import logging

from aiogram import Router
from aiogram.filters import Command, StateFilter
from aiogram.types import CallbackQuery, Message
from dateutil.parser import parse
from sqlalchemy.ext.asyncio import AsyncSession
from aiogram.fsm.context import FSMContext

from bot.internal.callbacks import (
    ChooseRecordCallbackFactory,
    DeleteRecordCallbackFactory,
    MenuSectionCallbackFactory,
    RecordActionCallbackFactory,
)
from bot.internal.controllers import compose_all_records_reply, get_date_suffix
from bot.internal.enums import MenuSection, RecordAction, States
from bot.internal.keyboards import add_record_kb, delete_record_confirm_kb, delete_record_kb
from bot.internal.replies import answer
from database.crud.record import create_record, delete_record_from_user, get_all_records_from_user, get_record_by_id
from database.models import Record, User


router = Router()
logger = logging.getLogger(__name__)


@router.message(Command("records"))
async def records_command(message: Message, user: User, db_session: AsyncSession):
    records = await get_all_records_from_user(user.user_id, db_session)
    if not records:
        await message.answer(text=answer["records_reply_unregistered"], reply_markup=add_record_kb())
    else:
        reply_text = compose_all_records_reply(user.utc_offset, records)
        await message.answer(text=reply_text, reply_markup=add_record_kb(with_delete=True))


@router.callback_query(RecordActionCallbackFactory.filter())
async def event_name(
    call: CallbackQuery,
    callback_data: RecordActionCallbackFactory,
    user: User,
    db_session: AsyncSession,
    state: FSMContext,
):
    await call.answer()
    match callback_data.action:
        case RecordAction.ADD_RECORD:
            await call.message.answer(text=answer["event_name_reply"])
            await state.set_state(States.EVENT_NAME)
        case RecordAction.DELETE_RECORD:
            records = await get_all_records_from_user(user.user_id, db_session)
            kb = delete_record_kb(records)
            reply_text = "\n".join((compose_all_records_reply(user.utc_offset, records), answer["event_delete_reply"]))
            await call.message.edit_text(text=reply_text, reply_markup=kb)


@router.callback_query(ChooseRecordCallbackFactory.filter())
async def choose_record(
    call: CallbackQuery, callback_data: ChooseRecordCallbackFactory, user: User, db_session: AsyncSession
):
    await call.answer()
    record_id = callback_data.record_id
    record = await get_record_by_id(record_id, db_session)
    kb = delete_record_confirm_kb(record_id)
    await call.message.edit_text(
        text=answer["event_delete_confirm"].format(record.event_name, get_date_suffix(user.utc_offset, record)),
        reply_markup=kb,
    )


@router.callback_query(MenuSectionCallbackFactory.filter())
async def menu_section(
    call: CallbackQuery, callback_data: MenuSectionCallbackFactory, user: User, db_session: AsyncSession
):
    await call.answer()
    match callback_data.section:
        case MenuSection.RECORDS:
            records = await get_all_records_from_user(user.user_id, db_session)
            reply_text = compose_all_records_reply(user.utc_offset, records)
            await call.message.edit_text(text=reply_text, reply_markup=add_record_kb(with_delete=True))


@router.callback_query(DeleteRecordCallbackFactory.filter())
async def delete_record(
    call: CallbackQuery, callback_data: DeleteRecordCallbackFactory, user: User, db_session: AsyncSession
):
    await call.answer()
    await delete_record_from_user(callback_data.record_id, db_session)
    records = await get_all_records_from_user(user.user_id, db_session)
    if not records:
        await call.message.edit_text(text=answer["records_reply_unregistered"], reply_markup=add_record_kb())
    else:
        reply_text = compose_all_records_reply(user.utc_offset, records)
        await call.message.edit_text(text=reply_text, reply_markup=add_record_kb(with_delete=True))


@router.message(StateFilter(States.EVENT_NAME))
async def name_input(message: Message, state: FSMContext):
    name = message.text
    await state.update_data(event_name=name)
    await message.answer(text=answer["event_date_reply"])
    await state.set_state(States.EVENT_DATE)


@router.message(StateFilter(States.EVENT_DATE))
async def date_input(message: Message, state: FSMContext, user: User, db_session: AsyncSession):
    reply = message.text
    try:
        raw_date = parse(timestr=reply, dayfirst=True)
        if raw_date.tzinfo is None:
            if user.utc_offset is not None:
                tz = timezone(timedelta(hours=user.utc_offset))
            else:
                tz = timezone.utc
            date = raw_date.replace(tzinfo=tz)
        else:
            date = raw_date
        data = await state.get_data()
        name = data.get("event_name")
        record = Record(
            user_id=message.from_user.id,
            event_name=name,
            event_date=date,
        )
        await create_record(record, db_session)
        records = await get_all_records_from_user(user.user_id, db_session)
        await message.answer(
            text=compose_all_records_reply(user.utc_offset, records), reply_markup=add_record_kb(with_delete=True)
        )
        await state.set_state()
    except ValueError as e:
        await message.answer(answer["value_error_reply"])
        logger.debug(answer["value_error_log"], message.from_user.id, e, message.text)
