import asyncio
import requests

from aiogram.types import ParseMode
from bs4 import BeautifulSoup
from datetime import datetime
from zoneinfo import ZoneInfo

import pytz

from src.create_bot import bot
from src.database.user import get_all_targets, add_advertisement
from src.handlers.user.kb import Keyboards
from src.utils import logger


class Parser:
    async def search_ads(self):
        all_targets = get_all_targets()
        for target in all_targets:
            ads_found = await self.__parse_last_three_olx_ads(target.url)
            for ad in ads_found:
                # Save advertisement to the database and if it did not exist send message to user
                successfully_added_advertisement = add_advertisement(ad['link'], target.id)
                if successfully_added_advertisement:
                    ad_text = f"**{ad['title']}**\nЦена: {ad['price']}\nВремя публикации: {ad['time']}\nЛокация: {ad['location']}"
                    logger.info(ad_text)
                    await bot.send_photo(chat_id=target.chat_id,
                                         photo=ad['photo_url'],
                                         caption=ad_text,
                                         parse_mode=ParseMode.MARKDOWN,
                                         reply_markup=Keyboards.get_url_keyboard(ad['link']))



    async def __parse_last_three_olx_ads(self, target_url: str):
        ads = []

        # Parse OLX.ua page
        response = requests.get(target_url)
        soup = BeautifulSoup(response.content, 'lxml')
        ad_items = soup.find_all('div', class_='css-1sw7q4x')

        for ad_item in ad_items[3:7]:
            try:
                title = ad_item.find('h4', class_='css-hzlye5').text.strip()
                location_and_time_text = ad_item.find('p', class_='css-1b24pxk').text.strip()
                location = location_and_time_text[:location_and_time_text.find(' -')]
                # Parse publish time and convert it to user_timezone
                publish_time_text = location_and_time_text[location_and_time_text.find('- ') + 2:]
                # If time text doesn't start with Сьогодні it means that it was published days before,
                # and it doesn't have time
                if not publish_time_text.startswith('Сьогодні'):
                    publish_time = publish_time_text
                else:
                    time_text = publish_time_text.split()[-1]
                    publish_time = await self.__convert_publish_time(time_text, 'Europe/Kiev', 'UTC')

                price = ad_item.find('p', class_='css-blr5zl').text.strip()

                link = 'https://www.olx.ua' + ad_item.find('a', class_='css-1tqlkj0').get('href')
                # Follow the link in the ad
                ad_response = requests.get(link)
                ad_soup = BeautifulSoup(ad_response.content, 'lxml')

                photo_url = ad_soup.find('img', class_='css-1bmvjcs').get('src')
                ads.append({
                    'title': title,
                    'price': price,
                    'link': link,
                    'photo_url': photo_url,
                    'time': publish_time,
                    'location': location + ' '
                })
            except Exception as e:
                logger.error(f"Exception raised: {e}")
        return ads

    @staticmethod
    async def __convert_publish_time(time: str, user_time_zone: str, original_time_zone: str) -> str:
        """
        Convert time to users timezone

        """
        user_timezone = pytz.timezone(user_time_zone)
        machine_tz = ZoneInfo(original_time_zone)

        publish_time = datetime.strptime(time, '%H:%M').time()
        today_in_src = datetime.now(machine_tz).date()
        machine_date_time = datetime.combine(today_in_src, publish_time, tzinfo=machine_tz)
        user_dt = machine_date_time.astimezone(user_timezone)
        user_publish_time_str = user_dt.strftime("%H:%M")

        return user_publish_time_str


if __name__ == '__main__':
    result = asyncio.run(Parser()._Parser__parse_last_three_olx_ads('https://www.olx.ua/uk/transport/legkovye-avtomobili/tesla/?currency=USD&search%5Bfilter_float_price:to%5D=30000'))
    print(result)
