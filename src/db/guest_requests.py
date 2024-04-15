from sqlalchemy import insert, select, update
from src.db.models import *
from src.db.SQL_session import *


async def add_user(name: str,
                   nickname: str,
                   email: str,
                   password: str,
                   role: str,
                   session: AsyncSession) -> int:
    stmt = insert(user).values(
        name=name,
        nickname=nickname,
        email=email,
        password=password,
        role=role
    ).returning(user.c.id)

    result = await session.execute(stmt)
    user_id = result.scalar_one()
    await session.commit()

    return user_id


async def add_user_if_not_exists(session: AsyncSession,
                                 name: str,
                                 nickname: str,
                                 email: str,
                                 password: str,
                                 role: str):
    stmt = select(user).where(user.c.nickname == nickname,
                              user.c.email == email)
    result = await session.execute(stmt)
    user_exists = result.scalar_one_or_none() is not None

    if not user_exists:
        stmt = insert(user).values(
            name=name,
            nickname=nickname,
            email=email,
            password=password,
            role=role,
            registered_at=datetime.utcnow()
        )
        await session.execute(stmt)
        await session.commit()


async def update_user(session: AsyncSession,
                                 name: str,
                                 nickname: str,
                                 email: str,
                                 password: str,
                                 role: str):
    try:
        update_user_stmt = (update(user)
        .where(user.c.nickname == nickname)
        .values(
            name=name,
            email=email,
            password=password,
            role=role
        ))
        await session.execute(update_user_stmt)
        await session.commit()
        return True
    except:
        return False


async def find_user_by_nickname(session: AsyncSession, nickname: str):
    stmt = select(user).where(user.c.nickname == nickname)
    result = await session.execute(stmt)
    user_record = result.one_or_none()

    if user_record:
        return {
            "id": user_record.id,
            "name": user_record.name,
            "nickname": user_record.nickname,
            "email": user_record.email,
            "password": user_record.password,
            "role": user_record.role,
            "registered_at": user_record.registered_at
        }
    else:
        return None


async def find_user_by_email(session: AsyncSession, email: str):
    stmt = select(user).where(user.c.email == email)
    result = await session.execute(stmt)
    user_record = result.one_or_none()

    if user_record:
        return {
            "id": user_record.id,
            "name": user_record.name,
            "nickname": user_record.nickname,
            "email": user_record.email,
            "password": user_record.password,
            "role": user_record.role,
            "registered_at": user_record.registered_at
        }
    else:
        return None
