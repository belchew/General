import os
import requests
import git
# Път до твоето репозиторио, това ще бъде автоматично във всяка стъпка на GitHub Actions
repo_path = os.getcwd()  # Това ще даде директорията на текущото репозиторио в GitHub Actions

# URL на файла, който искаш да клонираш
file_url = 'https://raw.githubusercontent.com/rosendonchev/linkove/refs/heads/main/video_stream.m3u'  # Замени с твоя URL

# Локален път, където ще запишеш файла
local_filename = 'basic.m3u'  # Промененото име на файла
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
        
def edit_file_in_destination():
    dest_path = os.path.join(repo_path, file_to_copy)
    try:
        with open(dest_path, 'r+', encoding='utf-8') as file: 
            content = file.read()
            # Заменяме
            content = content.replace('#EXTM3U', '#EXTM3U catchup="flussonic" url-tvg="https://github.com/harrygg/EPG/raw/refs/heads/master/all-2days.details.epg.xml.gz"\n')
            content = content.replace('#EXTINF:-1,BNT1', '#EXTINF:-1 tvg-name="БНТ 1" tvg-logo="https://www.glebul.com/images/tv-logo/bnt-1-hd.png" group-title="ЕФИРНИ" , BNT 1 HD')
            content = content.replace('#EXTINF:-1,BNT2', '#EXTINF:-1 tvg-name="БНТ 2" tvg-logo="https://www.glebul.com/images/tv-logo/bnt-2.png" group-title="ЕФИРНИ" , BNT 2')
            content = content.replace('#EXTINF:-1,BNT3', '#EXTINF:-1 tvg-name="БНТ 3" tvg-logo="https://www.glebul.com/images/tv-logo/bnt-3-hd.png" group-title="ЕФИРНИ" , BNT 3')
            content = content.replace('#EXTINF:-1,BNT4', '#EXTINF:-1 tvg-name="БНТ 4" tvg-logo="https://www.glebul.com/images/tv-logo/bnt-4.png" group-title="ЕФИРНИ" , BNT 4 HD')
            content = content.replace('#EXTINF:-1,bTVAction', '#EXTINF:-1 tvg-name="bTV Action" tvg-logo="https://www.glebul.com/images/tv-logo/btv-action-hd.png" group-title="Спортни"  , bTV Action HD')
            content = content.replace('#EXTINF:-1,bTVCinema', '#EXTINF:-1 tvg-name="bTV Cinema" tvg-logo="https://www.glebul.com/images/tv-logo/btv-cinema.png" group-title="Филмови" , bTV Cinema HD')
            content = content.replace('#EXTINF:-1,bTVComedy', '#EXTINF:-1 tvg-name="bTV Comedy" tvg-logo="https://www.glebul.com/images/tv-logo/btv-comedy.png" group-title="Филмови" , bTV Comedy HD')
            content = content.replace('#EXTINF:-1,bTVStory', '#EXTINF:-1 tvg-name="bTV Story" tvg-logo="https://www.glebul.com/images/tv-logo/btv-story.png" group-title="Филмови" , bTV Story HD')
            content = content.replace('#EXTINF:-1,bTV', '#EXTINF:-1 tvg-name="bTV" tvg-logo="https://www.glebul.com/images/tv-logo/btv-hd.png" group-title="ЕФИРНИ" , bTV HD')
            content = content.replace('#EXTINF:-1,KinoNova', '#EXTINF:-1 tvg-name="KinoNova" tvg-logo="https://www.glebul.com/images/tv-logo/kino-nova.png" group-title="Филмови" , KinoNova')
            content = content.replace('#EXTINF:-1,DiemaFamily', '#EXTINF:-1 tvg-name="Diema Family" tvg-logo="https://www.glebul.com/images/tv-logo/diema-family.png" group-title="Филмови" , Diema Family')
            content = content.replace('#EXTINF:-1,STARChannel', '#EXTINF:-1 tvg-name="STAR CHANNEL" tvg-logo="https://www.glebul.com/images/tv-logo/star-channel-hd.png" group-title="Филмови" , STAR CHANNEL HD')
            content = content.replace('#EXTINF:-1,STARLife', '#EXTINF:-1 tvg-name="STAR Life" tvg-logo="https://www.glebul.com/images/tv-logo/star-life-hd.png" group-title="Филмови" , STAR Life HD')
            content = content.replace('#EXTINF:-1,STARCrime', '#EXTINF:-1 tvg-name="STAR Crime " tvg-logo="https://www.glebul.com/images/tv-logo/star-crime-hd.png" group-title="Филмови" , STAR Crime HD')
            content = content.replace('#EXTINF:-1,FilmBoxStars', '#EXTINF:-1 tvg-id="FilmboxStars.bg" tvg-name="FilmBox Stars HD" tvg-logo="http://iphd.tv/service/bulsat/filmbox_stars-18-02-2021.svg" group-title="Филмови" , FilmBox Stars HD')
            content = content.replace('#EXTINF:-1,FilmBoXtraHD', '#EXTINF:-1 tvg-id="FilmBoxExtra.bg" tvg-name="FilmBox Extra HD" tvg-logo="http://iphd.tv/service/bulsat/filmbox_extra-16-02-2021.svg" group-title="Филмови" , FilmBox Extra HD')
            content = content.replace('#EXTINF:-1,MovieStar', '#EXTINF:-1 tvg-id="MovieStar.bg" tvg-name="BG:Moviestar HD" tvg-logo="http://iphd.tv/service/bulsat/moviestar-23-04-2019.svg" group-title="Филмови" , Moviestar HD')
            content = content.replace('#EXTINF:-1,AMC', '#EXTINF:-1 tvg-id="AMC" tvg-name="AMC" tvg-logo="http://iphd.tv/service/bulsat/amc-17-02-2022.svg" group-title="Филмови" , AMC')
            content = content.replace('#EXTINF:-1,AXN', '#EXTINF:-1 tvg-id="AXN" tvg-name="AXN" tvg-logo="https://www.glebul.com/images/tv-logo/axn.png" group-title="Филмови" , AXN')
            content = content.replace('#EXTINF:-1,24kitchen', '#EXTINF:-1 tvg-name="24 Kitchen" tvg-logo="https://www.glebul.com/images/tv-logo/24-kitchen-hd.png" group-title="Други" , 24 Kitchen HD')
            content = content.replace('#EXTINF:-1,Discovery', '#EXTINF:-1 tvg-name="Discovery Channel" tvg-logo="https://www.glebul.com/images/tv-logo/discovery-channel-hd.png" group-title="Научни" , Discovery Channel HD')
            content = content.replace('#EXTINF:-1,NatGeoWild', '#EXTINF:-1 tvg-name="Nat Geo Wild" tvg-logo="https://www.glebul.com/images/tv-logo/nat-geo-wild-hd.png" group-title="Научни" , Nat Geo Wild HD')
            content = content.replace('#EXTINF:-1,History', '#EXTINF:-1 tvg-id="HistoryChannel.bg" tvg-name="History Channel HD" tvg-logo="http://iphd.tv/service/bulsat/history_channel-23-04-2019.svg" group-title="Научни" , History Channel HD')
            content = content.replace('#EXTINF:-1,Docubox', '#EXTINF:-1 tvg-id="DocuBox" tvg-name="Docu Box HD" tvg-logo="http://iphd.tv/service/bulsat/docubox-16-02-2021.svg" group-title="Научни" , Docu Box HD')
            content = content.replace('#EXTINF:-1,ViasatExplorer', '#EXTINF:-1 tvg-id="ViasatExplorer.bg" tvg-name="Viasat Explore HD" tvg-logo="http://iphd.tv/service/bulsat/viasat_explore-17-02-2022.svg" group-title="Научни" , Viasat Explore HD')
            content = content.replace('#EXTINF:-1,ViasatHistory', '#EXTINF:-1 tvg-id="ViasatHistory.bg" tvg-name="Viasat History HD" tvg-logo="http://iphd.tv/service/bulsat/viasat_history-17-02-2022.svg" group-title="Научни" , Viasat History HD')
            content = content.replace('#EXTINF:-1,ViasatNature', '#EXTINF:-1 tvg-id="ViasatNature.bg" tvg-name="Viasat Nature HD" tvg-logo="http://iphd.tv/service/bulsat/viasat_nature-17-02-2022.svg" group-title="Научни" , Viasat Nature HD')
            content = content.replace('#EXTINF:-1,AnimalPlanet', '#EXTINF:-1 tvg-id="AnimalPlanet.bg" tvg-name="Animal Planet HD" tvg-logo="http://iphd.tv/service/bulsat/animal_planet-23-04-2019.svg" group-title="Научни" , Animal Planet HD')
            content = content.replace('#EXTINF:-1,TLC', '#EXTINF:-1 tvg-name="TLC" tvg-logo="https://www.glebul.com/images/tv-logo/tlc.png" group-title="Други" , TLC HD')
            content = content.replace('#EXTINF:-1,Balkanika', '#EXTINF:-1 tvg-id="Balkanika.bg" tvg-name="Balkanika HD" tvg-logo="http://iphd.tv/service/bulsat/balkanika-23-04-2019.svg" group-title="Музикални" , Balkanika HD')
            content = content.replace('#EXTINF:-1,PlanetaFolk', '#EXTINF:-1 tvg-name="Planeta Folk" tvg-logo="https://www.glebul.com/images/tv-logo/planeta-folk.png" group-title="Музикални" , Planeta Folk')
            content = content.replace('#EXTINF:-1,DiemaSport2', '#EXTINF:-1 tvg-name="Diema Sport 2" tvg-logo="https://www.glebul.com/images/tv-logo/diema-sport-2-hd.png" group-title="Спортни" , Diema Sport 2')
            content = content.replace('#EXTINF:-1,DiemaSport3', '#EXTINF:-1 tvg-name="Diema Sport 3" tvg-logo="https://www.glebul.com/images/tv-logo/diema-sport-3-hd.png" group-title="Спортни" , Diema Sport 3')
            content = content.replace('#EXTINF:-1,MAXSport1', '#EXTINF:-1 tvg-name="Max Sport 1 HD" tvg-logo="https://www.glebul.com/images/tv-logo/max-sport-1-hd.png" group-title="Спортни" , Max Sport 1 HD')
            content = content.replace('#EXTINF:-1,MAXSport2', '#EXTINF:-1 tvg-name="Max Sport 2 HD" tvg-logo="https://www.glebul.com/images/tv-logo/max-sport-2-hd.png" group-title="Спортни" , Max Sport 2 HD')
            content = content.replace('#EXTINF:-1,MAXSport3', '#EXTINF:-1 tvg-name="Max Sport 3 HD" tvg-logo="https://www.glebul.com/images/tv-logo/max-sport-3-hd.png" group-title="Спортни" , Max Sport 3 HD')
            content = content.replace('#EXTINF:-1,MAXSport4', '#EXTINF:-1 tvg-name="Max Sport 4 HD" tvg-logo="https://www.glebul.com/images/tv-logo/max-sport-4-hd.png" group-title="Спортни" , Max Sport 4 HD')
            content = content.replace('#EXTINF:-1,NovaSport', '#EXTINF:-1 tvg-name="Nova Sport" tvg-logo="https://www.glebul.com/images/tv-logo/nova-sport-hd.png" group-title="Спортни" , Nova Sport HD')
            content = content.replace('#EXTINF:-1,RING', '#EXTINF:-1 tvg-name="Ring BG" tvg-logo="https://www.glebul.com/images/tv-logo/ring-bg-hd.png" group-title="Спортни" , Ring BG')
            content = content.replace('#EXTINF:-1,DiemaSport', '#EXTINF:-1 tvg-name="Diema Sport" tvg-logo="https://www.glebul.com/images/tv-logo/diema-sport-hd.png" group-title="Спортни" , Diema Sport')
            content = content.replace('#EXTINF:-1,Diema', '#EXTINF:-1 tvg-name="Diema" tvg-logo="https://www.glebul.com/images/tv-logo/diema.png" group-title="Филмови" , Diema')
            content = content.replace('#EXTINF:-1,Planeta', '#EXTINF:-1 tvg-name="Planeta" tvg-logo="https://www.glebul.com/images/tv-logo/planeta-hd.png" group-title="Музикални" , Planeta HD')
            content = content.replace('#EXTINF:-1,Nova', '#EXTINF:-1 tvg-name="Nova TV" tvg-logo="https://www.glebul.com/images/tv-logo/nova-tv-hd.png" group-title="ЕФИРНИ" , NovaTV')
            content = content.replace('#EXTINF:-1,CartoonNetwork', '#EXTINF:-1 tvg-name="Cartoon Network" tvg-logo="https://www.glebul.com/images/tv-logo/cartoon-network.png" group-title="Детски" , Cartoon Network HD')
            content = content.replace('#EXTINF:-1,Disney', '#EXTINF:-1 tvg-name="Disney channel" tvg-logo="https://www.glebul.com/images/tv-logo/disney-channel.png" group-title="Детски" , Disney channel')
            content = content.replace('#EXTINF:-1,Nickelodeon', '#EXTINF:-1 tvg-name="Nickelodeon" tvg-logo="https://www.glebul.com/images/tv-logo/nickelodeon.png" group-title="Детски" , Nickelodeon')
            content = content.replace('#EXTINF:-1,NickJr', '#EXTINF:-1 tvg-name="NickJr" tvg-logo="https://www.glebul.com/images/tv-logo/nick-jr.png" group-title="Детски" , Nick Jr') 
            content = content.replace('#EXTINF:-1,Nicktoons', '#EXTINF:-1 tvg-name="Nicktoons" tvg-logo="https://www.glebul.com/images/tv-logo/nicktoons.png" group-title="Детски" , Nicktoons') 
            content = content.replace('#EXTINF:-1,NatGeo', '#EXTINF:-1 tvg-name="National Geographic" tvg-logo="https://www.glebul.com/images/tv-logo/nat-geo-hd.png" group-title="Научни" , National Geographic HD')
            # Изтриваме последните 16 реда
            lines = content.splitlines()
            if len(lines) > 18:
                content = '\n'.join(lines[:-18])
            file.seek(0)
            file.truncate()
            file.write(content)
        print(f"File {file_to_copy} edited successfully in {repo_path}")
    except Exception as e:
        print(f"Error editing the file {file_to_copy} in {repo_path}: {e}")
        
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
    # Изтегли файла и го преименувай на basic.txt
    download_file(file_url, local_file_path)
    
    # Извърши комитване и качване на промените
    commit_and_push_changes()
