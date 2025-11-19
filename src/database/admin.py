from .models import User


def add_admin(telegram_id: int):
    if not is_admin_exist(telegram_id):
        User.update(admin=True).where(User.telegram_id == telegram_id).execute()


def delete_admin(telegram_id: int) -> bool:
    try:
        User.update(admin=False).where(User.telegram_id == telegram_id).execute()
    except User.DoesNotExist:
        return False
    else:
        return True


def get_admins():
    return [(user.telegram_id, user.name) for user in User.select().where(User.admin == True)]


def get_admin_ids():
    return [user.telegram_id for user in User.select().where(User.admin == True)]


def is_admin_exist(telegram_id: int):
    admin = User.get_or_none(User.telegram_id == telegram_id)
    return True if admin else False

