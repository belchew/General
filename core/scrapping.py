import os
import base64
import re
import pandas as pd
import requests
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Каналите и техните линкове
channel_mapping = {
    '#EXTINF:-1 tvg-name="БНТ 1" tvg-logo="https://www.glebul.com/images/tv-logo/bnt-1-hd.png" group-title="ЕФИРНИ" , BNT 1 HD': 'https://www.seir-sanduk.com/?id=hd-bnt-1-hd&pass=&hash=',
}

# Функция за откриване на m3u линкове чрез Selenium
def update_links_with_selenium(channel, source_link):
    # Опции за браузъра Chrome (или Chromium в GitHub Actions)
    options = Options()
    options.add_argument('--headless')  # Стартира браузъра без графичен интерфейс
    options.add_argument('--no-sandbox')  # Това е необходимо за GitHub Actions
    options.add_argument('--disable-dev-shm-usage')  # За да избегнем проблеми с паметта в CI среда
    options.binary_location = os.environ.get('CHROME_BIN', '/usr/bin/chromium-browser')  # Път до Chromium в CI

    # Инициализация на WebDriver с конфигурираните опции
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    driver.get(source_link)
    time.sleep(5)  # Изчакваме малко време, за да се зареди съдържанието

    try:
        # Чакаме до 10 секунди за елемент с .m3u8 в href атрибута
        m3u_link = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//a[contains(@href, ".m3u8")]'))
        ).get_attribute('href')
        print(f"Fetched m3u link for {channel}: {m3u_link}")
        return m3u_link
    except Exception as e:
        print(f"Error fetching m3u link for {channel}: {e}")
        return None
    finally:
        driver.quit()

# Използваме Selenium за откриване на линковете
data_list = []
m3u_links = []

for channel, source_link in channel_mapping.items():
    fetched_link = update_links_with_selenium(channel, source_link)
    data_list.append({'Channel': channel, 'SourceLink': source_link, 'LinkToUpdate': fetched_link})
