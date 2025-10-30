
import os
import base64
import re
import pandas as pd
import requests
import subprocess
#from datetime import datetime

# Име на файла
#file_path = 'result.txt'

# Вземаме днешната дата
#today = datetime.now()
#month = today.strftime("%m")
#day = today.strftime("%d")
#date_suffix = f"{month}{month}{day}{day}{month}{day}{month}"

# Създаваме желания ред
#password = f"pass=11kalAdKaAde11sF{date_suffix}"

# Записваме във файла
#with open(file_path, 'w', encoding='utf-8') as file:
#    file.write(final_line)

#print("Файлът е променен.")

#with open('result.txt', 'r') as f:
#    password = f.read().strip()

# Channel mapping
channel_mapping = {
            '#EXTINF:-1 tvg-name="БНТ 1" tvg-logo="https://www.glebul.com/images/tv-logo/bnt-1-hd.png" group-title="ЕФИРНИ" , BNT 1 HD': 'https://www.seir-sanduk.com/hd-bnt-1-hd?player=13&id=hd-bnt-1-hd&pass=',
            '#EXTINF:-1 tvg-name="bTV" tvg-logo="https://www.glebul.com/images/tv-logo/btv-hd.png" group-title="ЕФИРНИ" , bTV HD': 'https://www.seir-sanduk.com/hd-btv-hd?player=13&id=hd-btv-hd&pass=',
            '#EXTINF:-1 tvg-name="Nova TV" tvg-logo="https://www.glebul.com/images/tv-logo/nova-tv-hd.png" group-title="ЕФИРНИ" , NovaTV': 'https://www.seir-sanduk.com/hd-nova-tv-hd?player=13&id=hd-bnt-1-hd&pass=',
            '#EXTINF:-1 tvg-name="БНТ 2" tvg-logo="https://www.glebul.com/images/tv-logo/bnt-2.png" group-title="ЕФИРНИ" , BNT 2': 'https://www.seir-sanduk.com/bnt-2?player=13&id=bnt-2&pass=',
            '#EXTINF:-1 tvg-name="БНТ 3" tvg-logo="https://www.glebul.com/images/tv-logo/bnt-3-hd.png" group-title="ЕФИРНИ" , BNT 3': 'https://www.seir-sanduk.com/hd-bnt-3-hd?player=13&id=hd-bnt-3-hd&pass=',
            '#EXTINF:-1 tvg-name="БНТ 4" tvg-logo="https://www.glebul.com/images/tv-logo/bnt-4.png" group-title="ЕФИРНИ" , BNT 4 HD': 'https://www.seir-sanduk.com/bnt-4?player=13&id=bnt-4&pass=',
            '#EXTINF:-1 tvg-name="TV1" tvg-logo="https://www.glebul.com/images/tv-logo/tv-1.png" group-title="ЕФИРНИ" , TV1': 'https://www.seir-sanduk.com/tv-1?player=13&id=tv-1&pass=',
            '#EXTINF:-1 tvg-name="Канал 3" tvg-logo="https://www.glebul.com/images/tv-logo/kanal-3.png" group-title="ЕФИРНИ" , Kanal3': 'https://www.seir-sanduk.com/kanal-3?player=13&id=kanal-3&pass=',
            '#EXTINF:-1 tvg-name="Evrokom" tvg-logo="https://www.glebul.com/images/tv-logo/evrokom.png" group-title="ЕФИРНИ" , Evrokom': 'https://www.seir-sanduk.com/evrokom?player=13&id=evrokom&pass=',
            '#EXTINF:-1 tvg-name="Skat" tvg-logo="https://www.glebul.com/images/tv-logo/skat.png" group-title="ЕФИРНИ" , Skat': 'https://www.seir-sanduk.com/skat?player=13&id=skat&pass=',
            '#EXTINF:-1 tvg-name="bgonair.bg" tvg-logo="https://www.glebul.com/images/tv-logo/bulgaria-on-air.png" group-title="ЕФИРНИ" , Bulgaria ON Air': 'https://www.seir-sanduk.com/bulgaria-on-air?player=13&id=bulgaria-on-air&pass=',
            '#EXTINF:-1 tvg-name="Bloomberg" tvg-logo="https://www.glebul.com/images/tv-logo/bloomberg-tv.png" group-title="ЕФИРНИ" , Bloomberg TV Bulgaria': 'https://www.seir-sanduk.com/bloomberg-tv?player=13&id=bloomberg-tv&pass=',
            '#EXTINF:-1 tvg-name="Euronews Bulgaria" tvg-logo="https://www.glebul.com/images/tv-logo/euronews-bulgaria.png" group-title="ЕФИРНИ" , Euronews Bulgaria': 'https://www.seir-sanduk.com/euronews-bulgaria?player=13&id=euronews-bulgaria&pass=',
            '#EXTINF:-1 tvg-name="Diema" tvg-logo="https://www.glebul.com/images/tv-logo/diema.png" group-title="Филмови" , Diema': 'https://www.seir-sanduk.com/diema?player=13&id=diema&pass=',
            '#EXTINF:-1 tvg-name="bTV Action" tvg-logo="https://www.glebul.com/images/tv-logo/btv-action-hd.png" group-title="Спортни"  , bTV Action HD': 'https://www.seir-sanduk.com/hd-btv-action-hd?player=13&id=hd-btv-action-hd&pass=',
            '#EXTINF:-1 tvg-name="bTV Cinema" tvg-logo="https://www.glebul.com/images/tv-logo/btv-cinema.png" group-title="Филмови" , bTV Cinema HD': 'https://www.seir-sanduk.com/btv-cinema?player=13&id=btv-cinema&pass=',
            '#EXTINF:-1 tvg-name="bTV Comedy" tvg-logo="https://www.glebul.com/images/tv-logo/btv-comedy.png" group-title="Филмови" , bTV Comedy HD': 'https://www.seir-sanduk.com/btv-comedy?player=13&id=btv-comedy&pass=',
            '#EXTINF:-1 tvg-name="bTV Story" tvg-logo="https://www.glebul.com/images/tv-logo/btv-story.png" group-title="Филмови" , bTV Story HD': 'https://www.seir-sanduk.com/btv-story?player=13&id=btv-story&pass=',
            '#EXTINF:-1 tvg-name="KinoNova" tvg-logo="https://www.glebul.com/images/tv-logo/kino-nova.png" group-title="Филмови" , KinoNova': 'https://www.seir-sanduk.com/kino-nova?player=13&id=kino-nova&pass=',
            '#EXTINF:-1 tvg-name="id extra HD" tvg-logo="https://www.glebul.com/images/tv-logo/id-xtra-hd.png" group-title="Филмови" , ID Extra HD': 'https://www.seir-sanduk.com/hd-id-xtra-hd?player=13&id=hd-id-xtra-hd&pass=',
            '#EXTINF:-1 tvg-name="Diema Family" tvg-logo="https://www.glebul.com/images/tv-logo/diema-family.png" group-title="Филмови" , Diema Family': 'https://www.seir-sanduk.com/diema-family?player=13&id=diema-family&pass=',
            '#EXTINF:-1 tvg-name="STAR CHANNEL" tvg-logo="https://www.glebul.com/images/tv-logo/star-channel-hd.png" group-title="Филмови" , STAR CHANNEL HD': 'https://www.seir-sanduk.com/hd-star-channel-hd?player=13&id=hd-star-channel-hd&pass=',
            '#EXTINF:-1 tvg-name="STAR Life" tvg-logo="https://www.glebul.com/images/tv-logo/star-life-hd.png" group-title="Филмови" , STAR Life HD': 'https://www.seir-sanduk.com/hd-star-life-hd?player=13&id=hd-star-life-hd&pass=',
            '#EXTINF:-1 tvg-name="STAR Crime " tvg-logo="https://www.glebul.com/images/tv-logo/star-crime-hd.png" group-title="Филмови" , STAR Crime HD': 'https://www.seir-sanduk.com/hd-star-crime-hd?player=13&id=hd-star-crime-hd&pass=',
            '#EXTINF:-1 tvg-name="7/8 TV" tvg-logo="https://www.glebul.com/images/tv-logo/78-tv-hd.png" group-title="ЕФИРНИ" , 7/8 TV HD': 'https://www.seir-sanduk.com/hd-78-tv-hd?player=13&id=hd-78-tv-hd&pass=',
            '#EXTINF:-1 tvg-name="Nova Sport" tvg-logo="https://www.glebul.com/images/tv-logo/nova-sport-hd.png" group-title="Спортни" , Nova Sport HD': 'https://www.seir-sanduk.com/hd-nova-sport-hd?player=13&id=hd-nova-sport-hd&pass=',
            '#EXTINF:-1 tvg-name="Ring BG" tvg-logo="https://www.glebul.com/images/tv-logo/ring-bg-hd.png" group-title="Спортни" , Ring BG': 'https://www.seir-sanduk.com/hd-ring-bg-hd?player=13&id=hd-ring-bg-hd&pass=',
            '#EXTINF:-1 tvg-name="Diema Sport" tvg-logo="https://www.glebul.com/images/tv-logo/diema-sport-hd.png" group-title="Спортни" , Diema Sport': 'https://www.seir-sanduk.com/hd-diema-sport-hd?player=13&id=hd-diema-sport-hd&pass=',
            '#EXTINF:-1 tvg-name="Diema Sport 2" tvg-logo="https://www.glebul.com/images/tv-logo/diema-sport-2-hd.png" group-title="Спортни" , Diema Sport 2': 'https://www.seir-sanduk.com/hd-diema-sport-2-hd?player=13&id=hd-diema-sport-2-hd&pass=',
            '#EXTINF:-1 tvg-name="Diema Sport 3" tvg-logo="https://www.glebul.com/images/tv-logo/diema-sport-3-hd.png" group-title="Спортни" , Diema Sport 3': 'https://www.seir-sanduk.com/hd-diema-sport-3-hd?player=13&id=hd-diema-sport-3-hd&pass=',
            '#EXTINF:-1 tvg-name="Max Sport 1 HD" tvg-logo="https://www.glebul.com/images/tv-logo/max-sport-1-hd.png" group-title="Спортни" , Max Sport 1 HD': 'https://www.seir-sanduk.com/hd-max-sport-1-hd?player=13&id=hd-max-sport-1-hd&pass=',
            '#EXTINF:-1 tvg-name="Max Sport 2 HD" tvg-logo="https://www.glebul.com/images/tv-logo/max-sport-2-hd.png" group-title="Спортни" , Max Sport 2 HD': 'https://www.seir-sanduk.com/hd-max-sport-2-hd?player=13&id=hd-max-sport-2-hd&pass=',
            '#EXTINF:-1 tvg-name="Max Sport 3 HD" tvg-logo="https://www.glebul.com/images/tv-logo/max-sport-3-hd.png" group-title="Спортни" , Max Sport 3 HD': 'https://www.seir-sanduk.com/hd-max-sport-3-hd?player=13&id=hd-max-sport-3-hd&pass=',
            '#EXTINF:-1 tvg-name="Max Sport 4 HD" tvg-logo="https://www.glebul.com/images/tv-logo/max-sport-4-hd.png" group-title="Спортни" , Max Sport 4 HD': 'https://www.seir-sanduk.com/hd-max-sport-4-hd?player=13&id=hd-max-sport-4-hd&pass=',
            '#EXTINF:-1 tvg-name="Eurosport" tvg-logo="https://www.glebul.com/images/tv-logo/eurosport-1-hd.png" group-title="Спортни" , Eurosport HD': 'https://www.seir-sanduk.com/hd-eurosport-1-hd?player=13&id=hd-eurosport-1-hd&pass=',
            '#EXTINF:-1 tvg-name="Eurosport 2" tvg-logo="https://www.glebul.com/images/tv-logo/eurosport-2-hd.png" group-title="Спортни" , Eurosport 2 HD': 'https://www.seir-sanduk.com/hd-eurosport-2-hd?player=13&id=hd-eurosport-2-hd&pass=',
            #'#EXTINF:-1 tvg-id="FilmBox Stars" tvg-name="FilmBox Stars" tvg-logo="https://www.bg-gledai.video/wp-content/uploads/filmboxplus.png" group-title="Филмови" , FilmBox Stars': '',
            #'#EXTINF:-1 tvg-id="FilmBox Extra" tvg-name="FilmBox Extra" tvg-logo="https://www.bg-gledai.video/wp-content/uploads/filmboxextra.png" group-title="Филмови" , FilmBox Extra': '',
            #'#EXTINF:-1 tvg-id="MovieStar.bg" tvg-name="Moviestar HD" tvg-logo="https://www.bg-gledai.video/wp-content/uploads/moviestar.png" group-title="Филмови" , Moviestar HD': '',
            #'#EXTINF:-1 tvg-id="amc.bg" tvg-name="AMC" tvg-logo="https://www.bg-gledai.video/wp-content/uploads/amc.png" group-title="Филмови" , AMC': '',
            '#EXTINF:-1 tvg-id="AXN" tvg-name="AXN" tvg-logo="https://www.glebul.com/images/tv-logo/axn.png" group-title="Филмови" , AXN': 'https://www.seir-sanduk.com/axn?player=13&id=axn&pass=',
            '#EXTINF:-1 tvg-name="Discovery Channel" tvg-logo="https://www.glebul.com/images/tv-logo/discovery-channel-hd.png" group-title="Научни" , Discovery Channel HD': 'https://www.seir-sanduk.com/hd-discovery-channel-hd?player=13&id=hd-discovery-channel-hd&pass=',
            '#EXTINF:-1 tvg-name="NatGeo Wild" tvg-logo="https://www.glebul.com/images/tv-logo/nat-geo-wild-hd.png" group-title="Научни" , Nat Geo Wild HD': 'https://www.seir-sanduk.com/hd-nat-geo-wild-hd?player=13&id=hd-nat-geo-wild-hd&pass=',
            #'#EXTINF:-1 tvg-id="HistoryChannel.bg" tvg-name="History Channel HD" tvg-logo="https://www.bg-gledai.video/wp-content/uploads/history-1.png" group-title="Научни" , History Channel HD': '',
            #'#EXTINF:-1 tvg-id="DocuBox" tvg-name="DocuBox" tvg-logo="https://www.bg-gledai.video/wp-content/uploads/docubox.png" group-title="Научни" , Docu Box HD': '',
            #'#EXTINF:-1 tvg-id="ViasatExplorer.bg" tvg-name="Viasat Explore HD" tvg-logo="https://www.bg-gledai.video/wp-content/uploads/viasat_explore.png" group-title="Научни" , Viasat Explore HD': '',
            #'#EXTINF:-1 tvg-id="ViasatHistory.bg" tvg-name="Viasat History HD" tvg-logo="https://www.bg-gledai.video/wp-content/uploads/viasat_history.png" group-title="Научни" , Viasat History HD': '',
            #'#EXTINF:-1 tvg-id="ViasatNature.bg" tvg-name="Viasat Nature HD" tvg-logo="https://www.bg-gledai.video/wp-content/uploads/viasat_nature.png" group-title="Научни" , Viasat Nature HD': '',
            #'#EXTINF:-1 tvg-id="AnimalPlanet.bg" tvg-name="Animal Planet HD" tvg-logo="https://www.glebul.com/images/tv-logo/animal-planet.png" group-title="Научни" , Animal Planet HD': '',
            '#EXTINF:-1 tvg-name="DSTV" tvg-logo="https://www.glebul.com/images/tv-logo/dstv.png" group-title="Музикални" , DSTV': 'https://www.seir-sanduk.com/dstv?player=13&id=dstv&pass=',
            #'#EXTINF:-1 tvg-id="Balkanika.bg" tvg-name="Balkanika HD" tvg-logo="https://www.glebul.com/images/tv-logo/balkanika-hd.png" group-title="Музикални" , Balkanika HD': '',
            '#EXTINF:-1 tvg-name="Planeta" tvg-logo="https://www.glebul.com/images/tv-logo/planeta-hd.png" group-title="Музикални" , Planeta HD': 'https://www.seir-sanduk.com/hd-planeta-hd?player=13&id=hd-planeta-hd&pass=',
            '#EXTINF:-1 tvg-name="Planeta Folk" tvg-logo="https://www.glebul.com/images/tv-logo/planeta-folk.png" group-title="Музикални" , Planeta Folk': 'https://www.seir-sanduk.com/planeta-folk?player=13&id=planeta-folk&pass=',
            '#EXTINF:-1 tvg-name="The Voice" tvg-logo="https://www.glebul.com/images/tv-logo/the-voice.png" group-title="Музикални" , The Voice': 'https://www.seir-sanduk.com/the-voice?player=13&id=he-voice&pass=',
            '#EXTINF:-1 tvg-name="City TV" tvg-logo="https://www.glebul.com/images/tv-logo/city-tv.png" group-title="Музикални" , City TV': 'https://www.seir-sanduk.com/city-tv?player=13&id=city-tv&pass=',
            '#EXTINF:-1 tvg-name="folklor-tv" tvg-logo="https://www.glebul.com/images/tv-logo/folklor-tv.png" group-title="Музикални" , Folklor TV': 'https://www.seir-sanduk.com/folklor-tv=?player=13&id=folklor-tv&pass=',
            '#EXTINF:-1 tvg-name="Rodina TV" tvg-logo="https://www.glebul.com/images/tv-logo/rodina-tv.png" group-title="Музикални" , Rodina TV HD': 'https://www.seir-sanduk.com/rodina-tv?player=13&id=rodina-tv&pass=',
            '#EXTINF:-1 tvg-name="TiankovFolk" tvg-logo="https://www.glebul.com/images/tv-logo/tiankov-tv.png" group-title="Музикални" , Tiankov Folk': 'https://www.seir-sanduk.com/tiankov-tv?player=13&id=tiankov-tv&pass=', 
            '#EXTINF:-1 tvg-name="Cartoon Network" tvg-logo="https://www.glebul.com/images/tv-logo/cartoon-network.png" group-title="Детски" , Cartoon Network HD': 'https://www.seir-sanduk.com/cartoon-network?player=13&id=cartoon-network&pass=',
            '#EXTINF:-1 tvg-name="Disney channel" tvg-logo="https://www.glebul.com/images/tv-logo/disney-channel.png" group-title="Детски" , Disney channel': 'https://www.seir-sanduk.com/disney-channel?player=13&id=disney-channel&pass=',
            '#EXTINF:-1 tvg-name="Nickeldeon" tvg-logo="https://www.glebul.com/images/tv-logo/nickelodeon.png" group-title="Детски" , Nickelodeon': 'https://www.seir-sanduk.com/nickelodeon?player=13&id=nickelodeon&pass=',
            '#EXTINF:-1 tvg-name="Nick Jr." tvg-logo="https://www.glebul.com/images/tv-logo/nick-jr.png" group-title="Детски" , Nick Jr': 'https://www.seir-sanduk.com/nick-jr?player=13&id=nick-jr&pass=',
            '#EXTINF:-1 tvg-name="EKids" tvg-logo="https://www.glebul.com/images/tv-logo/e-kids.png" group-title="Детски" , EKids': 'https://www.seir-sanduk.com/e-kids?player=13&id=e-kids&pass=',
            '#EXTINF:-1 tvg-name="Nicktoons" tvg-logo="https://www.glebul.com/images/tv-logo/nicktoons.png" group-title="Детски" , Nicktoons': 'https://www.seir-sanduk.com/nicktoons?player=13&id=nicktoons&pass=',
            '#EXTINF:-1 tvg-name="National Geographic" tvg-logo="https://www.glebul.com/images/tv-logo/nat-geo-hd.png" group-title="Научни" , National Geographic HD': 'https://www.seir-sanduk.com/hd-nat-geo-hd?player=13&id=hd-nat-geo-hd&pass=',
            '#EXTINF:-1 tvg-name="Travel" tvg-logo="https://www.glebul.com/images/tv-logo/travel-tv.png" group-title="Други" , Travel TV': 'https://www.seir-sanduk.com/travel-tv?player=13&id=travel-tv&pass=',
            #'#EXTINF:-1 tvg-name="Magic" tvg-logo="https://www.bg-gledai.video/wp-content/uploads/fantv.png" group-title="Музикални" , Magic TV': '',
            '#EXTINF:-1 tvg-name="VTK" tvg-logo="https://www.glebul.com/images/tv-logo/vtk.png" group-title="Други" , VTK': 'https://www.seir-sanduk.com/vtk?player=13&id=vtk&pass=',
            '#EXTINF:-1 tvg-name="CodeFashion HD" tvg-logo="https://www.glebul.com/images/tv-logo/code-fashion-tv-hd.png" group-title="Други" , CodeFashion': 'https://www.seir-sanduk.com/hd-code-fashion-tv-hd?player=13&id=hd-code-fashion-tv-hd&pass=',
            '#EXTINF:-1 tvg-name="Food Network" tvg-logo="https://www.glebul.com/images/tv-logo/food-network-hd.png" group-title="Други" , Food Network': 'https://www.seir-sanduk.com/hd-food-network-hd?player=13&id=hd-food-network-hd&pass=', 
            '#EXTINF:-1 tvg-name="Epic Drama" tvg-logo="https://www.glebul.com/images/tv-logo/epic-drama-hd.png" group-title="Филмови" , Epic Drama': 'https://www.seir-sanduk.com/hd-epic-drama-hd?player=13&id=hd-epic-drama-hd&pass=',
            '#EXTINF:-1 tvg-name="TLC" tvg-logo="https://www.glebul.com/images/tv-logo/tlc.png" group-title="Други" , TLC HD': 'https://www.seir-sanduk.com/tlc?player=13&id=tlc&pass=',
            '#EXTINF:-1 tvg-name="24 Kitchen" tvg-logo="https://www.glebul.com/images/tv-logo/24-kitchen-hd.png" group-title="Други" , 24 Kitchen HD': 'https://www.seir-sanduk.com/hd-24-kitchen-hd?player=13&id=hd-24-kitchen-hd&pass=',
            '#EXTINF:-1 tvg-name="Travel Channel" tvg-logo="https://www.glebul.com/images/tv-logo/travel-channel-hd.png" group-title="Научни" , Travel Channel': 'https://www.seir-sanduk.com/hd-travel-channel-hd?player=13&id=hd-travel-channel-hd&pass=' 
        
            

    # Add more channels as needed
}

