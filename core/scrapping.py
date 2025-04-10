from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time

# Функция за инициализиране на драйвера с Chrome
def get_driver():
    options = Options()
    options.add_argument("--headless")  # Скрива браузъра, за да работи в бекграунд
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    return driver

# Примерна функция за извличане на линкове от сайт
def get_stream_link(url):
    driver = get_driver()
    driver.get(url)
    
    # Добавете логика за извличане на линк от страницата
    # Например, търсене на видео линк или m3u8 линк:
    time.sleep(5)  # Добавяне на изчакване за зареждане на съдържанието
    try:
        video_link = driver.find_element(By.XPATH, '//*[@id="video-player"]/@src').get_attribute("src")
    except Exception as e:
        print(f"Не успях да намеря видео линк: {e}")
        video_link = None
    
    driver.quit()
    return video_link

# Функция за запис в m3u файл
def write_to_m3u(channel_name, channel_link):
    with open("sources.m3u", "a") as file:
        file.write(f'#EXTINF:-1 tvg-name="{channel_name}" tvg-logo="https://www.glebul.com/images/tv-logo/{channel_name.lower()}-hd.png" group-title="ЕФИРНИ", {channel_name}\n')
        file.write(f'{channel_link}\n')

def main():
    # Примерен URL и канал
    url = "https://www.some-streaming-site.com/channel/bnt-1-hd"
    channel_name = "BNT 1 HD"
    
    # Извличане на видео линк
    video_link = get_stream_link(url)
    
    if video_link:
        # Записване на линка в sources.m3u
        write_to_m3u(channel_name, video_link)
        print(f'Записан линк за {channel_name} в sources.m3u')
    else:
        print(f'Не беше намерен линк за {channel_name}')

if __name__ == "__main__":
    main()
