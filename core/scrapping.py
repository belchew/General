from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By  # Импортиране на By
import time

# Структура за каналите
channel_mapping = {
    '#EXTINF:-1 tvg-name="БНТ 1" tvg-logo="https://www.glebul.com/images/tv-logo/bnt-1-hd.png" group-title="ЕФИРНИ" , BNT 1 HD': 'https://www.seir-sanduk.com/?id=hd-bnt-1-hd&pass=&hash=',
}

# Функция за търсене на линкове с Selenium
def update_links_selenium(channel, source_link):
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Стартира браузъра в "headless" режим (без графичен интерфейс)
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    # Създаване на WebDriver с автоматично конфигуриран ChromeDriver
    service = Service(ChromeDriverManager().install())  # Използваме Service за ChromeDriver
    driver = webdriver.Chrome(service=service, options=chrome_options)  # Премахваме директния път към ChromeDriver

    driver.get(source_link)
    time.sleep(5)  # Изчакване за зареждане на страницата

    try:
        # Търсене на линкове съдържащи "index.m3u8" в текста
        m3u_link_elements = driver.find_elements(By.XPATH, '//*[contains(@href, "index.m3u8")]')  # Променено тук

        # Извличаме всички намерени линкове
        m3u_links = [element.get_attribute("href") for element in m3u_link_elements]

        if m3u_links:
            print(f"Fetched m3u links for {channel}: {m3u_links}")
            return m3u_links
        else:
            print(f"No m3u links found for {channel}")
            return None
    except Exception as e:
        print(f"Error finding m3u links for {channel}: {e}")
        return None
    finally:
        driver.quit()

# Използваме функцията за извличане на линкове
data_list = []
m3u_links = []

for channel, source_link in channel_mapping.items():
    fetched_links = update_links_selenium(channel, source_link)
    data_list.append({'Channel': channel, 'SourceLink': source_link, 'LinkToUpdate': fetched_links})
    if fetched_links:  # Ако линкове са намерени, ги добавяме в списъка
        for link in fetched_links:
            m3u_links.append(f"{channel}\n{link}")

# Записваме новите линкове в .m3u файл
file_path = 'sources.m3u'
with open(file_path, 'w') as file:
    file.write('#EXTM3U catchup="flussonic" url-tvg="https://github.com/harrygg/EPG/raw/refs/heads/master/all-2days.details.epg.xml.gz"\n')  # Добавяме на първия ред #EXTM3U
    for link in m3u_links:
        file.write(link + '\n')

print(f"File {file_path} successfully updated with new links.")
