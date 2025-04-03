import os
import requests
import git

# Път до твоето репозиторио, това ще бъде автоматично във всяка стъпка на GitHub Actions
repo_path = os.getcwd()  

file_url = 'https://raw.githubusercontent.com/rosendonchev/skandalScraping/refs/heads/main/sources.m3u' 

# Локален път, където ще запишеш файла
local_filename = 'basic.m3u' 
local_file_path = os.path.join(repo_path, local_filename)

# Функция за изтегляне на файл от URL
def download_file(url, dest_path):
    response = requests.get(url)
    if response.status_code == 200:
        with open(dest_path, 'wb') as file:
            file.write(response.content)
        print(f"Файлът е изтеглен успешно и преименуван на {dest_path}")
    else:
        print(f"Грешка при изтегляне на файла: {response.status_code}")
        
# Функция за замяна на съдържание във файла
def replace_multiple_content(file_path, replacements):
    try:
        # Отваряме файла за четене
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()

        # Извършваме замените
        for old_content, new_content in replacements.items():
            content = content.replace(old_content, new_content)

        # Записваме обратно промененото съдържание
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(content)

        print(f"Съдържанието е успешно заменено в {file_path}.")
    
    except Exception as e:
        print(f"Грешка при замяна на съдържание във файла: {e}")

