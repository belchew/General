from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

def get_chrome_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Без графичен интерфейс
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    # Автоматично инсталиране на правилната версия на ChromeDriver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    return driver

def fetch_m3u_links(url, output_file="sources.m3u"):
    driver = get_chrome_driver()
    driver.get(url)

    # Тук трябва да добавите логиката за извличане на линковете от страницата
    # Пример: Извличане на всички линкове от <a> тагове (можете да адаптирате за вашата структура)
    links = driver.find_elements_by_tag_name("a")
    
    # Записване на линковете в m3u файл
    with open(output_file, "w") as file:
        for link in links:
            href = link.get_attribute("href")
            if href:
                # Записване на линковете в .m3u формат
                file.write(f"{href}\n")
    
    driver.quit()
    print(f"Линковете са записани в {output_file}")

# Примерно използване на функцията
url = "https://www.seir-sanduk.com/?id=hd-bnt-1-hd&pass=&hash="  # Поставете URL-то на страницата от която искате да извлечете линкове
fetch_m3u_links(url)
