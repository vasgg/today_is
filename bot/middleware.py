from datetime import datetime
from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.types import Message
from bot.models import User
from bot.database import session
from sqlalchemy import select, literal
from bot.config import redis


class AuthMiddleware(BaseMiddleware):
    async def on_process_message(self, message: Message, data: dict):
        now = datetime.utcnow()

        user = session.query(User.user_id).filter(User.user_id == message.from_user.id)
        user_exist = session.query(literal(True)).filter(user.exists()).scalar()

        redis.incrby('total', 1)
        redis.incrby(f'user:{message.from_user.id}', 1)

        if not user_exist:
            user = User(user_id=message.from_user.id,
                        firstname=message.from_user.first_name,
                        lastname=message.from_user.last_name,
                        username=message.from_user.username,
                        created_at=now,
                        updated_at=now,
                        language_code=message.from_user.language_code)
            session.add(user)
            session.commit()
            session.close()
