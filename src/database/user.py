from typing import Generator
from datetime import datetime, timedelta
from peewee import IntegrityError

from src.database.models import User, Target, Advertisement


SUPPORTED_LANGUAGE_CODES = {'ru', 'uk', 'en'}


def normalize_language_code(language_code: str | None) -> str:
    if not language_code:
        return 'ru'

    normalized_code = language_code.lower().split('-')[0]
    return normalized_code if normalized_code in SUPPORTED_LANGUAGE_CODES else 'ru'


def create_user_if_not_exist(username: str, first_name: str, last_name: str, telegram_id: int,
                             language_code: str | None = None) -> bool:
    if not get_user_by_telegram_id_or_none(telegram_id):
        User.create(
            username=username,
            first_name=first_name,
            last_name=last_name,
            telegram_id=telegram_id,
            language_code=normalize_language_code(language_code),
        )
        return True
    return False


def create_target(user_telegram_id: int, target_name: str, target_url: str, chat_id: str):
    user = User.get(telegram_id=user_telegram_id)
    Target.create(user=user, name=target_name, url=target_url, chat_id=chat_id)


def get_user_targets(user_telegram_id: int) -> [Target]:
    user = User.get_or_none(User.telegram_id == user_telegram_id)
    if user is None:
        return None
    user_targets = Target.select().where(Target.user == user).order_by(Target.id)
    return user_targets


def get_user_target(user_telegram_id: int, target_id: int) -> Target | None:
    return (Target
            .select()
            .join(User)
            .where(Target.id == target_id, User.telegram_id == user_telegram_id)
            .first())


def update_target(target_id: int, **fields) -> int:
    if 'chat_id' in fields:
        fields['chat_id'] = str(fields['chat_id'])

    return Target.update(**fields).where(Target.id == target_id).execute()

def add_advertisement(ad_url: str, target_id: int):
    try:
        Advertisement.create(url=ad_url, target_id=target_id)
        return True
    except IntegrityError:
        return False

def get_all_targets() -> [Target]:
    return Target.select().join(User).where(Target.active == True).order_by(Target.id)


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
        return normalize_language_code(User.get(User.telegram_id == telegram_id).language_code)
    except User.DoesNotExist:
        return None


def set_locale(telegram_id: int, language_code: str) -> None:
    User.update(language_code=normalize_language_code(language_code)).where(User.telegram_id == telegram_id).execute()

