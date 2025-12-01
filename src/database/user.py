from peewee import IntegrityError
from typing import Generator
from datetime import datetime, timedelta

from src.database.models import User, Target, Advertisement
from src.utils import logger


def create_user_if_not_exist(username: str, first_name: str, last_name: str, telegram_id: int) -> bool:
    if not get_user_by_telegram_id_or_none(telegram_id):
        User.create(username=username, first_name=first_name, last_name=last_name, telegram_id=telegram_id)
        return True
    return False


def create_target(user_telegram_id: int, target_name: str, target_url: str, chat_id: str):
    user = User.get(telegram_id=user_telegram_id)
    Target.create(user=user, name=target_name, url=target_url, chat_id=chat_id)


def get_user_targets(user_telegram_id: int) -> [Target]:
    user = User.get_or_none(User.telegram_id == user_telegram_id)
    if user is None:
        return None
    user_targets = Target.select().where(Target.user == user)
    return user_targets

def add_advertisement(ad_url: str, target_id: int):
    try:
        Advertisement.create(url=ad_url, target_id=target_id)
        return True
    except IntegrityError:
        return False

def get_all_targets() -> [Target]:
    return Target.select().order_by(Target.id)


def get_users_total_count() -> int:
    return User.select().count()


def get_users_by_hours(hours: int):
    start_time = datetime.now() - timedelta(hours=hours)
    users_count = User.select().where(User.registration_timestamp >= start_time).count()

    return users_count


def get_user_ids() -> Generator:
    yield from (user.telegram_id for user in User.select())


def get_all_users() -> tuple:
    yield from ((user.username, user.first_name, user.last_name, user.telegram_id) for
                user in User.select())


def get_user_by_telegram_id_or_none(telegram_id: int) -> None:
    return User.get_or_none(User.telegram_id == telegram_id)


def get_locale(telegram_id: int) -> str | None:
    try:
        return User.get(User.telegram_id == telegram_id).language_code
    except User.DoesNotExist:
        return None


def get_user_1win_id(telegram_id: int) -> int:
    return User.get(User.telegram_id == telegram_id).onewin_id


def check_onewin_id(onewin_id: int):
    onewin_object = WinId.get_or_none(onewin_id=onewin_id)
    return onewin_object is not None


def set_user_1win_id(telegram_id: int, onewin_id: int):
    User.update(onewin_id=onewin_id).where(User.telegram_id == telegram_id).execute()


def set_1win_deposit(onewin_id: int):
    user, created = User.get_or_create(onewin_id=onewin_id, defaults={'deposit': True})
    if not created:
        user.deposit = True
        user.save()


def check_user_deposit(telegram_id: int) -> int:
    return User.get(User.telegram_id == telegram_id).deposit


def set_locale(telegram_id: int, language_code: str) -> None:
    User.update(language_code=language_code).where(User.telegram_id == telegram_id).execute()