# Функция за изтриване на последните 18 реда от файла
def delete_last_n_lines(file_path, n=18):
    try:
        # Отваряме файла за четене
        with open(file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()

        # Премахваме последните n реда
        lines = lines[:-n]

        # Записваме обратно промененото съдържание в същия файл
        with open(file_path, 'w', encoding='utf-8') as file:
            file.writelines(lines)

        print(f"Последните {n} реда са изтрити успешно от файла {file_path}.")
    
    except Exception as e:
        print(f"Грешка при изтриване на последните {n} реда от файла: {e}")

# Функция за клониране на репозиторио и качване на промените
def commit_and_push_changes():
    # Отвори локалното репозиторио с gitpython
    repo = git.Repo(repo_path)
    
    # Добави новия файл
    repo.git.add(local_filename)
    
    # Извърши commit
    repo.git.commit('-m', 'Добавен нов файл basic.m3u от URL')
    
    # Изпрати промените към origin (можеш да промениш името на remote, ако е различно)
    repo.git.push('origin', 'main')
    print(f"Промените са качени успешно в репозиториото: {repo_path}")

if __name__ == "__main__":
    # Изтегли файла и го преименувай на basic.m3u
    download_file(file_url, local_file_path)
    
    # Изтриване на последните 18 реда от файла
    # delete_last_n_lines(local_file_path, 18)

        # Замяна на множество редове съдържание във файла
    replacements = {
        	"#EXTM3U": '#EXTM3U catchup="flussonic" url-tvg="https://github.com/harrygg/EPG/raw/refs/heads/master/all-2days.details.epg.xml.gz"\n',
            "#EXTINF:-1,BNT1": '#EXTINF:-1 tvg-name="БНТ 1" tvg-logo="https://www.glebul.com/images/tv-logo/bnt-1-hd.png" group-title="ЕФИРНИ" , BNT 1 HD',
            "#EXTINF:-1,BNT2": '#EXTINF:-1 tvg-name="БНТ 2" tvg-logo="https://www.glebul.com/images/tv-logo/bnt-2.png" group-title="ЕФИРНИ" , BNT 2',
            "#EXTINF:-1,BNT3": '#EXTINF:-1 tvg-name="БНТ 3" tvg-logo="https://www.glebul.com/images/tv-logo/bnt-3-hd.png" group-title="ЕФИРНИ" , BNT 3',
            "#EXTINF:-1,BNT4": '#EXTINF:-1 tvg-name="БНТ 4" tvg-logo="https://www.glebul.com/images/tv-logo/bnt-4.png" group-title="ЕФИРНИ" , BNT 4 HD',
            "#EXTINF:-1,bTVAction": '#EXTINF:-1 tvg-name="bTV Action" tvg-logo="https://www.glebul.com/images/tv-logo/btv-action-hd.png" group-title="Спортни"  , bTV Action HD',
            "#EXTINF:-1,bTVCinema": '#EXTINF:-1 tvg-name="bTV Cinema" tvg-logo="https://www.glebul.com/images/tv-logo/btv-cinema.png" group-title="Филмови" , bTV Cinema HD',
            "#EXTINF:-1,bTVComedy": '#EXTINF:-1 tvg-name="bTV Comedy" tvg-logo="https://www.glebul.com/images/tv-logo/btv-comedy.png" group-title="Филмови" , bTV Comedy HD',
            "#EXTINF:-1,bTVStory": '#EXTINF:-1 tvg-name="bTV Story" tvg-logo="https://www.glebul.com/images/tv-logo/btv-story.png" group-title="Филмови" , bTV Story HD',
            "#EXTINF:-1,bTV": '#EXTINF:-1 tvg-name="bTV" tvg-logo="https://www.glebul.com/images/tv-logo/btv-hd.png" group-title="ЕФИРНИ" , bTV HD',
            "#EXTINF:-1,KinoNova": '#EXTINF:-1 tvg-name="KinoNova" tvg-logo="https://www.glebul.com/images/tv-logo/kino-nova.png" group-title="Филмови" , KinoNova',
            "#EXTINF:-1,DiemaFamily": '#EXTINF:-1 tvg-name="Diema Family" tvg-logo="https://www.glebul.com/images/tv-logo/diema-family.png" group-title="Филмови" , Diema Family',
            "#EXTINF:-1,STARChannel": '#EXTINF:-1 tvg-name="STAR CHANNEL" tvg-logo="https://www.glebul.com/images/tv-logo/star-channel-hd.png" group-title="Филмови" , STAR CHANNEL HD',
            "#EXTINF:-1,STARLife": '#EXTINF:-1 tvg-name="STAR Life" tvg-logo="https://www.glebul.com/images/tv-logo/star-life-hd.png" group-title="Филмови" , STAR Life HD',
            "#EXTINF:-1,STARCrime": '#EXTINF:-1 tvg-name="STAR Crime " tvg-logo="https://www.glebul.com/images/tv-logo/star-crime-hd.png" group-title="Филмови" , STAR Crime HD',
            "#EXTINF:-1,FilmBoxStars": '#EXTINF:-1 tvg-id="FilmBox Stars" tvg-name="FilmBox Stars" tvg-logo="https://www.bg-gledai.video/wp-content/uploads/filmboxplus.png" group-title="Филмови" , FilmBox Stars',
            "#EXTINF:-1,FilmBoXtraHD": '#EXTINF:-1 tvg-id="FilmBox Extra" tvg-name="FilmBox Extra" tvg-logo="https://www.bg-gledai.video/wp-content/uploads/filmboxextra.png" group-title="Филмови" , FilmBox Extra',
            "#EXTINF:-1,MovieStar": '#EXTINF:-1 tvg-id="MovieStar.bg" tvg-name="Moviestar HD" tvg-logo="https://www.bg-gledai.video/wp-content/uploads/moviestar.png" group-title="Филмови" , Moviestar HD',
            "#EXTINF:-1,AMC": '#EXTINF:-1 tvg-id="amc.bg" tvg-name="AMC" tvg-logo="https://www.bg-gledai.video/wp-content/uploads/amc.png" group-title="Филмови" , AMC',
            "#EXTINF:-1,AXN": '#EXTINF:-1 tvg-id="AXN" tvg-name="AXN" tvg-logo="https://www.glebul.com/images/tv-logo/axn.png" group-title="Филмови" , AXN',
            "#EXTINF:-1,24kitchen": '#EXTINF:-1 tvg-name="24 Kitchen" tvg-logo="https://www.glebul.com/images/tv-logo/24-kitchen-hd.png" group-title="Други" , 24 Kitchen HD',
            "#EXTINF:-1,Discovery": '#EXTINF:-1 tvg-name="Discovery Channel" tvg-logo="https://www.glebul.com/images/tv-logo/discovery-channel-hd.png" group-title="Научни" , Discovery Channel HD',
            "#EXTINF:-1,NatGeoWild": '#EXTINF:-1 tvg-name="NatGeo Wild" tvg-logo="https://www.glebul.com/images/tv-logo/nat-geo-wild-hd.png" group-title="Научни" , Nat Geo Wild HD',
            "#EXTINF:-1,History": '#EXTINF:-1 tvg-id="HistoryChannel.bg" tvg-name="History Channel HD" tvg-logo="https://www.bg-gledai.video/wp-content/uploads/history-1.png" group-title="Научни" , History Channel HD',
            "#EXTINF:-1,Docubox": '#EXTINF:-1 tvg-id="DocuBox" tvg-name="DocuBox" tvg-logo="https://www.bg-gledai.video/wp-content/uploads/docubox.png" group-title="Научни" , Docu Box HD',
            "#EXTINF:-1,ViasatExplorer": '#EXTINF:-1 tvg-id="ViasatExplorer.bg" tvg-name="Viasat Explore HD" tvg-logo="https://www.bg-gledai.video/wp-content/uploads/viasat_explore.png" group-title="Научни" , Viasat Explore HD',
            "#EXTINF:-1,ViasatHistory": '#EXTINF:-1 tvg-id="ViasatHistory.bg" tvg-name="Viasat History HD" tvg-logo="https://www.bg-gledai.video/wp-content/uploads/viasat_history.png" group-title="Научни" , Viasat History HD',
            "#EXTINF:-1,ViasatNature": '#EXTINF:-1 tvg-id="ViasatNature.bg" tvg-name="Viasat Nature HD" tvg-logo="https://www.bg-gledai.video/wp-content/uploads/viasat_nature.png" group-title="Научни" , Viasat Nature HD',
            "#EXTINF:-1,AnimalPlanet": '#EXTINF:-1 tvg-id="AnimalPlanet.bg" tvg-name="Animal Planet HD" tvg-logo="https://www.glebul.com/images/tv-logo/animal-planet.png" group-title="Научни" , Animal Planet HD',
            "#EXTINF:-1,TLC": '#EXTINF:-1 tvg-name="TLC" tvg-logo="https://www.glebul.com/images/tv-logo/tlc.png" group-title="Други" , TLC HD',
            "#EXTINF:-1,Balkanika": '#EXTINF:-1 tvg-id="Balkanika.bg" tvg-name="Balkanika HD" tvg-logo="https://www.glebul.com/images/tv-logo/balkanika-hd.png" group-title="Музикални" , Balkanika HD',
            "#EXTINF:-1,PlanetaFolk": '#EXTINF:-1 tvg-name="Planeta Folk" tvg-logo="https://www.glebul.com/images/tv-logo/planeta-folk.png" group-title="Музикални" , Planeta Folk',
            "#EXTINF:-1,DiemaSport2": '#EXTINF:-1 tvg-name="Diema Sport 2" tvg-logo="https://www.glebul.com/images/tv-logo/diema-sport-2-hd.png" group-title="Спортни" , Diema Sport 2',
            "#EXTINF:-1,DiemaSport3": '#EXTINF:-1 tvg-name="Diema Sport 3" tvg-logo="https://www.glebul.com/images/tv-logo/diema-sport-3-hd.png" group-title="Спортни" , Diema Sport 3',
            "#EXTINF:-1,MAXSport1": '#EXTINF:-1 tvg-name="Max Sport 1 HD" tvg-logo="https://www.glebul.com/images/tv-logo/max-sport-1-hd.png" group-title="Спортни" , Max Sport 1 HD',
            "#EXTINF:-1,MAXSport2": '#EXTINF:-1 tvg-name="Max Sport 2 HD" tvg-logo="https://www.glebul.com/images/tv-logo/max-sport-2-hd.png" group-title="Спортни" , Max Sport 2 HD',
            "#EXTINF:-1,MAXSport3": '#EXTINF:-1 tvg-name="Max Sport 3 HD" tvg-logo="https://www.glebul.com/images/tv-logo/max-sport-3-hd.png" group-title="Спортни" , Max Sport 3 HD',
            "#EXTINF:-1,MAXSport4": '#EXTINF:-1 tvg-name="Max Sport 4 HD" tvg-logo="https://www.glebul.com/images/tv-logo/max-sport-4-hd.png" group-title="Спортни" , Max Sport 4 HD',
            "#EXTINF:-1,NovaSport": '#EXTINF:-1 tvg-name="Nova Sport" tvg-logo="https://www.glebul.com/images/tv-logo/nova-sport-hd.png" group-title="Спортни" , Nova Sport HD',
            "#EXTINF:-1,RING": '#EXTINF:-1 tvg-name="Ring BG" tvg-logo="https://www.glebul.com/images/tv-logo/ring-bg-hd.png" group-title="Спортни" , Ring BG',
            "#EXTINF:-1,DiemaSport": '#EXTINF:-1 tvg-name="Diema Sport" tvg-logo="https://www.glebul.com/images/tv-logo/diema-sport-hd.png" group-title="Спортни" , Diema Sport',
            "#EXTINF:-1,Diema": '#EXTINF:-1 tvg-name="Diema" tvg-logo="https://www.glebul.com/images/tv-logo/diema.png" group-title="Филмови" , Diema',
            "#EXTINF:-1,Planeta": '#EXTINF:-1 tvg-name="Planeta" tvg-logo="https://www.glebul.com/images/tv-logo/planeta-hd.png" group-title="Музикални" , Planeta HD',
            "#EXTINF:-1,Nova": '#EXTINF:-1 tvg-name="Nova TV" tvg-logo="https://www.glebul.com/images/tv-logo/nova-tv-hd.png" group-title="ЕФИРНИ" , NovaTV',
            "#EXTINF:-1,CartoonNetwork": '#EXTINF:-1 tvg-name="Cartoon Network" tvg-logo="https://www.glebul.com/images/tv-logo/cartoon-network.png" group-title="Детски" , Cartoon Network HD',
            "#EXTINF:-1,Disney": '#EXTINF:-1 tvg-name="Disney channel" tvg-logo="https://www.glebul.com/images/tv-logo/disney-channel.png" group-title="Детски" , Disney channel',
            "#EXTINF:-1,Nickelodeon": '#EXTINF:-1 tvg-name="Nickeldeon" tvg-logo="https://www.glebul.com/images/tv-logo/nickelodeon.png" group-title="Детски" , Nickelodeon',
            "#EXTINF:-1,NickJr": '#EXTINF:-1 tvg-name="Nick Jr." tvg-logo="https://www.glebul.com/images/tv-logo/nick-jr.png" group-title="Детски" , Nick Jr',
            "#EXTINF:-1,Nicktoons": '#EXTINF:-1 tvg-name="Nicktoons" tvg-logo="https://www.glebul.com/images/tv-logo/nicktoons.png" group-title="Детски" , Nicktoons',
            "#EXTINF:-1,NatGeo": '#EXTINF:-1 tvg-name="National Geographic" tvg-logo="https://www.glebul.com/images/tv-logo/nat-geo-hd.png" group-title="Научни" National Geographic HD',
            "#EXTINF:-1,Eurosport1": '#EXTINF:-1 tvg-name="Eurosport" tvg-logo="https://www.glebul.com/images/tv-logo/eurosport-1-hd.png" group-title="Спортни" , Eurosport HD',
            "#EXTINF:-1,Eurosport2": '#EXTINF:-1 tvg-name="Eurosport 2" tvg-logo="https://www.glebul.com/images/tv-logo/eurosport-2-hd.png" group-title="Спортни" , Eurosport 2 HD',
            "#EXTINF:-1,The Voice": '#EXTINF:-1 tvg-name="The Voice" tvg-logo="https://www.glebul.com/images/tv-logo/the-voice.png" group-title="Музикални" , The Voice',
            "#EXTINF:-1,City": '#EXTINF:-1 tvg-name="City TV" tvg-logo="https://www.glebul.com/images/tv-logo/city-tv.png" group-title="Музикални" , City TV',
            "#EXTINF:-1,Travel": '#EXTINF:-1 tvg-name="Travel" tvg-logo="https://www.glebul.com/images/tv-logo/travel-tv.png" group-title="Други" , Travel TV',
            "#EXTINF:-1,Magic": '#EXTINF:-1 tvg-name="Magic" tvg-logo="https://www.bg-gledai.video/wp-content/uploads/fantv.png" group-title="Музикални" , Magic TV',
            "#EXTINF:-1,BulgariaOnAir": '#EXTINF:-1 tvg-name="bgonair.bg" tvg-logo="https://www.glebul.com/images/tv-logo/bulgaria-on-air.png" group-title="ЕФИРНИ" , Bulgaria ON Air HD.bg',
            "#EXTINF:-1,CodeFashion": '#EXTINF:-1 tvg-name="CodeFashion HD" tvg-logo="https://www.glebul.com/images/tv-logo/code-fashion-tv-hd.png" group-title="Други" , CodeFashion HD',
            "#EXTINF:-1,DSTV": '#EXTINF:-1 tvg-name="DSTV" tvg-logo="https://www.glebul.com/images/tv-logo/dstv.png" group-title="Музикални" , DSTV',
            "#EXTINF:-1,EKids": '#EXTINF:-1 tvg-name="EKids" tvg-logo="https://www.glebul.com/images/tv-logo/e-kids.png" group-title="Детски" , EKids',
            "#EXTINF:-1,EpicDrama": '#EXTINF:-1 tvg-name="Epic Drama" tvg-logo="https://www.glebul.com/images/tv-logo/epic-drama-hd.png" group-title="Филмови" , Epic Drama HD',
            "#EXTINF:-1,Eurocom": '#EXTINF:-1 tvg-name="Evrokom" tvg-logo="https://www.glebul.com/images/tv-logo/evrokom.png" group-title="ЕФИРНИ" , Evrokom',
            "#EXTINF:-1,FolklorTV": '#EXTINF:-1 tvg-name="folklor-tv" tvg-logo="https://www.glebul.com/images/tv-logo/folklor-tv.png" group-title="Музикални" , Folklor TV HD',
            "#EXTINF:-1,FoodNetwork": '#EXTINF:-1 tvg-name="Food Network" tvg-logo="https://www.glebul.com/images/tv-logo/food-network-hd.png" group-title="Други" , Food Network HD',
            "#EXTINF:-1,ID": '#EXTINF:-1 tvg-name="id extra HD" tvg-logo="https://www.glebul.com/images/tv-logo/id-xtra-hd.png" group-title="Филмови" , ID Extra HD',
            "#EXTINF:-1,TravelChannel": '#EXTINF:-1 tvg-name="Travel Channel" tvg-logo="https://www.glebul.com/images/tv-logo/travel-channel-hd.png" group-title="Научни" , Travel Channel',
            "#EXTINF:-1,TLC": '#EXTINF:-1 tvg-name="TLC" tvg-logo="https://www.glebul.com/images/tv-logo/tlc.png" group-title="Други" , TLC HD',
            "#EXTINF:-1,EuroNews": '#EXTINF:-1 tvg-name="Euronews Bulgaria" tvg-logo="https://www.glebul.com/images/tv-logo/euronews-bulgaria.png" group-title="ЕФИРНИ" , Euronews Bulgaria',
            "https://cdn1.glebul.com/hls/": 'https://ro.glebul.com/dvr/',
            "https://cdn2.glebul.com/hls/": 'https://ro.glebul.com/dvr/',
            "https://cdn3.glebul.com/hls/": 'https://ro.glebul.com/dvr/',
            "https://cdn4.glebul.com/hls/": 'https://ro.glebul.com/dvr/',
            "https://cdn5.glebul.com/hls/": 'https://ro.glebul.com/dvr/',
            "https://cdn6.glebul.com/hls/": 'https://ro.glebul.com/dvr/',
            "https://cdn7.glebul.com/hls/": 'https://ro.glebul.com/dvr/',
            "https://cdn8.glebul.com/hls/": 'https://ro.glebul.com/dvr/',
            "https://cdn9.glebul.com/hls/": 'https://ro.glebul.com/dvr/',
            "https://cdn10.glebul.com/hls/": 'https://ro.glebul.com/dvr/',
            "https://cdn11.glebul.com/hls/": 'https://ro.glebul.com/dvr/',
            "https://cdn12.glebul.com/hls/": 'https://ro.glebul.com/dvr/'
    }
    replace_multiple_content(local_file_path, replacements)
    # Извърши комитване и качване на промените
    commit_and_push_changes()
