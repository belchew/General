import os
import time
import git
from playwright.sync_api import sync_playwright

# Mapping of URL IDs to specific channel names required for the EPG
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
    "diema-family-online": "DiemaFamily",
    "diema-sport-hd-online": "DiemaSport",
    "diema-sport-2-hd-online": "DiemaSport2",
    "diema-sport-3-hd-online": "DiemaSport3",
    "diema-online": "Diema",
    "disney-channel-online": "Disney",
    "discovery-channel-hd-online": "Discovery",
    "dstv-online": "DSTV",
    "e-kids-online": "EKids",
    "epic-drama-hd-online": "EpicDrama",
    "eurosport-1-hd-online": "Eurosport1",
    "eurosport-2-hd-online": "Eurosport2",
    "euronews-bulgaria-online": "EuroNews",
    "evrokom-online": "Eurocom",
    "folklor-tv-online": "FolklorTV",
    "food-network-hd-online": "FoodNetwork",
    "star-crime-hd-online": "STARCrime",
    "star-channel-hd-online": "STARChannel",
    "star-life-hd-online": "STARLife",
    "id-xtra-hd-online": "ID",
    "kanal-3-online": "Kanal3",
    "kino-nova-online": "KinoNova",
    "max-sport-1-hd-online": "MAXSport1",
    "max-sport-2-hd-online": "MAXSport2",
    "max-sport-3-hd-online": "MAXSport3",
    "max-sport-4-hd-online": "MAXSport4",
    "nat-geo-hd-online": "NatGeo",
    "nat-geo-wild-hd-online": "NatGeoWild",
    "nick-jr-online": "NickJr",
    "nickelodeon-online": "Nickelodeon",
    "nicktoons-online": "Nicktoons",
    "nova-news-hd-online": "NovaNews",
    "nova-sport-hd-online": "NovaSport",
    "planeta-folk-online": "PlanetaFolk",
    "planeta-hd-online": "Planeta",
    "ring-bg-hd-online": "RING",
    "rodina-tv-online": "Rodina",
    "78-tv-hd-online": "78TV",
    "skat-online": "Skat",
    "the-voice-online": "TheVoice",
    "tiankov-tv-online": "TiankovFolk",
    "tlc-online": "TLC",
    "travel-channel-hd-online": "TravelChannel",
    "travel-tv-online": "Travel",
    "tv-1-online": "TV1",
    "vtk-online": "VTK",
    "24-kitchen-hd-online": "24kitchen",
    "alfa-tv-online": "Alfa",
    "axn-online": "AXN",
    "axn-black-online": "AXNBlack",
    "axn-white-online": "AXNWhite",
    "bloomberg-tv-online": "Bloomberg",
    # Add more mappings as needed
}

# Set to store recorded channels and avoid duplicates
recorded_channels = set()

def scrape_and_push_to_git():
    # Clear the sources.m3u file before writing new data
    with open('sources.m3u', 'w', encoding='utf-8') as f:
        f.write('#EXTM3U\n')
    
    recorded_channels.clear()

    # Using Playwright to scrape
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        # Replace this URL with the URL of the page containing the links you want to scrape
        url = 'https://www.seir-sanduk.com/hd-bnt-1-hd-online'
        page.goto(url)

        # Extract all links from the page
        links = page.evaluate("""
            () => {
                return Array.from(document.querySelectorAll('a')).map(link => link.href);
            }
        """)

        for link in links:
            try:
                page.goto(link)

                player_source = page.evaluate("""
                    () => {
                        const scriptTags = document.querySelectorAll('script');
                        let source = null;
                        
                        scriptTags.forEach(script => {
                            const scriptContent = script.innerHTML;
                            if (scriptContent.includes('Element")')) {
                                const match = scriptContent.match(/file:\\s*"([^"]+)"/);
                                if (match) {
                                    source = match[1];
                                }
                            } else if (scriptContent.includes('const streamUrl =')) {
                                const match = scriptContent.match(/const streamUrl =\\s*"([^"]+)"/);
                                if (match) {
                                    source = match[1];
                                }  
                            }
                        });

                        return source;
                    }
                """)

                if player_source and player_source != "https://www.seir-sanduk.com/otustanausta1.mp4":
                    # Extract the channel name from the URL (if it's part of the URL)
                    channel_id = link.split('online/')[1].split(' ')[0] if 'online/' in link else 'Unknown Channel'

                    # Check the mapping for the correct channel name
                    channel_name = channel_name_mapping.get(channel_id, channel_id)

                    # Skip "Unknown Channel" and duplicates
                    if channel_name != 'Unknown Channel' and channel_name not in recorded_channels:
                        with open('sources.m3u', 'a', encoding='utf-8') as f:
                            f.write(f'#EXTINF:-1,{channel_name}\n{player_source}\n')

                        print(f'Data successfully written for {channel_name}')
                        recorded_channels.add(channel_name)  # Add to the set of recorded channels
                    else:
                        print(f'Skipped duplicate or unknown channel: {channel_name}')
                else:
                    print(f'No player source found for {link}')

            except Exception as error:
                print(f'Error visiting {link}: {error}')

        # Close the browser instance
        browser.close()

    # Commit and push changes to GitHub
    repo = git.Repo(search_parent_directories=True)
    repo.git.add('sources.m3u')
    repo.index.commit('Update sources.m3u with new player sources')
    origin = repo.remote(name='origin')
    origin.push()

# Run the function to scrape and push to Git
if __name__ == "__main__":
    scrape_and_push_to_git()
