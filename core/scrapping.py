from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import re
import time

def update_links(channel, source_link):
    # Настройки за Selenium (headless режим, без отваряне на графичен браузър)
    options = Options()
    options.headless = True  # Работи в headless режим (без графичен интерфейс)
    
    # Пътят към ChromeDriver (използвай правилния път за твоя компютър)
    driver = webdriver.Chrome(executable_path=r'път_към_chromedriver', options=options)

    try:
        # Зареждаме URL-то на канала
        driver.get(source_link)
        
        # Изчакваме малко, за да се зареди динамично съдържанието (ако е необходимо)
        time.sleep(5)  # Този таймаут може да бъде настроен според нуждите

        # Вземаме HTML съдържанието на страницата
        page_source = driver.page_source
        
        # Логваме част от съдържанието на страницата, за да видим дали линкът е там
        print(f"Page source snippet: {page_source[:500]}...")  # Показваме само първите 500 символа за да видим как изглежда съдържанието

        # Регулярен израз за намиране на m3u линковете
        match = re.search(r'https://[^\s"]+\.m3u8(?:\?[^\s"]*)?', page_source)
        
        if match:
            m3u_link = match.group(0)  # Извличаме намерения линк
            print(f"Fetched m3u link for {channel}: {m3u_link}")
            return m3u_link
        else:
            print(f"No m3u link found for {channel}")
            return None
    except Exception as e:
        print(f"Error occurred while fetching m3u link for {channel}: {e}")
        return None
    finally:
        # Затваряме драйвера
        driver.quit()

# Пример за използване на функцията
channel = "#EXTINF:-1 tvg-name=\"БНТ 1\" tvg-logo=\"https://www.glebul.com/images/tv-logo/bnt-1-hd.png\" group-title=\"ЕФИРНИ\" , BNT 1 HD"
source_link = "https://www.seir-sanduk.com/?id=hd-bnt-1-hd&pass=&hash="  # Примерен линк

m3u_link = update_links(channel, source_link)
if m3u_link:
    print(f"Final m3u link: {m3u_link}")
