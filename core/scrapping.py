from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager  # Импортиране на webdriver_manager

def update_links_with_selenium(channel, source_link):
    # Настройки за Chrome драйвера
    options = Options()
    options.add_argument('--headless')  # Без графичен интерфейс (за CI/CD)
    options.add_argument('--no-sandbox')  # Избягване на проблеми в CI/CD
    options.add_argument('--disable-dev-shm-usage')  # Ограничения за ресурси в контейнерите

    # Инсталиране на ChromeDriver чрез webdriver_manager
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    driver.get(source_link)  # Отваря линка в браузъра

    # Опитайте да намерите линк с m3u
    try:
        m3u_link = driver.find_element(By.XPATH, '//*[@id="m3u_link_xpath"]')  # Замести с правилния XPath
        return m3u_link.get_attribute('href')  # Връща m3u линка
    except Exception as e:
        print(f"Error while extracting m3u link: {e}")
        return None
    finally:
        driver.quit()  # Затваряме браузъра след приключване

def main():
    channels = [
        {"name": "БНТ 1", "link": "https://www.seir-sanduk.com/?id=hd-bnt-1-hd&pass=&hash="},
        # Добавете повече канали тук, ако е нужно
    ]

    for channel in channels:
        print(f"Processing channel: {channel['name']}")
        fetched_link = update_links_with_selenium(channel['name'], channel['link'])
        if fetched_link:
            print(f"Fetched link for {channel['name']}: {fetched_link}")
        else:
            print(f"Failed to fetch link for {channel['name']}")

if __name__ == "__main__":
    main()