# Функция за намиране на m3u8 линкове
def update_links(channel, source_link):
    with requests.Session() as session:
        response = session.get(source_link)
        match = re.search(r'https://[^\s"]+\.m3u8(?:\?[^\s"]*)?', response.text)
        if match:
            m3u_link = match.group(0)
            print(f"Fetched m3u link for {channel}: {m3u_link}")
            return m3u_link
        else:
            print(f"No m3u link found for {channel}")
            return None

# Събиране на линковете
data_list = []
m3u_links = []


for channel, source_link in channel_mapping.items():
#    source_link = source_link.replace('password', password)  # Заместваме password
    fetched_link = update_links(channel, source_link)
    data_list.append({'Channel': channel, 'SourceLink': source_link, 'LinkToUpdate': fetched_link})
    if fetched_link:
        m3u_links.append(f"{channel}\n{fetched_link}")

#for channel, source_link in channel_mapping.items():
#    fetched_link = update_links(channel, source_link)
#    data_list.append({'Channel': channel, 'SourceLink': source_link, 'LinkToUpdate': fetched_link})
#    if fetched_link:
#        m3u_links.append(f"{channel}\n{fetched_link}")

#channel_df = pd.DataFrame(data_list)

# Запис във файла sources.m3u
file_path = '/Users/administrator/Downloads/connecting/sources.m3u'
extra_file_path = 'radios.m3u'

with open(file_path, 'w') as file:
    file.write('#EXTM3U catchup="flussonic" url-tvg="https://github.com/harrygg/EPG/raw/refs/heads/master/all-2days.full.epg.xml.gz"\n\n')  # Добавен \n за нов ред
    for link in m3u_links:
        file.write(link + '\n')

    # + Добавяне на съдържанието от другия файл (radios.m3u)
#    try:
#        with open(extra_file_path, 'r') as extra_file:
#            for line in extra_file:
#                file.write(line)
#    except FileNotFoundError:
#        print(f"Файлът {extra_file_path} не беше намерен. Пропускам добавянето му.")

print(f"Файлът {file_path} беше обновен с новите линкове.")

# 🔁 Замяна на .m3u8 с .mmpeg
with open(file_path, 'r') as file:
    content = file.read()

# Замени разширението
updated_content = content.replace('ssdraid.glebul.com', 'cdn11.glebul.com:8443').replace('rewind-86400', 'index')
# Запиши отново файла с променените линкове
with open(file_path, 'w') as file:
    file.write(updated_content)

print(f"File generated {file_path}.")
