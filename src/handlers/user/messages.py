from aiogram.types import InputFile


class Messages:
    DEFAULT_LANGUAGE = 'ru'
    SUPPORTED_LANGUAGES = ('ru', 'uk', 'en')

    LANGUAGE_NAMES = {
        'ru': '🇷🇺 Русский',
        'uk': '🇺🇦 Українська',
        'en': '🇬🇧 English',
    }

    BUTTONS = {
        'targets_menu': {'ru': 'Таргеты 🚀', 'uk': 'Таргети 🚀', 'en': 'Targets 🚀'},
        'my_targets': {'ru': 'Мои таргеты', 'uk': 'Мої таргети', 'en': 'My targets'},
        'add_target': {'ru': 'Добавить таргет ➕', 'uk': 'Додати таргет ➕', 'en': 'Add target ➕'},
        'main_menu': {'ru': 'Главное меню 🏠', 'uk': 'Головне меню 🏠', 'en': 'Main menu 🏠'},
        'language_menu': {'ru': 'Язык 🌐', 'uk': 'Мова 🌐', 'en': 'Language 🌐'},
        'cancel_target': {'ru': 'Отменить', 'uk': 'Скасувати', 'en': 'Cancel'},
    }

    TEXTS = {
        'loading': {'ru': '♻ Loading...', 'uk': '♻ Loading...', 'en': '♻ Loading...'},
        'throttled_error': {
            'ru': 'Пожалуйста, не так часто 🙏',
            'uk': 'Будь ласка, не так часто 🙏',
            'en': 'Please slow down a bit 🙏',
        },
        'welcome_text': {
            'ru': 'Добро пожаловать в бот по поиску объявлений.',
            'uk': 'Ласкаво просимо до бота для пошуку оголошень.',
            'en': 'Welcome to the listings search bot.',
        },
        'targets_menu_text': {
            'ru': 'Меню таргетов',
            'uk': 'Меню таргетів',
            'en': 'Targets menu',
        },
        'choose_target_to_edit': {
            'ru': 'Чтобы редактировать таргет, нажмите на один из них.',
            'uk': 'Щоб редагувати таргет, натисніть на один із них.',
            'en': 'Choose a target to edit it.',
        },
        'no_targets': {
            'ru': 'У вас пока нет таргетов.',
            'uk': 'У вас поки немає таргетів.',
            'en': 'You do not have any targets yet.',
        },
        'add_target_name': {
            'ru': 'Введите название таргета:',
            'uk': 'Введіть назву таргета:',
            'en': 'Enter the target name:',
        },
        'add_target_url': {
            'ru': 'Введите URL таргета (ссылка должна содержать все нужные фильтры):',
            'uk': 'Введіть URL таргета (посилання має містити всі потрібні фільтри):',
            'en': 'Enter the target URL (the link must include all required filters):',
        },
        'add_target_chat_id': {
            'ru': 'Введите chat_id, куда бот будет отправлять результаты:',
            'uk': 'Введіть chat_id, куди бот надсилатиме результати:',
            'en': 'Enter the chat_id where the bot should send results:',
        },
        'wrong_target_url': {
            'ru': 'URL таргета должен начинаться с https://',
            'uk': 'URL таргета має починатися з https://',
            'en': 'The target URL must start with https://',
        },
        'wrong_target_chat_id': {
            'ru': 'Некорректный chat_id. Проверьте, что бот имеет доступ к чату, и попробуйте снова.',
            'uk': 'Некоректний chat_id. Перевірте, що бот має доступ до чату, і спробуйте ще раз.',
            'en': 'Invalid chat_id. Make sure the bot has access to the chat and try again.',
        },
        'cancel_target': {
            'ru': 'Действие отменено.',
            'uk': 'Дію скасовано.',
            'en': 'Action canceled.',
        },
        'target_created': {
            'ru': 'Таргет успешно добавлен.',
            'uk': 'Таргет успішно додано.',
            'en': 'Target added successfully.',
        },
        'language_prompt': {
            'ru': 'Выберите язык интерфейса:',
            'uk': 'Оберіть мову інтерфейсу:',
            'en': 'Choose the interface language:',
        },
        'language_updated': {
            'ru': 'Язык обновлен.',
            'uk': 'Мову оновлено.',
            'en': 'Language updated.',
        },
        'target_not_found': {
            'ru': 'Таргет не найден.',
            'uk': 'Таргет не знайдено.',
            'en': 'Target not found.',
        },
        'edit_name_prompt': {
            'ru': 'Введите новое название таргета:',
            'uk': 'Введіть нову назву таргета:',
            'en': 'Enter the new target name:',
        },
        'edit_url_prompt': {
            'ru': 'Введите новый URL таргета:',
            'uk': 'Введіть новий URL таргета:',
            'en': 'Enter the new target URL:',
        },
        'edit_chat_id_prompt': {
            'ru': 'Введите новый chat_id:',
            'uk': 'Введіть новий chat_id:',
            'en': 'Enter the new chat_id:',
        },
        'target_updated': {
            'ru': 'Таргет обновлен.',
            'uk': 'Таргет оновлено.',
            'en': 'Target updated.',
        },
        'target_active_enabled': {
            'ru': 'Таргет включен.',
            'uk': 'Таргет увімкнено.',
            'en': 'Target enabled.',
        },
        'target_active_disabled': {
            'ru': 'Таргет выключен.',
            'uk': 'Таргет вимкнено.',
            'en': 'Target disabled.',
        },
        'enable_target': {
            'ru': 'Включить',
            'uk': 'Увімкнути',
            'en': 'Enable',
        },
        'disable_target': {
            'ru': 'Выключить',
            'uk': 'Вимкнути',
            'en': 'Disable',
        },
        'status_active': {'ru': 'Активен', 'uk': 'Активний', 'en': 'Active'},
        'status_inactive': {'ru': 'Выключен', 'uk': 'Вимкнений', 'en': 'Inactive'},
        'field_name': {'ru': 'Название', 'uk': 'Назва', 'en': 'Name'},
        'field_url': {'ru': 'Ссылка', 'uk': 'Посилання', 'en': 'URL'},
        'field_chat_id': {'ru': 'Chat ID', 'uk': 'Chat ID', 'en': 'Chat ID'},
        'field_active': {'ru': 'Статус', 'uk': 'Статус', 'en': 'Status'},
        'target_details_title': {'ru': 'Таргет', 'uk': 'Таргет', 'en': 'Target'},
        'ad_title': {'ru': 'Цена', 'uk': 'Ціна', 'en': 'Price'},
        'ad_time': {'ru': 'Время публикации', 'uk': 'Час публікації', 'en': 'Published'},
        'ad_location': {'ru': 'Локация', 'uk': 'Локація', 'en': 'Location'},
        'ad_button': {'ru': 'Объявление 🏠', 'uk': 'Оголошення 🏠', 'en': 'Open listing 🏠'},
    }

    @classmethod
    def normalize_language(cls, language_code: str | None) -> str:
        if not language_code:
            return cls.DEFAULT_LANGUAGE

        normalized_code = language_code.lower().split('-')[0]
        return normalized_code if normalized_code in cls.SUPPORTED_LANGUAGES else cls.DEFAULT_LANGUAGE

    @classmethod
    def get_text(cls, key: str, language_code: str | None = None) -> str:
        normalized_code = cls.normalize_language(language_code)
        return cls.TEXTS[key][normalized_code]

    @classmethod
    def get_button(cls, key: str, language_code: str | None = None) -> str:
        normalized_code = cls.normalize_language(language_code)
        return cls.BUTTONS[key][normalized_code]

    @classmethod
    def get_button_variants(cls, key: str) -> set[str]:
        return set(cls.BUTTONS[key].values())

    @classmethod
    def get_language_button(cls, language_code: str) -> str:
        return cls.LANGUAGE_NAMES[cls.normalize_language(language_code)]

    @classmethod
    def get_language_by_button(cls, button_text: str) -> str | None:
        for language_code, language_name in cls.LANGUAGE_NAMES.items():
            if button_text == language_name:
                return language_code
        return None

    @staticmethod
    def get_menu_photo() -> str:
        return 'https://www.google.com/url?sa=i&url=https%3A%2F%2Fcommons.wikimedia.org%2Fwiki%2FFile%3ATest-Logo.svg&psig=AOvVaw0lG3HvYAtKg_y2_IAqDwOr&ust=1763831042425000&source=images&cd=vfe&opi=89978449&ved=0CBIQjRxqFwoTCIDh4-jcg5EDFQAAAAAdAAAAABAE'

    @staticmethod
    def get_instruction_video() -> InputFile:
        return InputFile('resources/mines/instruction.mp4')

    @classmethod
    def get_target_details_text(cls, target, language_code: str | None = None) -> str:
        normalized_code = cls.normalize_language(language_code)
        status_text = cls.get_text('status_active', normalized_code) if target.active else cls.get_text('status_inactive', normalized_code)
        return (
            f"<b>{cls.get_text('target_details_title', normalized_code)}:</b> {target.name}\n"
            f"<b>{cls.get_text('field_url', normalized_code)}:</b> <code>{target.url}</code>\n"
            f"<b>{cls.get_text('field_chat_id', normalized_code)}:</b> <code>{target.chat_id}</code>\n"
            f"<b>{cls.get_text('field_active', normalized_code)}:</b> {status_text}"
        )

    @classmethod
    def get_throttled_error(cls, language_code: str | None = None) -> str:
        return cls.get_text('throttled_error', language_code)

    @classmethod
    def get_advertisement_text(cls, ad: dict, language_code: str | None = None) -> str:
        normalized_code = cls.normalize_language(language_code)
        return (
            f"<b>{ad['title']}</b>\n"
            f"{cls.get_text('ad_title', normalized_code)}: {ad['price']}\n"
            f"{cls.get_text('ad_time', normalized_code)}: {ad['time']}\n"
            f"{cls.get_text('ad_location', normalized_code)}: {ad['location']}"
        )
