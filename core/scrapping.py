import time
import re
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Channel mapping (пример)
channel_mapping = {
    '#EXTINF:-1 tvg-name="БНТ 1" tvg-logo="https://www.glebul.com/images/tv-logo/bnt-1-hd.png" group-title="ЕФИРНИ" , BNT 1 HD': 'https://www.seir-sanduk.com/?id=hd-bnt-1-hd&pass=&hash=',
}

# Функция за извличане на m3u8 линкове с Selenium
def fetch_m3u8_link_with_selenium(url):
    # Конфигурираме Selenium с headless режим (без да се отваря графичен браузър)
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    
    # Стартиране на браузъра
    driver = webdriver.Chrome(options=options)
    
    try:
        driver.get(url)
        
        # Изчакваме да се заредят динамични елементи на страницата (например плеър или линкове)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
        
        # Изчакваме още малко време за да се заредят всички елементи
        time.sleep(5)
        
        # Вземане на HTML съдържанието след като се е заредило
        page_source = driver.page_source
        print(f"Fetched content from {url}:\n{page_source[:500]}")  # Показваме първите 500 символа от HTML
        
        # Извличане на m3u8 линкове
        match = re.search(r'https://[^\s"]+\.m3u8(?:\?[^\s"]*)?', page_source)
        if match:
            m3u_link = match.group(0)
            print(f"Found m3u8 link: {m3u_link}")
            return m3u_link
        else:
            print("No m3u8 link found.")
            return None
    except Exception as e:
        print(f"Error fetching content from {url}: {e}")
        return None
    finally:
        driver.quit()  # Затваряме браузъра след края на изпълнението

# Главен скрипт за обработка на каналите
data_list = []
m3u_links = []

# Преглед на каналите и извличане на m3u8 линкове
for channel, source_link in channel_mapping.items():
    fetched_link = fetch_m3u8_link_with_selenium(source_link)
    data_list.append({'Channel': channel, 'SourceLink': source_link, 'LinkToUpdate': fetched_link})
    if fetched_link:  # Ако линкът е открит, го добавяме към m3u_links списъка
        m3u_links.append(f"{channel}\n{fetched_link}")

# Създаване на DataFrame с резултатите
channel_df = pd.DataFrame(data_list)

# Път до m3u файла
file_path = 'sources.m3u'

# Записване на m3u линковете в файла
with open(file_path, 'w') as file:
    file.write('#EXTM3U catchup="flussonic" url-tvg="https://github.com/harrygg/EPG/raw/refs/heads/master/all-2days.details.epg.xml.gz"\n')
    for link in m3u_links:
        file.write(link + '\n')

print(f"File {file_path} successfully updated with new links.")
