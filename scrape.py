import os
import git
import re
from playwright.sync_api import sync_playwright

# Mapping на ID-та към имена на канали
channel_name_mapping = {
    "bnt-1-hd-online": "BNT1",
    "bnt-2-online": "BNT2",
    "bnt-3-hd-online": "BNT3",
    "bnt-4-online": "BNT4",
    "nova-tv-hd-online": "Nova",
    "btv-hd-online": "bTV",
    "btv-action-hd-online": "bTVAction",
    "btv-cinema-online": "bTVCinema",
    "btv-comedy-online": "bTVComedy",
    "btv-story-online": "bTVStory",
    "bulgaria-on-air-online": "BulgariaOnAir",
    "cartoon-network-online": "CartoonNetwork",
    "city-tv-online": "City",
    "code-fashion-tv-hd-online": "CodeFashion",
    # Добави още канали тук
}

# Set за записаните канали, за да избегнем дублиране
recorded_channels = set()

def scrape_and_push_to_git():
    # Почистване на sources.m3u файла
    if os.path.exists('sources.m3u'):
        os.remove('sources.m3u')
    with open('sources.m3u', 'w', encoding='utf-8') as f:
        f.write("#EXTM3U\n")

    # Стартиране на браузъра с Playwright
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)  # headless=True за скрит браузър
        page = browser.new_page()

        # Замени URL с този, от който искаш да извлечеш линковете
        url = 'https://seirsanduk.online/bnt-1-hd-online'
        page.goto(url)

        # Извличане на всички линкове от страницата
        links = page.locator('a').all_hrefs()

        for link in links:
            try:
                page.goto(link)

                # Извличане на източника на видеото
                player_source = None
                scripts = page.locator('script').all_text_contents()
                for script_content in scripts:
                    if 'file' in script_content:
                        match = re.search(r'file:\s*"([^"]+)"', script_content)
                        if match:
                            player_source = match.group(1)
                            break
                    elif 'const streamUrl =' in script_content:
                        match = re.search(r'const streamUrl =\s*"([^"]+)"', script_content)
                        if match:
                            player_source = match.group(1)
                            break

                # Проверка дали източник е намерен
                if player_source and player_source != "https://www.seir-sanduk.com/otustanausta1.mp4":
                    channel_id = link.split('online/')[1].split(' ')[0] if 'online/' in link else 'Unknown Channel'
                    channel_name = channel_name_mapping.get(channel_id, channel_id)

                    if channel_name != 'Unknown Channel' and channel_name not in recorded_channels:
                        with open('sources.m3u', 'a', encoding='utf-8') as f:
                            f.write(f"#EXTINF:-1,{channel_name}\n{player_source}\n")
                        recorded_channels.add(channel_name)
                        print(f"Data successfully written for {channel_name}")
                    else:
                        print(f"Skipped duplicate or unknown channel: {channel_name}")

            except Exception as e:
                print(f"Error visiting {link}: {e}")

        browser.close()

    # Git добавяне, commit и push
    try:
        repo = git.Repo(search_parent_directories=True)
        repo.git.add('sources.m3u')
        repo.git.commit('-m', 'Update sources.m3u with new player sources')
        repo.git.push()
        print("Changes successfully pushed to GitHub repository")
    except Exception as e:
        print(f"Error with Git operations: {e}")

if __name__ == "__main__":
    scrape_and_push_to_git()
