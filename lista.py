import requests
import os
import re
import json
import xml.etree.ElementTree as ET
from collections import defaultdict
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()

def merger_playlist():
    # Codice del primo script qui
    # Aggiungi il codice del tuo script "merger_playlist.py" in questa funzione.
    # Ad esempio:
    print("Eseguendo il merger_playlist.py...")
    # Il codice che avevi nello script "merger_playlist.py" va qui, senza modifiche.
    import requests
    import os
    from dotenv import load_dotenv

    # Carica le variabili d'ambiente dal file .env
    load_dotenv()

    NOMEREPO = os.getenv("NOMEREPO", "").strip()
    NOMEGITHUB = os.getenv("NOMEGITHUB", "").strip()

    # Percorsi o URL delle playlist M3U8
    url1 = "channels_italy.m3u8"  # File locale
    url2 = "eventi.m3u8"   
    url3 = "https://raw.githubusercontent.com/Brenders/Pluto-TV-Italia-M3U/main/PlutoItaly.m3u"  # Remoto

    # Funzione per scaricare o leggere una playlist
    def download_playlist(source, append_params=False, exclude_group_title=None):
        if source.startswith("http"):
            response = requests.get(source)
            response.raise_for_status()
            playlist = response.text
        else:
            with open(source, 'r', encoding='utf-8') as f:
                playlist = f.read()

        # Rimuovi intestazione iniziale
        playlist = '\n'.join(line for line in playlist.split('\n') if not line.startswith('#EXTM3U'))

        if exclude_group_title:
            playlist = '\n'.join(line for line in playlist.split('\n') if exclude_group_title not in line)

        return playlist

    # Ottieni la directory dove si trova lo script
    script_directory = os.path.dirname(os.path.abspath(__file__))

    # Scarica/leggi le playlist
    playlist1 = download_playlist(url1)
    playlist2 = download_playlist(url2, append_params=True)
    playlist3 = download_playlist(url3)

    # Unisci le playlist
    lista = playlist1 + "\n" + playlist2 + "\n" + playlist3

    # Aggiungi intestazione EPG
    lista = f'#EXTM3U x-tvg-url="https://raw.githubusercontent.com/{NOMEGITHUB}/{NOMEREPO}/refs/heads/main/epg.xml"\n' + lista

    # Salva la playlist
    output_filename = os.path.join(script_directory, "lista.m3u")
    with open(output_filename, 'w', encoding='utf-8') as file:
        file.write(lista)

    print(f"Playlist combinata salvata in: {output_filename}")

# Funzione per il primo script (merger_playlist.py)
def merger_playlistworld():
    # Codice del primo script qui
    # Aggiungi il codice del tuo script "merger_playlist.py" in questa funzione.
    # Ad esempio:
    print("Eseguendo il merger_playlist.py...")
    # Il codice che avevi nello script "merger_playlist.py" va qui, senza modifiche.
    import requests
    import os
    from dotenv import load_dotenv

    # Carica le variabili d'ambiente dal file .env
    load_dotenv()

    NOMEREPO = os.getenv("NOMEREPO", "").strip()
    NOMEGITHUB = os.getenv("NOMEGITHUB", "").strip()

    # Percorsi o URL delle playlist M3U8
    url1 = "channels_italy.m3u8"  # File locale
    url2 = "eventi.m3u8"   
    url3 = "https://raw.githubusercontent.com/Brenders/Pluto-TV-Italia-M3U/main/PlutoItaly.m3u"  # Remoto
    url4 = "world.m3u8"           # File locale

    # Funzione per scaricare o leggere una playlist
    def download_playlist(source, append_params=False, exclude_group_title=None):
        if source.startswith("http"):
            response = requests.get(source)
            response.raise_for_status()
            playlist = response.text
        else:
            with open(source, 'r', encoding='utf-8') as f:
                playlist = f.read()

        # Rimuovi intestazione iniziale
        playlist = '\n'.join(line for line in playlist.split('\n') if not line.startswith('#EXTM3U'))

        if exclude_group_title:
            playlist = '\n'.join(line for line in playlist.split('\n') if exclude_group_title not in line)

        return playlist

    # Ottieni la directory dove si trova lo script
    script_directory = os.path.dirname(os.path.abspath(__file__))

    # Scarica/leggi le playlist
    playlist1 = download_playlist(url1)
    playlist2 = download_playlist(url2, append_params=True)
    playlist3 = download_playlist(url3)
    playlist4 = download_playlist(url4, exclude_group_title="Italy")

    # Unisci le playlist
    lista = playlist1 + "\n" + playlist2 + "\n" + playlist3 + "\n" + playlist4

    # Aggiungi intestazione EPG
    lista = f'#EXTM3U x-tvg-url="https://raw.githubusercontent.com/{NOMEGITHUB}/{NOMEREPO}/refs/heads/main/epg.xml"\n' + lista

    # Salva la playlist
    output_filename = os.path.join(script_directory, "lista.m3u")
    with open(output_filename, 'w', encoding='utf-8') as file:
        file.write(lista)

    print(f"Playlist combinata salvata in: {output_filename}")

# Funzione per il secondo script (epg_merger.py)
def epg_merger():
    # Codice del secondo script qui
    # Aggiungi il codice del tuo script "epg_merger.py" in questa funzione.
    # Ad esempio:
    print("Eseguendo l'epg_merger.py...")
    # Il codice che avevi nello script "epg_merger.py" va qui, senza modifiche.
    import requests
    import gzip
    import os
    import xml.etree.ElementTree as ET
    import io

    # URL dei file GZIP o XML da elaborare
    urls_gzip = [
        'https://www.open-epg.com/files/italy1.xml',
        'https://www.open-epg.com/files/italy2.xml',
        'https://www.open-epg.com/files/italy3.xml',
        'https://www.open-epg.com/files/italy4.xml',
        'https://epgshare01.online/epgshare01/epg_ripper_IT1.xml.gz'
    ]

    # File di output
    output_xml = 'epg.xml'    # Nome del file XML finale

    # URL remoto di it.xml
    url_it = 'https://raw.githubusercontent.com/matthuisman/i.mjh.nz/master/PlutoTV/it.xml'

    # File eventi locale
    path_eventi = 'eventi.xml'

    def download_and_parse_xml(url):
        """Scarica un file .xml o .gzip e restituisce l'ElementTree."""
        try:
            response = requests.get(url, timeout=30)
            response.raise_for_status()

            # Prova a decomprimere come GZIP
            try:
                with gzip.open(io.BytesIO(response.content), 'rb') as f_in:
                    xml_content = f_in.read()
            except (gzip.BadGzipFile, OSError):
                # Non è un file gzip, usa direttamente il contenuto
                xml_content = response.content

            return ET.ElementTree(ET.fromstring(xml_content))
        except requests.exceptions.RequestException as e:
            print(f"Errore durante il download da {url}: {e}")
        except ET.ParseError as e:
            print(f"Errore nel parsing del file XML da {url}: {e}")
        return None

    # Creare un unico XML vuoto
    root_finale = ET.Element('tv')
    tree_finale = ET.ElementTree(root_finale)

    # Processare ogni URL
    for url in urls_gzip:
        tree = download_and_parse_xml(url)
        if tree is not None:
            root = tree.getroot()
            for element in root:
                root_finale.append(element)

    # Aggiungere eventi.xml da file locale
    if os.path.exists(path_eventi):
        try:
            tree_eventi = ET.parse(path_eventi)
            root_eventi = tree_eventi.getroot()
            for programme in root_eventi.findall(".//programme"):
                root_finale.append(programme)
        except ET.ParseError as e:
            print(f"Errore nel parsing del file eventi.xml: {e}")
    else:
        print(f"File non trovato: {path_eventi}")

    # Aggiungere it.xml da URL remoto
    tree_it = download_and_parse_xml(url_it)
    if tree_it is not None:
        root_it = tree_it.getroot()
        for programme in root_it.findall(".//programme"):
            root_finale.append(programme)
    else:
        print(f"Impossibile scaricare o analizzare il file it.xml da {url_it}")

    # Funzione per pulire attributi
    def clean_attribute(element, attr_name):
        if attr_name in element.attrib:
            old_value = element.attrib[attr_name]
            new_value = old_value.replace(" ", "").lower()
            element.attrib[attr_name] = new_value

    # Pulire gli ID dei canali
    for channel in root_finale.findall(".//channel"):
        clean_attribute(channel, 'id')

    # Pulire gli attributi 'channel' nei programmi
    for programme in root_finale.findall(".//programme"):
        clean_attribute(programme, 'channel')

    # Salvare il file XML finale
    with open(output_xml, 'wb') as f_out:
        tree_finale.write(f_out, encoding='utf-8', xml_declaration=True)
    print(f"File XML salvato: {output_xml}")

def eventi_m3u8_generator_world():
    # Codice del terzo script qui
    # Aggiungi il codice del tuo script "eventi_m3u8_generator.py" in questa funzione.
    print("Eseguendo l'eventi_m3u8_generator.py...")
    # Il codice che avevi nello script "eventi_m3u8_generator.py" va qui, senza modifiche.
    import json 
    import re 
    import requests 
    from datetime import datetime, timedelta 
    from dateutil import parser 
    import urllib.parse 
    import os
    from dotenv import load_dotenv
    from PIL import Image, ImageDraw, ImageFont
    import io
    import time

    # Carica le variabili d'ambiente dal file .env
    load_dotenv()

    PROXY = os.getenv("PROXYIP", "").strip()  
    JSON_FILE = "daddyliveSchedule.json" 
    OUTPUT_FILE = "eventi.m3u8" 
    LINK_DADDY = os.getenv("LINK_DADDY", "https://daddylive.dad").strip()

        # Funzione per pulire il nome della categoria
    def clean_category_name(name): 
        # Rimuove tag html come </span> o simili 
        return re.sub(r'<[^>]+>', '', name).strip()

    def clean_tvg_id(tvg_id):
        """
        Pulisce il tvg-id rimuovendo caratteri speciali, spazi e convertendo tutto in minuscolo
        """
        import re
        # Rimuove caratteri speciali comuni mantenendo solo lettere e numeri
        # Solo lettere e numeri, incluse vocali accentate italiane
        cleaned = re.sub(r'[^a-zA-Z0-9àèéìòóùÀÈÉÌÒÓÙ]', '', tvg_id)
        return cleaned.lower()

    def search_logo_for_event(event_name): 
        """ 
        Cerca un logo per l'evento specificato utilizzando un motore di ricerca 
        Restituisce l'URL dell'immagine trovata o None se non trovata 
        """ 
        try: 
            # Rimuovi eventuali riferimenti all'orario dal nome dell'evento
            # Cerca pattern come "Team A vs Team B (20:00)" e rimuovi la parte dell'orario
            clean_event_name = re.sub(r'\s*\(\d{1,2}:\d{2}\)\s*$', '', event_name)
            # Se c'Ã¨ un ':', prendi solo la parte dopo
            if ':' in clean_event_name:
                clean_event_name = clean_event_name.split(':', 1)[1].strip()

            # Verifica se l'evento contiene "vs" o "-" per identificare le due squadre
            teams = None
            if " vs " in clean_event_name:
                teams = clean_event_name.split(" vs ")
            elif " VS " in clean_event_name:
                teams = clean_event_name.split(" VS ")
            elif " VS. " in clean_event_name:
                teams = clean_event_name.split(" VS. ")
            elif " vs. " in clean_event_name:
                teams = clean_event_name.split(" vs. ")

            # Se abbiamo identificato due squadre, cerchiamo i loghi separatamente
            if teams and len(teams) == 2:
                team1 = teams[0].strip()
                team2 = teams[1].strip()

                print(f"[🔍] Ricerca logo per Team 1: {team1}")
                logo1_url = search_team_logo(team1)

                print(f"[🔍] Ricerca logo per Team 2: {team2}")
                logo2_url = search_team_logo(team2)

                # Se abbiamo trovato entrambi i loghi, creiamo un'immagine combinata
                if logo1_url and logo2_url:
                    # Scarica i loghi e l'immagine VS
                    try:
                        from os.path import exists, getmtime

                        # Crea la cartella logos se non esiste
                        logos_dir = "logos"
                        os.makedirs(logos_dir, exist_ok=True)

                        # Verifica se l'immagine combinata esiste giÃ  e non Ã¨ obsoleta
                        output_filename = f"logos/{team1}_vs_{team2}.png"
                        if exists(output_filename):
                            file_age = current_time - os.path.getmtime(output_filename)
                            if file_age <= three_hours_in_seconds:
                                print(f"[✓] Utilizzo immagine combinata esistente: {output_filename}")

                                # Carica le variabili d'ambiente per GitHub
                                NOMEREPO = os.getenv("NOMEREPO", "").strip()
                                NOMEGITHUB = os.getenv("NOMEGITHUB", "").strip()

                                # Se le variabili GitHub sono disponibili, restituisci l'URL raw di GitHub
                                if NOMEGITHUB and NOMEREPO:
                                    github_raw_url = f"https://raw.githubusercontent.com/{NOMEGITHUB}/{NOMEREPO}/main/{output_filename}"
                                    print(f"[✓] URL GitHub generato per logo esistente: {github_raw_url}")
                                    return github_raw_url
                                else:
                                    # Altrimenti restituisci il percorso locale
                                    return output_filename

                        # Scarica i loghi
                        response1 = requests.get(logo1_url, timeout=10)
                        img1 = Image.open(io.BytesIO(response1.content))

                        response2 = requests.get(logo2_url, timeout=10)
                        img2 = Image.open(io.BytesIO(response2.content))

                        # Carica l'immagine VS (assicurati che esista nella directory corrente)
                        vs_path = "vs.png"
                        if exists(vs_path):
                            img_vs = Image.open(vs_path)
                            # Converti l'immagine VS in modalitÃ  RGBA se non lo Ã¨ giÃ 
                            if img_vs.mode != 'RGBA':
                                img_vs = img_vs.convert('RGBA')
                        else:
                            # Crea un'immagine di testo "VS" se il file non esiste
                            img_vs = Image.new('RGBA', (100, 100), (255, 255, 255, 0))
                            from PIL import ImageDraw, ImageFont
                            draw = ImageDraw.Draw(img_vs)
                            try:
                                font = ImageFont.truetype("arial.ttf", 40)
                            except:
                                font = ImageFont.load_default()
                            draw.text((30, 30), "VS", fill=(255, 0, 0), font=font)

                        # Ridimensiona le immagini a dimensioni uniformi
                        size = (150, 150)
                        img1 = img1.resize(size)
                        img2 = img2.resize(size)
                        img_vs = img_vs.resize((100, 100))

                        # Assicurati che tutte le immagini siano in modalitÃ  RGBA per supportare la trasparenza
                        if img1.mode != 'RGBA':
                            img1 = img1.convert('RGBA')
                        if img2.mode != 'RGBA':
                            img2 = img2.convert('RGBA')

                        # Crea una nuova immagine con spazio per entrambi i loghi e il VS
                        combined_width = 300
                        combined = Image.new('RGBA', (combined_width, 150), (255, 255, 255, 0))

                        # Posiziona le immagini con il VS sovrapposto al centro
                        # Posiziona il primo logo a sinistra
                        combined.paste(img1, (0, 0), img1)
                        # Posiziona il secondo logo a destra
                        combined.paste(img2, (combined_width - 150, 0), img2)

                        # Posiziona il VS al centro, sovrapposto ai due loghi
                        vs_x = (combined_width - 100) // 2

                        # Crea una copia dell'immagine combinata prima di sovrapporre il VS
                        # Questo passaggio Ã¨ importante per preservare i dettagli dei loghi sottostanti
                        combined_with_vs = combined.copy()
                        combined_with_vs.paste(img_vs, (vs_x, 25), img_vs)

                        # Usa l'immagine con VS sovrapposto
                        combined = combined_with_vs

                        # Salva l'immagine combinata
                        os.makedirs(os.path.dirname(output_filename), exist_ok=True)
                        combined.save(output_filename)

                        print(f"[✓] Immagine combinata creata: {output_filename}")

                        # Carica le variabili d'ambiente per GitHub
                        NOMEREPO = os.getenv("NOMEREPO", "").strip()
                        NOMEGITHUB = os.getenv("NOMEGITHUB", "").strip()

                        # Se le variabili GitHub sono disponibili, restituisci l'URL raw di GitHub
                        if NOMEGITHUB and NOMEREPO:
                            github_raw_url = f"https://raw.githubusercontent.com/{NOMEGITHUB}/{NOMEREPO}/main/{output_filename}"
                            print(f"[✓] URL GitHub generato: {github_raw_url}")
                            return github_raw_url
                        else:
                            # Altrimenti restituisci il percorso locale
                            return output_filename

                    except Exception as e:
                        print(f"[!] Errore nella creazione dell'immagine combinata: {e}")
                        # Se fallisce, restituisci solo il primo logo trovato
                        return logo1_url

                # Se non abbiamo trovato entrambi i loghi, restituisci quello che abbiamo
                return logo1_url or logo2_url
            if ':' in event_name:
                # Usa la parte prima dei ":" per la ricerca
                prefix_name = event_name.split(':', 1)[0].strip()
                print(f"[🔍] Tentativo ricerca logo con prefisso: {prefix_name}")

                # Prepara la query di ricerca con il prefisso
                search_query = urllib.parse.quote(f"{prefix_name} logo")

                # Utilizziamo l'API di Bing Image Search con parametri migliorati
                search_url = f"https://www.bing.com/images/search?q={search_query}&qft=+filterui:photo-transparent+filterui:aspect-square&form=IRFLTR"

                headers = { 
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36",
                    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
                    "Accept-Language": "it-IT,it;q=0.9,en-US;q=0.8,en;q=0.7",
                    "Cache-Control": "max-age=0",
                    "Connection": "keep-alive"
                } 

                response = requests.get(search_url, headers=headers, timeout=10)

                if response.status_code == 200: 
                    # Metodo 1: Cerca pattern per murl (URL dell'immagine media)
                    patterns = [
                        r'murl&quot;:&quot;(https?://[^&]+)&quot;',
                        r'"murl":"(https?://[^"]+)"',
                        r'"contentUrl":"(https?://[^"]+\.(?:png|jpg|jpeg|svg))"',
                        r'<img[^>]+src="(https?://[^"]+\.(?:png|jpg|jpeg|svg))[^>]+class="mimg"',
                        r'<a[^>]+class="iusc"[^>]+m=\'{"[^"]*":"[^"]*","[^"]*":"(https?://[^"]+)"'
                    ]

                    for pattern in patterns:
                        matches = re.findall(pattern, response.text)
                        if matches and len(matches) > 0:
                            # Prendi il primo risultato che sembra un logo (preferibilmente PNG o SVG)
                            for match in matches:
                                if '.png' in match.lower() or '.svg' in match.lower():
                                    print(f"[✓] Logo trovato con prefisso: {match}")
                                    return match
                            # Se non troviamo PNG o SVG, prendi il primo risultato
                            print(f"[✓] Logo trovato con prefisso: {matches[0]}")
                            return matches[0]

            # Se non riusciamo a identificare le squadre e il prefisso non ha dato risultati, procedi con la ricerca normale
            print(f"[🔍] Ricerca standard per: {clean_event_name}")


            # Se non riusciamo a identificare le squadre, procedi con la ricerca normale
            # Prepara la query di ricerca piÃ¹ specifica
            search_query = urllib.parse.quote(f"{clean_event_name} logo")

            # Utilizziamo l'API di Bing Image Search con parametri migliorati
            search_url = f"https://www.bing.com/images/search?q={search_query}&qft=+filterui:photo-transparent+filterui:aspect-square&form=IRFLTR"

            headers = { 
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
                "Accept-Language": "it-IT,it;q=0.9,en-US;q=0.8,en;q=0.7",
                "Cache-Control": "max-age=0",
                "Connection": "keep-alive"
            } 

            response = requests.get(search_url, headers=headers, timeout=10)

            if response.status_code == 200: 
                # Metodo 1: Cerca pattern per murl (URL dell'immagine media)
                patterns = [
                    r'murl&quot;:&quot;(https?://[^&]+)&quot;',
                    r'"murl":"(https?://[^"]+)"',
                    r'"contentUrl":"(https?://[^"]+\.(?:png|jpg|jpeg|svg))"',
                    r'<img[^>]+src="(https?://[^"]+\.(?:png|jpg|jpeg|svg))[^>]+class="mimg"',
                    r'<a[^>]+class="iusc"[^>]+m=\'{"[^"]*":"[^"]*","[^"]*":"(https?://[^"]+)"'
                ]

                for pattern in patterns:
                    matches = re.findall(pattern, response.text)
                    if matches and len(matches) > 0:
                        # Prendi il primo risultato che sembra un logo (preferibilmente PNG o SVG)
                        for match in matches:
                            if '.png' in match.lower() or '.svg' in match.lower():
                                return match
                        # Se non troviamo PNG o SVG, prendi il primo risultato
                        return matches[0]

                # Metodo alternativo: cerca JSON incorporato nella pagina
                json_match = re.search(r'var\s+IG\s*=\s*(\{.+?\});\s*', response.text)
                if json_match:
                    try:
                        # Estrai e analizza il JSON
                        json_str = json_match.group(1)
                        # Pulisci il JSON se necessario
                        json_str = re.sub(r'([{,])\s*([a-zA-Z0-9_]+):', r'\1"\2":', json_str)
                        data = json.loads(json_str)

                        # Cerca URL di immagini nel JSON
                        if 'images' in data and len(data['images']) > 0:
                            for img in data['images']:
                                if 'murl' in img:
                                    return img['murl']
                    except Exception as e:
                        print(f"[!] Errore nell'analisi JSON: {e}")

                print(f"[!] Nessun logo trovato per '{clean_event_name}' con i pattern standard")

                # Ultimo tentativo: cerca qualsiasi URL di immagine nella pagina
                any_img = re.search(r'(https?://[^"\']+\.(?:png|jpg|jpeg|svg|webp))', response.text)
                if any_img:
                    return any_img.group(1)

        except Exception as e: 
            print(f"[!] Errore nella ricerca del logo per '{event_name}': {e}") 

        # Se non troviamo nulla, restituiamo None 
        return None

    def search_team_logo(team_name):
        """
        Funzione dedicata alla ricerca del logo di una singola squadra
        """
        try:
            # Prepara la query di ricerca specifica per la squadra
            search_query = urllib.parse.quote(f"{team_name} logo")

            # Utilizziamo l'API di Bing Image Search con parametri migliorati
            search_url = f"https://www.bing.com/images/search?q={search_query}&qft=+filterui:photo-transparent+filterui:aspect-square&form=IRFLTR"

            headers = { 
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
                "Accept-Language": "it-IT,it;q=0.9,en-US;q=0.8,en;q=0.7",
                "Cache-Control": "max-age=0",
                "Connection": "keep-alive"
            } 

            response = requests.get(search_url, headers=headers, timeout=10)

            if response.status_code == 200: 
                # Metodo 1: Cerca pattern per murl (URL dell'immagine media)
                patterns = [
                    r'murl&quot;:&quot;(https?://[^&]+)&quot;',
                    r'"murl":"(https?://[^"]+)"',
                    r'"contentUrl":"(https?://[^"]+\.(?:png|jpg|jpeg|svg))"',
                    r'<img[^>]+src="(https?://[^"]+\.(?:png|jpg|jpeg|svg))[^>]+class="mimg"',
                    r'<a[^>]+class="iusc"[^>]+m=\'{"[^"]*":"[^"]*","[^"]*":"(https?://[^"]+)"'
                ]

                for pattern in patterns:
                    matches = re.findall(pattern, response.text)
                    if matches and len(matches) > 0:
                        # Prendi il primo risultato che sembra un logo (preferibilmente PNG o SVG)
                        for match in matches:
                            if '.png' in match.lower() or '.svg' in match.lower():
                                return match
                        # Se non troviamo PNG o SVG, prendi il primo risultato
                        return matches[0]

                # Metodo alternativo: cerca JSON incorporato nella pagina
                json_match = re.search(r'var\s+IG\s*=\s*(\{.+?\});\s*', response.text)
                if json_match:
                    try:
                        # Estrai e analizza il JSON
                        json_str = json_match.group(1)
                        # Pulisci il JSON se necessario
                        json_str = re.sub(r'([{,])\s*([a-zA-Z0-9_]+):', r'\1"\2":', json_str)
                        data = json.loads(json_str)

                        # Cerca URL di immagini nel JSON
                        if 'images' in data and len(data['images']) > 0:
                            for img in data['images']:
                                if 'murl' in img:
                                    return img['murl']
                    except Exception as e:
                        print(f"[!] Errore nell'analisi JSON: {e}")

                print(f"[!] Nessun logo trovato per '{team_name}' con i pattern standard")

                # Ultimo tentativo: cerca qualsiasi URL di immagine nella pagina
                any_img = re.search(r'(https?://[^"\']+\.(?:png|jpg|jpeg|svg|webp))', response.text)
                if any_img:
                    return any_img.group(1)

        except Exception as e: 
            print(f"[!] Errore nella ricerca del logo per '{team_name}': {e}") 

        # Se non troviamo nulla, restituiamo None 
        return None

    def extract_channels_from_json(path): 
        keywords = {"italy", "rai", "italia", "it", "uk", "tnt", "usa", "tennis channel", "tennis stream", "la"} 
        now = datetime.now() 
        yesterday = now.date() - timedelta(days=1)

        with open(path, "r", encoding="utf-8") as f: 
            data = json.load(f) 

        categorized_channels = {} 

        for date_key, sections in data.items(): 
            date_part = date_key.split(" - ")[0] 
            try: 
                date_obj = parser.parse(date_part, fuzzy=True).date() 
            except Exception as e: 
                print(f"[!] Errore parsing data '{date_part}': {e}") 
                continue 

            # Includi sia la data odierna che quella di ieri
            if date_obj != now.date() and date_obj != yesterday:
                continue 

            date_str = date_obj.strftime("%Y-%m-%d") 

            for category_raw, event_items in sections.items(): 
                category = clean_category_name(category_raw) 
                if category not in categorized_channels: 
                    categorized_channels[category] = [] 

                for item in event_items: 
                    time_str = item.get("time", "00:00") 
                    try: 
                        # Prima verifica l'orario originale (senza aggiungere le 2 ore)
                        original_time_obj = datetime.strptime(time_str, "%H:%M")

                        # Se Ã¨ il giorno precedente, includi solo gli eventi dalle 00:00 alle 04:00
                        if date_obj == yesterday:
                            if original_time_obj.hour < 0 or original_time_obj.hour >= 4:
                                continue

                        # Ora aggiungi le 2 ore per il display
                        time_obj = original_time_obj + timedelta(hours=2)
                        event_datetime = datetime.combine(date_obj, time_obj.time()) 

                        # Per il giorno corrente, mantieni la logica esistente
                        if date_obj == now.date() and now - event_datetime > timedelta(hours=2): 
                            continue 

                        time_formatted = time_obj.strftime("%H:%M") 
                    except Exception: 
                        time_formatted = time_str 

                    event_title = item.get("event", "Evento") 

                    for ch in item.get("channels", []): 
                        channel_name = ch.get("channel_name", "") 
                        channel_id = ch.get("channel_id", "") 

                        words = set(re.findall(r'\b\w+\b', channel_name.lower())) 
                        if keywords.intersection(words): 
                            tvg_name = f"{event_title} ({time_formatted})" 
                            categorized_channels[category].append({ 
                                "tvg_name": tvg_name, 
                                "channel_name": channel_name, 
                                "channel_id": channel_id, 
                                "event_title": event_title  # Aggiungiamo il titolo dell'evento per la ricerca del logo 
                            }) 

        return categorized_channels

    def generate_m3u_from_schedule(json_file, output_file): 
        categorized_channels = extract_channels_from_json(json_file) 

        with open(output_file, "w", encoding="utf-8") as f: 
            f.write("#EXTM3U\n") 

            for category, channels in categorized_channels.items(): 
                if not channels: 
                    continue 

                f.write(f'#EXTINF:-1 tvg-name="{category}" group-title="Eventi Live",--- {category} ---\nhttps://example.m3u8\n\n') 

                for ch in channels: 
                    tvg_name = ch["tvg_name"] 
                    channel_id = ch["channel_id"] 
                    event_title = ch["event_title"] 

                    # Cerca un logo per questo evento
                    clean_event_title = re.sub(r'\s*\(\d{1,2}:\d{2}\)\s*$', '', event_title)
                    print(f"[🔍] Ricerca logo per: {clean_event_title}")
                    logo_url = search_logo_for_event(clean_event_title) 
                    logo_attribute = f' tvg-logo="{logo_url}"' if logo_url else '' 

                    # Applica la pulizia al tvg-id
                    tvg_id_cleaned = clean_tvg_id(clean_event_title)

                    stream_url = (f"{PROXY}{LINK_DADDY}/embed/stream-{channel_id}.php")                    
                    f.write(f'#EXTINF:-1 tvg-id="{tvg_id_cleaned}" tvg-name="{tvg_name}"{logo_attribute} group-title="Eventi Live",{tvg_name}\n{stream_url}\n\n')
                    print(f"[✓] {tvg_name}" + (f" (logo trovato)" if logo_url else " (nessun logo trovato)"))

    if __name__ == "__main__": 
        # Assicurati che il modulo requests sia installato 
        try: 
            import requests 
        except ImportError: 
            print("[!] Il modulo 'requests' non Ã¨ installato. Installalo con 'pip install requests'") 
            exit(1) 

        generate_m3u_from_schedule(JSON_FILE, OUTPUT_FILE)

# Funzione per il terzo script (eventi_m3u8_generator.py)
def eventi_m3u8_generator():
    # Codice del terzo script qui
    # Aggiungi il codice del tuo script "eventi_m3u8_generator.py" in questa funzione.
    print("Eseguendo l'eventi_m3u8_generator.py...")
    # Il codice che avevi nello script "eventi_m3u8_generator.py" va qui, senza modifiche.
    import json 
    import re 
    import requests 
    from datetime import datetime, timedelta 
    from dateutil import parser 
    import urllib.parse 
    import os
    from dotenv import load_dotenv
    from PIL import Image, ImageDraw, ImageFont
    import io
    import time

    # Carica le variabili d'ambiente dal file .env
    load_dotenv()

    PROXY = os.getenv("PROXYIP", "").strip()  
    JSON_FILE = "daddyliveSchedule.json" 
    OUTPUT_FILE = "eventi.m3u8" 
    LINK_DADDY = os.getenv("LINK_DADDY", "https://daddylive.dad").strip()

    # Funzione per pulire il nome della categoria
    def clean_category_name(name): 
        # Rimuove tag html come </span> o simili 
        return re.sub(r'<[^>]+>', '', name).strip()

    def clean_tvg_id(tvg_id):
        """
        Pulisce il tvg-id rimuovendo caratteri speciali, spazi e convertendo tutto in minuscolo
        """
        import re
        # Rimuove caratteri speciali comuni mantenendo solo lettere e numeri
        cleaned = re.sub(r'[^a-zA-Z0-9àèéìòóùÀÈÉÌÒÓÙ]', '', tvg_id)
        return cleaned.lower()

    def search_logo_for_event(event_name): 
        """ 
        Cerca un logo per l'evento specificato utilizzando un motore di ricerca 
        Restituisce l'URL dell'immagine trovata o None se non trovata 
        """ 
        try: 
            # Rimuovi eventuali riferimenti all'orario dal nome dell'evento
            # Cerca pattern come "Team A vs Team B (20:00)" e rimuovi la parte dell'orario
            clean_event_name = re.sub(r'\s*\(\d{1,2}:\d{2}\)\s*$', '', event_name)
            # Se c'Ã¨ un ':', prendi solo la parte dopo
            if ':' in clean_event_name:
                clean_event_name = clean_event_name.split(':', 1)[1].strip()

            # Verifica se l'evento contiene "vs" o "-" per identificare le due squadre
            teams = None
            if " vs " in clean_event_name:
                teams = clean_event_name.split(" vs ")
            elif " VS " in clean_event_name:
                teams = clean_event_name.split(" VS ")
            elif " VS. " in clean_event_name:
                teams = clean_event_name.split(" VS. ")
            elif " vs. " in clean_event_name:
                teams = clean_event_name.split(" vs. ")

            # Se abbiamo identificato due squadre, cerchiamo i loghi separatamente
            if teams and len(teams) == 2:
                team1 = teams[0].strip()
                team2 = teams[1].strip()

                print(f"[🔍] Ricerca logo per Team 1: {team1}")
                logo1_url = search_team_logo(team1)

                print(f"[🔍] Ricerca logo per Team 2: {team2}")
                logo2_url = search_team_logo(team2)

                # Se abbiamo trovato entrambi i loghi, creiamo un'immagine combinata
                if logo1_url and logo2_url:
                    # Scarica i loghi e l'immagine VS
                    try:
                        from os.path import exists, getmtime

                        # Crea la cartella logos se non esiste
                        logos_dir = "logos"
                        os.makedirs(logos_dir, exist_ok=True)

                        # Controlla e rimuovi i loghi piÃ¹ vecchi di 3 ore
                        current_time = time.time()
                        three_hours_in_seconds = 3 * 60 * 60

                        for logo_file in os.listdir(logos_dir):
                            logo_path = os.path.join(logos_dir, logo_file)
                            if os.path.isfile(logo_path):
                                file_age = current_time - os.path.getmtime(logo_path)
                                if file_age > three_hours_in_seconds:
                                    try:
                                        os.remove(logo_path)
                                        print(f"[🗑️] Rimosso logo obsoleto: {logo_path}")
                                    except Exception as e:
                                        print(f"[!] Errore nella rimozione del logo {logo_path}: {e}")

                        # Verifica se l'immagine combinata esiste giÃ  e non Ã¨ obsoleta
                        output_filename = f"logos/{team1}_vs_{team2}.png"
                        if exists(output_filename):
                            file_age = current_time - os.path.getmtime(output_filename)
                            if file_age <= three_hours_in_seconds:
                                print(f"[✓] Utilizzo immagine combinata esistente: {output_filename}")

                                # Carica le variabili d'ambiente per GitHub
                                NOMEREPO = os.getenv("NOMEREPO", "").strip()
                                NOMEGITHUB = os.getenv("NOMEGITHUB", "").strip()

                                # Se le variabili GitHub sono disponibili, restituisci l'URL raw di GitHub
                                if NOMEGITHUB and NOMEREPO:
                                    github_raw_url = f"https://raw.githubusercontent.com/{NOMEGITHUB}/{NOMEREPO}/main/{output_filename}"
                                    print(f"[✓] URL GitHub generato per logo esistente: {github_raw_url}")
                                    return github_raw_url
                                else:
                                    # Altrimenti restituisci il percorso locale
                                    return output_filename

                        # Scarica i loghi
                        response1 = requests.get(logo1_url, timeout=10)
                        img1 = Image.open(io.BytesIO(response1.content))

                        response2 = requests.get(logo2_url, timeout=10)
                        img2 = Image.open(io.BytesIO(response2.content))

                        # Carica l'immagine VS (assicurati che esista nella directory corrente)
                        vs_path = "vs.png"
                        if exists(vs_path):
                            img_vs = Image.open(vs_path)
                            # Converti l'immagine VS in modalitÃ  RGBA se non lo Ã¨ giÃ 
                            if img_vs.mode != 'RGBA':
                                img_vs = img_vs.convert('RGBA')
                        else:
                            # Crea un'immagine di testo "VS" se il file non esiste
                            img_vs = Image.new('RGBA', (100, 100), (255, 255, 255, 0))
                            from PIL import ImageDraw, ImageFont
                            draw = ImageDraw.Draw(img_vs)
                            try:
                                font = ImageFont.truetype("arial.ttf", 40)
                            except:
                                font = ImageFont.load_default()
                            draw.text((30, 30), "VS", fill=(255, 0, 0), font=font)

                        # Ridimensiona le immagini a dimensioni uniformi
                        size = (150, 150)
                        img1 = img1.resize(size)
                        img2 = img2.resize(size)
                        img_vs = img_vs.resize((100, 100))

                        # Assicurati che tutte le immagini siano in modalitÃ  RGBA per supportare la trasparenza
                        if img1.mode != 'RGBA':
                            img1 = img1.convert('RGBA')
                        if img2.mode != 'RGBA':
                            img2 = img2.convert('RGBA')

                        # Crea una nuova immagine con spazio per entrambi i loghi e il VS
                        combined_width = 300
                        combined = Image.new('RGBA', (combined_width, 150), (255, 255, 255, 0))

                        # Posiziona le immagini con il VS sovrapposto al centro
                        # Posiziona il primo logo a sinistra
                        combined.paste(img1, (0, 0), img1)
                        # Posiziona il secondo logo a destra
                        combined.paste(img2, (combined_width - 150, 0), img2)

                        # Posiziona il VS al centro, sovrapposto ai due loghi
                        vs_x = (combined_width - 100) // 2

                        # Crea una copia dell'immagine combinata prima di sovrapporre il VS
                        # Questo passaggio Ã¨ importante per preservare i dettagli dei loghi sottostanti
                        combined_with_vs = combined.copy()
                        combined_with_vs.paste(img_vs, (vs_x, 25), img_vs)

                        # Usa l'immagine con VS sovrapposto
                        combined = combined_with_vs

                        # Salva l'immagine combinata
                        os.makedirs(os.path.dirname(output_filename), exist_ok=True)
                        combined.save(output_filename)

                        print(f"[✓] Immagine combinata creata: {output_filename}")

                        # Carica le variabili d'ambiente per GitHub
                        NOMEREPO = os.getenv("NOMEREPO", "").strip()
                        NOMEGITHUB = os.getenv("NOMEGITHUB", "").strip()

                        # Se le variabili GitHub sono disponibili, restituisci l'URL raw di GitHub
                        if NOMEGITHUB and NOMEREPO:
                            github_raw_url = f"https://raw.githubusercontent.com/{NOMEGITHUB}/{NOMEREPO}/main/{output_filename}"
                            print(f"[✓] URL GitHub generato: {github_raw_url}")
                            return github_raw_url
                        else:
                            # Altrimenti restituisci il percorso locale
                            return output_filename

                    except Exception as e:
                        print(f"[!] Errore nella creazione dell'immagine combinata: {e}")
                        # Se fallisce, restituisci solo il primo logo trovato
                        return logo1_url

                # Se non abbiamo trovato entrambi i loghi, restituisci quello che abbiamo
                return logo1_url or logo2_url

            if ':' in event_name:
                # Usa la parte prima dei ":" per la ricerca
                prefix_name = event_name.split(':', 1)[0].strip()
                print(f"[🔍] Tentativo ricerca logo con prefisso: {prefix_name}")

                # Prepara la query di ricerca con il prefisso
                search_query = urllib.parse.quote(f"{prefix_name} logo")

                # Utilizziamo l'API di Bing Image Search con parametri migliorati
                search_url = f"https://www.bing.com/images/search?q={search_query}&qft=+filterui:photo-transparent+filterui:aspect-square&form=IRFLTR"

                headers = { 
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36",
                    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
                    "Accept-Language": "it-IT,it;q=0.9,en-US;q=0.8,en;q=0.7",
                    "Cache-Control": "max-age=0",
                    "Connection": "keep-alive"
                } 

                response = requests.get(search_url, headers=headers, timeout=10)

                if response.status_code == 200: 
                    # Metodo 1: Cerca pattern per murl (URL dell'immagine media)
                    patterns = [
                        r'murl&quot;:&quot;(https?://[^&]+)&quot;',
                        r'"murl":"(https?://[^"]+)"',
                        r'"contentUrl":"(https?://[^"]+\.(?:png|jpg|jpeg|svg))"',
                        r'<img[^>]+src="(https?://[^"]+\.(?:png|jpg|jpeg|svg))[^>]+class="mimg"',
                        r'<a[^>]+class="iusc"[^>]+m=\'{"[^"]*":"[^"]*","[^"]*":"(https?://[^"]+)"'
                    ]

                    for pattern in patterns:
                        matches = re.findall(pattern, response.text)
                        if matches and len(matches) > 0:
                            # Prendi il primo risultato che sembra un logo (preferibilmente PNG o SVG)
                            for match in matches:
                                if '.png' in match.lower() or '.svg' in match.lower():
                                    print(f"[✓] Logo trovato con prefisso: {match}")
                                    return match
                            # Se non troviamo PNG o SVG, prendi il primo risultato
                            print(f"[✓] Logo trovato con prefisso: {matches[0]}")
                            return matches[0]

            # Se non riusciamo a identificare le squadre e il prefisso non ha dato risultati, procedi con la ricerca normale
            print(f"[🔍] Ricerca standard per: {clean_event_name}")

            # Se non riusciamo a identificare le squadre, procedi con la ricerca normale
            # Prepara la query di ricerca piÃ¹ specifica
            search_query = urllib.parse.quote(f"{clean_event_name} logo")

            # Utilizziamo l'API di Bing Image Search con parametri migliorati
            search_url = f"https://www.bing.com/images/search?q={search_query}&qft=+filterui:photo-transparent+filterui:aspect-square&form=IRFLTR"

            headers = { 
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
                "Accept-Language": "it-IT,it;q=0.9,en-US;q=0.8,en;q=0.7",
                "Cache-Control": "max-age=0",
                "Connection": "keep-alive"
            } 

            response = requests.get(search_url, headers=headers, timeout=10)

            if response.status_code == 200: 
                # Metodo 1: Cerca pattern per murl (URL dell'immagine media)
                patterns = [
                    r'murl&quot;:&quot;(https?://[^&]+)&quot;',
                    r'"murl":"(https?://[^"]+)"',
                    r'"contentUrl":"(https?://[^"]+\.(?:png|jpg|jpeg|svg))"',
                    r'<img[^>]+src="(https?://[^"]+\.(?:png|jpg|jpeg|svg))[^>]+class="mimg"',
                    r'<a[^>]+class="iusc"[^>]+m=\'{"[^"]*":"[^"]*","[^"]*":"(https?://[^"]+)"'
                ]

                for pattern in patterns:
                    matches = re.findall(pattern, response.text)
                    if matches and len(matches) > 0:
                        # Prendi il primo risultato che sembra un logo (preferibilmente PNG o SVG)
                        for match in matches:
                            if '.png' in match.lower() or '.svg' in match.lower():
                                return match
                        # Se non troviamo PNG o SVG, prendi il primo risultato
                        return matches[0]

                # Metodo alternativo: cerca JSON incorporato nella pagina
                json_match = re.search(r'var\s+IG\s*=\s*(\{.+?\});\s*', response.text)
                if json_match:
                    try:
                        # Estrai e analizza il JSON
                        json_str = json_match.group(1)
                        # Pulisci il JSON se necessario
                        json_str = re.sub(r'([{,])\s*([a-zA-Z0-9_]+):', r'\1"\2":', json_str)
                        data = json.loads(json_str)

                        # Cerca URL di immagini nel JSON
                        if 'images' in data and len(data['images']) > 0:
                            for img in data['images']:
                                if 'murl' in img:
                                    return img['murl']
                    except Exception as e:
                        print(f"[!] Errore nell'analisi JSON: {e}")

                print(f"[!] Nessun logo trovato per '{clean_event_name}' con i pattern standard")

                # Ultimo tentativo: cerca qualsiasi URL di immagine nella pagina
                any_img = re.search(r'(https?://[^"\']+\.(?:png|jpg|jpeg|svg|webp))', response.text)
                if any_img:
                    return any_img.group(1)

        except Exception as e: 
            print(f"[!] Errore nella ricerca del logo per '{event_name}': {e}") 

        # Se non troviamo nulla, restituiamo None 
        return None

    def search_team_logo(team_name):
        """
        Funzione dedicata alla ricerca del logo di una singola squadra
        """
        try:
            # Prepara la query di ricerca specifica per la squadra
            search_query = urllib.parse.quote(f"{team_name} logo")

            # Utilizziamo l'API di Bing Image Search con parametri migliorati
            search_url = f"https://www.bing.com/images/search?q={search_query}&qft=+filterui:photo-transparent+filterui:aspect-square&form=IRFLTR"

            headers = { 
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
                "Accept-Language": "it-IT,it;q=0.9,en-US;q=0.8,en;q=0.7",
                "Cache-Control": "max-age=0",
                "Connection": "keep-alive"
            } 

            response = requests.get(search_url, headers=headers, timeout=10)

            if response.status_code == 200: 
                # Metodo 1: Cerca pattern per murl (URL dell'immagine media)
                patterns = [
                    r'murl&quot;:&quot;(https?://[^&]+)&quot;',
                    r'"murl":"(https?://[^"]+)"',
                    r'"contentUrl":"(https?://[^"]+\.(?:png|jpg|jpeg|svg))"',
                    r'<img[^>]+src="(https?://[^"]+\.(?:png|jpg|jpeg|svg))[^>]+class="mimg"',
                    r'<a[^>]+class="iusc"[^>]+m=\'{"[^"]*":"[^"]*","[^"]*":"(https?://[^"]+)"'
                ]

                for pattern in patterns:
                    matches = re.findall(pattern, response.text)
                    if matches and len(matches) > 0:
                        # Prendi il primo risultato che sembra un logo (preferibilmente PNG o SVG)
                        for match in matches:
                            if '.png' in match.lower() or '.svg' in match.lower():
                                return match
                        # Se non troviamo PNG o SVG, prendi il primo risultato
                        return matches[0]

                # Metodo alternativo: cerca JSON incorporato nella pagina
                json_match = re.search(r'var\s+IG\s*=\s*(\{.+?\});\s*', response.text)
                if json_match:
                    try:
                        # Estrai e analizza il JSON
                        json_str = json_match.group(1)
                        # Pulisci il JSON se necessario
                        json_str = re.sub(r'([{,])\s*([a-zA-Z0-9_]+):', r'\1"\2":', json_str)
                        data = json.loads(json_str)

                        # Cerca URL di immagini nel JSON
                        if 'images' in data and len(data['images']) > 0:
                            for img in data['images']:
                                if 'murl' in img:
                                    return img['murl']
                    except Exception as e:
                        print(f"[!] Errore nell'analisi JSON: {e}")

                print(f"[!] Nessun logo trovato per '{team_name}' con i pattern standard")

                # Ultimo tentativo: cerca qualsiasi URL di immagine nella pagina
                any_img = re.search(r'(https?://[^"\']+\.(?:png|jpg|jpeg|svg|webp))', response.text)
                if any_img:
                    return any_img.group(1)

        except Exception as e: 
            print(f"[!] Errore nella ricerca del logo per '{team_name}': {e}") 

        # Se non troviamo nulla, restituiamo None 
        return None

    def extract_channels_from_json(path): 
        keywords = {"italy", "rai", "italia", "it"} 
        now = datetime.now() 

        with open(path, "r", encoding="utf-8") as f: 
            data = json.load(f) 

        categorized_channels = {} 

        for date_key, sections in data.items(): 
            date_part = date_key.split(" - ")[0] 
            try: 
                date_obj = parser.parse(date_part, fuzzy=True).date() 
            except Exception as e: 
                print(f"[!] Errore parsing data '{date_part}': {e}") 
                continue 

            if date_obj != now.date(): 
                continue 

            date_str = date_obj.strftime("%Y-%m-%d") 

            for category_raw, event_items in sections.items(): 
                category = clean_category_name(category_raw) 
                if category not in categorized_channels: 
                    categorized_channels[category] = [] 

                for item in event_items: 
                    time_str = item.get("time", "00:00") 
                    try: 
                        time_obj = datetime.strptime(time_str, "%H:%M") + timedelta(hours=2) 
                        event_datetime = datetime.combine(date_obj, time_obj.time()) 

                        if now - event_datetime > timedelta(hours=2): 
                            continue 

                        time_formatted = time_obj.strftime("%H:%M") 
                    except Exception: 
                        time_formatted = time_str 

                    event_title = item.get("event", "Evento") 

                    for ch in item.get("channels", []): 
                        channel_name = ch.get("channel_name", "") 
                        channel_id = ch.get("channel_id", "") 

                        words = set(re.findall(r'\b\w+\b', channel_name.lower())) 
                        if keywords.intersection(words): 
                            tvg_name = f"{event_title} ({time_formatted})" 
                            categorized_channels[category].append({ 
                                "tvg_name": tvg_name, 
                                "channel_name": channel_name, 
                                "channel_id": channel_id, 
                                "event_title": event_title  # Aggiungiamo il titolo dell'evento per la ricerca del logo 
                            }) 

        return categorized_channels 

    def generate_m3u_from_schedule(json_file, output_file): 
        categorized_channels = extract_channels_from_json(json_file) 

        with open(output_file, "w", encoding="utf-8") as f: 
            f.write("#EXTM3U\n") 

            for category, channels in categorized_channels.items(): 
                if not channels: 
                    continue 

                f.write(f'#EXTINF:-1 tvg-name="{category}" group-title="Eventi Live",--- {category} ---\nhttps://example.m3u8\n\n') 

                for ch in channels: 
                    tvg_name = ch["tvg_name"] 
                    channel_id = ch["channel_id"] 
                    event_title = ch["event_title"] 

                    # Cerca un logo per questo evento
                    clean_event_title = re.sub(r'\s*\(\d{1,2}:\d{2}\)\s*$', '', event_title)
                    print(f"[🔍] Ricerca logo per: {clean_event_title}")
                    logo_url = search_logo_for_event(clean_event_title) 
                    logo_attribute = f' tvg-logo="{logo_url}"' if logo_url else '' 

                    # Applica la pulizia al tvg-id
                    tvg_id_cleaned = clean_tvg_id(clean_event_title)

                    stream_url = (f"{PROXY}{LINK_DADDY}/embed/stream-{channel_id}.php")                    
                    f.write(f'#EXTINF:-1 tvg-id="{tvg_id_cleaned}" tvg-name="{tvg_name}"{logo_attribute} group-title="Eventi Live",{tvg_name}\n{stream_url}\n\n')
                    print(f"[✓] {tvg_name}" + (f" (logo trovato)" if logo_url else " (nessun logo trovato)"))

    if __name__ == "__main__": 
        # Assicurati che il modulo requests sia installato 
        try: 
            import requests 
        except ImportError: 
            print("[!] Il modulo 'requests' non Ã¨ installato. Installalo con 'pip install requests'") 
            exit(1) 

        generate_m3u_from_schedule(JSON_FILE, OUTPUT_FILE) 

# Funzione per il quarto script (schedule_extractor.py)
def schedule_extractor():
    # Codice del quarto script qui
    # Aggiungi il codice del tuo script "schedule_extractor.py" in questa funzione.
    print("Eseguendo lo schedule_extractor.py...")
    # Il codice che avevi nello script "schedule_extractor.py" va qui, senza modifiche.
    from playwright.sync_api import sync_playwright
    import os
    import json
    from datetime import datetime
    import re
    from bs4 import BeautifulSoup
    from dotenv import load_dotenv

    # Carica le variabili d'ambiente dal file .env
    load_dotenv()

    LINK_DADDY = os.getenv("LINK_DADDY", "https://daddylive.dad").strip()

    def html_to_json(html_content):
        soup = BeautifulSoup(html_content, 'html.parser')
        result = {}

        date_rows = soup.find_all('tr', class_='date-row')
        if not date_rows:
            print("AVVISO: Nessuna riga di data trovata nel contenuto HTML!")
            return {}

        current_date = None
        current_category = None

        for row in soup.find_all('tr'):
            if 'date-row' in row.get('class', []):
                current_date = row.find('strong').text.strip()
                result[current_date] = {}
                current_category = None

            elif 'category-row' in row.get('class', []) and current_date:
                current_category = row.find('strong').text.strip() + "</span>"
                result[current_date][current_category] = []

            elif 'event-row' in row.get('class', []) and current_date and current_category:
                time_div = row.find('div', class_='event-time')
                info_div = row.find('div', class_='event-info')

                if not time_div or not info_div:
                    continue

                time_strong = time_div.find('strong')
                event_time = time_strong.text.strip() if time_strong else ""
                event_info = info_div.text.strip()

                event_data = {
                    "time": event_time,
                    "event": event_info,
                    "channels": []
                }

                # Cerca la riga dei canali successiva
                next_row = row.find_next_sibling('tr')
                if next_row and 'channel-row' in next_row.get('class', []):
                    channel_links = next_row.find_all('a', class_='channel-button-small')
                    for link in channel_links:
                        href = link.get('href', '')
                        channel_id_match = re.search(r'stream-(\d+)\.php', href)
                        if channel_id_match:
                            channel_id = channel_id_match.group(1)
                            channel_name = link.text.strip()
                            channel_name = re.sub(r'\s*\(CH-\d+\)$', '', channel_name)

                            event_data["channels"].append({
                                "channel_name": channel_name,
                                "channel_id": channel_id
                            })

                result[current_date][current_category].append(event_data)

        return result

    def modify_json_file(json_file_path):
        with open(json_file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        current_month = datetime.now().strftime("%B")

        for date in list(data.keys()):
            match = re.match(r"(\w+\s\d+)(st|nd|rd|th)\s(\d{4})", date)
            if match:
                day_part = match.group(1)
                suffix = match.group(2)
                year_part = match.group(3)
                new_date = f"{day_part}{suffix} {current_month} {year_part}"
                data[new_date] = data.pop(date)

        with open(json_file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)

        print(f"File JSON modificato e salvato in {json_file_path}")

    def extract_schedule_container():
        url = f"{LINK_DADDY}/"

        script_dir = os.path.dirname(os.path.abspath(__file__))
        json_output = os.path.join(script_dir, "daddyliveSchedule.json")

        print(f"Accesso alla pagina {url} per estrarre il main-schedule-container...")

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context(
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0 Safari/537.36"
            )
            page = context.new_page()

            max_attempts = 3
            for attempt in range(1, max_attempts + 1):
                try:
                    print(f"Tentativo {attempt} di {max_attempts}...")
                    page.goto(url)
                    print("Attesa per il caricamento completo...")
                    page.wait_for_timeout(10000)  # 10 secondi

                    schedule_content = page.evaluate("""() => {
                        const container = document.getElementById('main-schedule-container');
                        return container ? container.outerHTML : '';
                    }""")

                    if not schedule_content:
                        print("AVVISO: main-schedule-container non trovato o vuoto!")
                        if attempt == max_attempts:
                            browser.close()
                            return False
                        else:
                            continue

                    print("Conversione HTML in formato JSON...")
                    json_data = html_to_json(schedule_content)

                    with open(json_output, "w", encoding="utf-8") as f:
                        json.dump(json_data, f, indent=4)

                    print(f"Dati JSON salvati in {json_output}")

                    modify_json_file(json_output)
                    browser.close()
                    return True

                except Exception as e:
                    print(f"ERRORE nel tentativo {attempt}: {str(e)}")
                    if attempt == max_attempts:
                        print("Tutti i tentativi falliti!")
                        browser.close()
                        return False
                    else:
                        print(f"Riprovando... (tentativo {attempt + 1} di {max_attempts})")

            browser.close()
            return False

    if __name__ == "__main__":
        success = extract_schedule_container()
        if not success:
            exit(1)

def epg_eventi_generator_world():
    # Codice del quinto script qui
    # Aggiungi il codice del tuo script "epg_eventi_generator.py" in questa funzione.
    print("Eseguendo l'epg_eventi_generator_world.py...")
    # Il codice che avevi nello script "epg_eventi_generator.py" va qui, senza modifiche.
    import os
    import re
    import json
    from datetime import datetime, timedelta

    # Funzione di utilitÃ  per pulire il testo (rimuovere tag HTML span)
    def clean_text(text):
        return re.sub(r'</?span.*?>', '', str(text))

    # Funzione di utilitÃ  per pulire il Channel ID (rimuovere spazi e caratteri speciali)
    def clean_channel_id(text):
        """Rimuove caratteri speciali e spazi dal channel ID lasciando tutto attaccato"""
        # Rimuovi prima i tag HTML
        text = clean_text(text)
        # Rimuovi tutti gli spazi
        text = re.sub(r'\s+', '', text)
        # Mantieni solo caratteri alfanumerici (rimuovi tutto il resto)
        text = re.sub(r'[^a-zA-Z0-9]', '', text)
        # Assicurati che non sia vuoto
        if not text:
            text = "unknownchannel"
        return text

    # --- SCRIPT 5: epg_eventi_xml_generator (genera eventi.xml) ---
    def load_json_for_epg(json_file_path):
        """Carica e filtra i dati JSON per la generazione EPG"""
        if not os.path.exists(json_file_path):
            print(f"[!] File JSON non trovato per EPG: {json_file_path}")
            return {}

        try:
            with open(json_file_path, "r", encoding="utf-8") as file:
                json_data = json.load(file)
        except json.JSONDecodeError as e:
            print(f"[!] Errore nel parsing del file JSON: {e}")
            return {}
        except Exception as e:
            print(f"[!] Errore nell'apertura del file JSON: {e}")
            return {}

        # Lista delle parole chiave per canali italiani
        keywords = ['italy', 'rai', 'italia', 'it', 'uk', 'tnt', 'usa', 'tennis channel', 'tennis stream', 'la']

        filtered_data = {}
        for date, categories in json_data.items():
            filtered_categories = {}
            for category, events in categories.items():
                filtered_events = []
                for event_info in events: # Original loop for events
                    # Filtra gli eventi in base all'orario specificato (00:00 - 04:00)
                    event_time_str = event_info.get("time", "00:00") # Prende l'orario dell'evento, default a "00:00" se mancante
                    try:
                        event_actual_time = datetime.strptime(event_time_str, "%H:%M").time()

                        # Definisci gli orari limite per il filtro
                        filter_start_time = datetime.strptime("00:00", "%H:%M").time()
                        filter_end_time = datetime.strptime("04:00", "%H:%M").time()

                        # Escludi eventi se l'orario Ã¨ compreso tra 00:00 e 04:00 inclusi
                        if filter_start_time <= event_actual_time <= filter_end_time:
                            continue # Salta questo evento e passa al successivo
                    except ValueError:
                        print(f"[!] Orario evento non valido '{event_time_str}' per l'evento '{event_info.get('event', 'Sconosciuto')}' durante il caricamento JSON. Evento saltato.")
                        continue

                    filtered_channels = []
                    # Utilizza .get("channels", []) per gestire casi in cui "channels" potrebbe mancare
                    for channel in event_info.get("channels", []): 
                        channel_name = clean_text(channel.get("channel_name", "")) # Usa .get per sicurezza

                        # Filtra per canali italiani - solo parole intere
                        channel_words = channel_name.lower().split()
                        if any(word in keywords for word in channel_words):
                            filtered_channels.append(channel)

                    if filtered_channels:
                        # Assicura che event_info sia un dizionario prima dello unpacking
                        if isinstance(event_info, dict):
                            filtered_events.append({**event_info, "channels": filtered_channels})
                        else:
                            # Logga un avviso se il formato dell'evento non Ã¨ quello atteso
                            print(f"[!] Formato evento non valido durante il filtraggio per EPG: {event_info}")

                if filtered_events:
                    filtered_categories[category] = filtered_events

            if filtered_categories:
                filtered_data[date] = filtered_categories

        return filtered_data

    def generate_epg_xml(json_data):
        """Genera il contenuto XML EPG dai dati JSON filtrati"""
        epg_content = '<?xml version="1.0" encoding="UTF-8"?>\n<tv>\n'

        italian_offset = timedelta(hours=2)
        italian_offset_str = "+0200" 

        current_datetime_utc = datetime.utcnow()
        current_datetime_local = current_datetime_utc + italian_offset

        # Tiene traccia degli ID dei canali per cui Ã¨ giÃ  stato scritto il tag <channel>
        channel_ids_processed_for_channel_tag = set() 

        for date_key, categories in json_data.items():
            # Dizionario per memorizzare l'ora di fine dell'ultimo evento per ciascun canale IN QUESTA DATA SPECIFICA
            # Viene resettato per ogni nuova data.
            last_event_end_time_per_channel_on_date = {}

            try:
                date_str_from_key = date_key.split(' - ')[0]
                date_str_cleaned = re.sub(r'(\d+)(st|nd|rd|th)', r'\1', date_str_from_key)
                event_date_part = datetime.strptime(date_str_cleaned, "%A %d %B %Y").date()
            except ValueError as e:
                print(f"[!] Errore nel parsing della data EPG: '{date_str_from_key}'. Errore: {e}")
                continue
            except IndexError as e:
                print(f"[!] Formato data non valido: '{date_key}'. Errore: {e}")
                continue

            if event_date_part < current_datetime_local.date():
                continue

            for category_name, events_list in categories.items():
                # Ordina gli eventi per orario di inizio (UTC) per garantire la corretta logica "evento precedente"
                try:
                    sorted_events_list = sorted(
                        events_list,
                        key=lambda x: datetime.strptime(x.get("time", "00:00"), "%H:%M").time()
                    )
                except Exception as e_sort:
                    print(f"[!] Attenzione: Impossibile ordinare gli eventi per la categoria '{category_name}' nella data '{date_key}'. Si procede senza ordinamento. Errore: {e_sort}")
                    sorted_events_list = events_list

                for event_info in sorted_events_list:
                    time_str_utc = event_info.get("time", "00:00")
                    event_name_original = clean_text(event_info.get("event", "Evento Sconosciuto"))
                    event_name = event_name_original.replace('&', 'and')
                    event_desc = event_info.get("description", f"Trasmesso in diretta.")

                    # USA EVENT NAME COME CHANNEL ID - PULITO DA CARATTERI SPECIALI E SPAZI
                    channel_id = clean_channel_id(event_name)

                    try:
                        event_time_utc_obj = datetime.strptime(time_str_utc, "%H:%M").time()
                        event_datetime_utc = datetime.combine(event_date_part, event_time_utc_obj)
                        event_datetime_local = event_datetime_utc + italian_offset
                    except ValueError as e:
                        print(f"[!] Errore parsing orario UTC '{time_str_utc}' per EPG evento '{event_name}'. Errore: {e}")
                        continue

                    if event_datetime_local < (current_datetime_local - timedelta(hours=2)):
                        continue

                    # Verifica che ci siano canali disponibili
                    channels_list = event_info.get("channels", [])
                    if not channels_list:
                        print(f"[!] Nessun canale disponibile per l'evento '{event_name}'")
                        continue

                    for channel_data in channels_list:
                        if not isinstance(channel_data, dict):
                            print(f"[!] Formato canale non valido per l'evento '{event_name}': {channel_data}")
                            continue

                        channel_name_cleaned = clean_text(channel_data.get("channel_name", "Canale Sconosciuto"))

                        # Crea tag <channel> se non giÃ  processato
                        if channel_id not in channel_ids_processed_for_channel_tag:
                            epg_content += f'  <channel id="{channel_id}">\n'
                            epg_content += f'    <display-name>{event_name}</display-name>\n'
                            epg_content += f'  </channel>\n'
                            channel_ids_processed_for_channel_tag.add(channel_id)

                        # --- LOGICA ANNUNCIO MODIFICATA ---
                        announcement_stop_local = event_datetime_local # L'annuncio termina quando inizia l'evento corrente

                        # Determina l'inizio dell'annuncio
                        if channel_id in last_event_end_time_per_channel_on_date:
                            # C'Ã¨ stato un evento precedente su questo canale in questa data
                            previous_event_end_time_local = last_event_end_time_per_channel_on_date[channel_id]

                            # Assicurati che l'evento precedente termini prima che inizi quello corrente
                            if previous_event_end_time_local < event_datetime_local:
                                announcement_start_local = previous_event_end_time_local
                            else:
                                # Sovrapposizione o stesso orario di inizio, problematico.
                                # Fallback a 00:00 del giorno, o potresti saltare l'annuncio.
                                print(f"[!] Attenzione: L'evento '{event_name}' inizia prima o contemporaneamente alla fine dell'evento precedente su questo canale. Fallback per l'inizio dell'annuncio.")
                                announcement_start_local = datetime.combine(event_datetime_local.date(), datetime.min.time())
                        else:
                            # Primo evento per questo canale in questa data
                            announcement_start_local = datetime.combine(event_datetime_local.date(), datetime.min.time()) # 00:00 ora italiana

                        # Assicura che l'inizio dell'annuncio sia prima della fine
                        if announcement_start_local < announcement_stop_local:
                            announcement_title = f'Inizia  alle {event_datetime_local.strftime("%H:%M")}.' # Orario italiano

                            epg_content += f'  <programme start="{announcement_start_local.strftime("%Y%m%d%H%M%S")} {italian_offset_str}" stop="{announcement_stop_local.strftime("%Y%m%d%H%M%S")} {italian_offset_str}" channel="{channel_id}">\n'
                            epg_content += f'    <title lang="it">{announcement_title}</title>\n'
                            epg_content += f'    <desc lang="it">{event_name}.</desc>\n' 
                            epg_content += f'    <category lang="it">Annuncio</category>\n'
                            epg_content += f'  </programme>\n'
                        elif announcement_start_local == announcement_stop_local:
                            print(f"[INFO] Annuncio di durata zero saltato per l'evento '{event_name}' sul canale '{channel_id}'.")
                        else: # announcement_start_local > announcement_stop_local
                            print(f"[!] Attenzione: L'orario di inizio calcolato per l'annuncio Ã¨ successivo all'orario di fine per l'evento '{event_name}' sul canale '{channel_id}'. Annuncio saltato.")

                        # --- EVENTO PRINCIPALE ---
                        main_event_start_local = event_datetime_local 
                        main_event_stop_local = event_datetime_local + timedelta(hours=2) # Durata fissa 2 ore

                        epg_content += f'  <programme start="{main_event_start_local.strftime("%Y%m%d%H%M%S")} {italian_offset_str}" stop="{main_event_stop_local.strftime("%Y%m%d%H%M%S")} {italian_offset_str}" channel="{channel_id}">\n'
                        epg_content += f'    <title lang="it">{event_desc}</title>\n'
                        epg_content += f'    <desc lang="it">{event_name}</desc>\n'
                        epg_content += f'    <category lang="it">{clean_text(category_name)}</category>\n'
                        epg_content += f'  </programme>\n'

                        # Aggiorna l'orario di fine dell'ultimo evento per questo canale in questa data
                        last_event_end_time_per_channel_on_date[channel_id] = main_event_stop_local

        epg_content += "</tv>\n"
        return epg_content

    def save_epg_xml(epg_content, output_file_path):
        """Salva il contenuto EPG XML su file"""
        try:
            with open(output_file_path, "w", encoding="utf-8") as file:
                file.write(epg_content)
            print(f"[✓] File EPG XML salvato con successo: {output_file_path}")
            return True
        except Exception as e:
            print(f"[!] Errore nel salvataggio del file EPG XML: {e}")
            return False

    def main_epg_generator(json_file_path, output_file_path="eventi.xml"):
        """Funzione principale per generare l'EPG XML"""
        print(f"[INFO] Inizio generazione EPG XML da: {json_file_path}")

        # Carica e filtra i dati JSON
        json_data = load_json_for_epg(json_file_path)

        if not json_data:
            print("[!] Nessun dato valido trovato nel file JSON.")
            return False

        print(f"[INFO] Dati caricati per {len(json_data)} date")

        # Genera il contenuto XML EPG
        epg_content = generate_epg_xml(json_data)

        # Salva il file XML
        success = save_epg_xml(epg_content, output_file_path)

        if success:
            print(f"[✓] Generazione EPG XML completata con successo!")
            return True
        else:
            print(f"[!] Errore durante la generazione EPG XML.")
            return False

    # Esempio di utilizzo
    if __name__ == "__main__":
        # Percorso del file JSON di input
        input_json_path = "daddyliveSchedule.json"  # Modifica con il tuo percorso

        # Percorso del file XML di output
        output_xml_path = "eventi.xml"

        # Esegui la generazione EPG
        main_epg_generator(input_json_path, output_xml_path)

# Funzione per il quinto script (epg_eventi_generator.py)
def epg_eventi_generator():
    # Codice del quinto script qui
    # Aggiungi il codice del tuo script "epg_eventi_generator.py" in questa funzione.
    print("Eseguendo l'epg_eventi_generator.py...")
    # Il codice che avevi nello script "epg_eventi_generator.py" va qui, senza modifiche.
    import os
    import re
    import json
    from datetime import datetime, timedelta

    # Funzione di utilitÃ  per pulire il testo (rimuovere tag HTML span)
    def clean_text(text):
        return re.sub(r'</?span.*?>', '', str(text))

    # Funzione di utilitÃ  per pulire il Channel ID (rimuovere spazi e caratteri speciali)
    def clean_channel_id(text):
        """Rimuove caratteri speciali e spazi dal channel ID lasciando tutto attaccato"""
        # Rimuovi prima i tag HTML
        text = clean_text(text)
        # Rimuovi tutti gli spazi
        text = re.sub(r'\s+', '', text)
        # Mantieni solo caratteri alfanumerici (rimuovi tutto il resto)
        text = re.sub(r'[^a-zA-Z0-9]', '', text)
        # Assicurati che non sia vuoto
        if not text:
            text = "unknownchannel"
        return text

    # --- SCRIPT 5: epg_eventi_xml_generator (genera eventi.xml) ---
    def load_json_for_epg(json_file_path):
        """Carica e filtra i dati JSON per la generazione EPG"""
        if not os.path.exists(json_file_path):
            print(f"[!] File JSON non trovato per EPG: {json_file_path}")
            return {}

        try:
            with open(json_file_path, "r", encoding="utf-8") as file:
                json_data = json.load(file)
        except json.JSONDecodeError as e:
            print(f"[!] Errore nel parsing del file JSON: {e}")
            return {}
        except Exception as e:
            print(f"[!] Errore nell'apertura del file JSON: {e}")
            return {}

        # Lista delle parole chiave per canali italiani
        keywords = ['italy', 'rai', 'italia', 'it']

        filtered_data = {}
        for date, categories in json_data.items():
            filtered_categories = {}
            for category, events in categories.items():
                filtered_events = []
                for event_info in events:
                    filtered_channels = []
                    # Utilizza .get("channels", []) per gestire casi in cui "channels" potrebbe mancare
                    for channel in event_info.get("channels", []): 
                        channel_name = clean_text(channel.get("channel_name", "")) # Usa .get per sicurezza

                        # Filtra per canali italiani - solo parole intere
                        channel_words = channel_name.lower().split()
                        if any(word in keywords for word in channel_words):
                            filtered_channels.append(channel)

                    if filtered_channels:
                        # Assicura che event_info sia un dizionario prima dello unpacking
                        if isinstance(event_info, dict):
                            filtered_events.append({**event_info, "channels": filtered_channels})
                        else:
                            # Logga un avviso se il formato dell'evento non Ã¨ quello atteso
                            print(f"[!] Formato evento non valido durante il filtraggio per EPG: {event_info}")

                if filtered_events:
                    filtered_categories[category] = filtered_events

            if filtered_categories:
                filtered_data[date] = filtered_categories

        return filtered_data

    def generate_epg_xml(json_data):
        """Genera il contenuto XML EPG dai dati JSON filtrati"""
        epg_content = '<?xml version="1.0" encoding="UTF-8"?>\n<tv>\n'

        italian_offset = timedelta(hours=2)
        italian_offset_str = "+0200" 

        current_datetime_utc = datetime.utcnow()
        current_datetime_local = current_datetime_utc + italian_offset

        # Tiene traccia degli ID dei canali per cui Ã¨ giÃ  stato scritto il tag <channel>
        channel_ids_processed_for_channel_tag = set() 

        for date_key, categories in json_data.items():
            # Dizionario per memorizzare l'ora di fine dell'ultimo evento per ciascun canale IN QUESTA DATA SPECIFICA
            # Viene resettato per ogni nuova data.
            last_event_end_time_per_channel_on_date = {}

            try:
                date_str_from_key = date_key.split(' - ')[0]
                date_str_cleaned = re.sub(r'(\d+)(st|nd|rd|th)', r'\1', date_str_from_key)
                event_date_part = datetime.strptime(date_str_cleaned, "%A %d %B %Y").date()
            except ValueError as e:
                print(f"[!] Errore nel parsing della data EPG: '{date_str_from_key}'. Errore: {e}")
                continue
            except IndexError as e:
                print(f"[!] Formato data non valido: '{date_key}'. Errore: {e}")
                continue

            if event_date_part < current_datetime_local.date():
                continue

            for category_name, events_list in categories.items():
                # Ordina gli eventi per orario di inizio (UTC) per garantire la corretta logica "evento precedente"
                try:
                    sorted_events_list = sorted(
                        events_list,
                        key=lambda x: datetime.strptime(x.get("time", "00:00"), "%H:%M").time()
                    )
                except Exception as e_sort:
                    print(f"[!] Attenzione: Impossibile ordinare gli eventi per la categoria '{category_name}' nella data '{date_key}'. Si procede senza ordinamento. Errore: {e_sort}")
                    sorted_events_list = events_list

                for event_info in sorted_events_list:
                    time_str_utc = event_info.get("time", "00:00")
                    event_name = clean_text(event_info.get("event", "Evento Sconosciuto"))
                    event_desc = event_info.get("description", f"Trasmesso in diretta.")

                    # USA EVENT NAME COME CHANNEL ID - PULITO DA CARATTERI SPECIALI E SPAZI
                    channel_id = clean_channel_id(event_name)

                    try:
                        event_time_utc_obj = datetime.strptime(time_str_utc, "%H:%M").time()
                        event_datetime_utc = datetime.combine(event_date_part, event_time_utc_obj)
                        event_datetime_local = event_datetime_utc + italian_offset
                    except ValueError as e:
                        print(f"[!] Errore parsing orario UTC '{time_str_utc}' per EPG evento '{event_name}'. Errore: {e}")
                        continue

                    if event_datetime_local < (current_datetime_local - timedelta(hours=2)):
                        continue

                    # Verifica che ci siano canali disponibili
                    channels_list = event_info.get("channels", [])
                    if not channels_list:
                        print(f"[!] Nessun canale disponibile per l'evento '{event_name}'")
                        continue

                    for channel_data in channels_list:
                        if not isinstance(channel_data, dict):
                            print(f"[!] Formato canale non valido per l'evento '{event_name}': {channel_data}")
                            continue

                        channel_name_cleaned = clean_text(channel_data.get("channel_name", "Canale Sconosciuto"))

                        # Crea tag <channel> se non giÃ  processato
                        if channel_id not in channel_ids_processed_for_channel_tag:
                            epg_content += f'  <channel id="{channel_id}">\n'
                            epg_content += f'    <display-name>{event_name}</display-name>\n'
                            epg_content += f'  </channel>\n'
                            channel_ids_processed_for_channel_tag.add(channel_id)

                        # --- LOGICA ANNUNCIO MODIFICATA ---
                        announcement_stop_local = event_datetime_local # L'annuncio termina quando inizia l'evento corrente

                        # Determina l'inizio dell'annuncio
                        if channel_id in last_event_end_time_per_channel_on_date:
                            # C'Ã¨ stato un evento precedente su questo canale in questa data
                            previous_event_end_time_local = last_event_end_time_per_channel_on_date[channel_id]

                            # Assicurati che l'evento precedente termini prima che inizi quello corrente
                            if previous_event_end_time_local < event_datetime_local:
                                announcement_start_local = previous_event_end_time_local
                            else:
                                # Sovrapposizione o stesso orario di inizio, problematico.
                                # Fallback a 00:00 del giorno, o potresti saltare l'annuncio.
                                print(f"[!] Attenzione: L'evento '{event_name}' inizia prima o contemporaneamente alla fine dell'evento precedente su questo canale. Fallback per l'inizio dell'annuncio.")
                                announcement_start_local = datetime.combine(event_datetime_local.date(), datetime.min.time())
                        else:
                            # Primo evento per questo canale in questa data
                            announcement_start_local = datetime.combine(event_datetime_local.date(), datetime.min.time()) # 00:00 ora italiana

                        # Assicura che l'inizio dell'annuncio sia prima della fine
                        if announcement_start_local < announcement_stop_local:
                            announcement_title = f'Inizia  alle {event_datetime_local.strftime("%H:%M")}.' # Orario italiano

                            epg_content += f'  <programme start="{announcement_start_local.strftime("%Y%m%d%H%M%S")} {italian_offset_str}" stop="{announcement_stop_local.strftime("%Y%m%d%H%M%S")} {italian_offset_str}" channel="{channel_id}">\n'
                            epg_content += f'    <title lang="it">{announcement_title}</title>\n'
                            epg_content += f'    <desc lang="it">{event_name}.</desc>\n' 
                            epg_content += f'    <category lang="it">Annuncio</category>\n'
                            epg_content += f'  </programme>\n'
                        elif announcement_start_local == announcement_stop_local:
                            print(f"[INFO] Annuncio di durata zero saltato per l'evento '{event_name}' sul canale '{channel_id}'.")
                        else: # announcement_start_local > announcement_stop_local
                            print(f"[!] Attenzione: L'orario di inizio calcolato per l'annuncio Ã¨ successivo all'orario di fine per l'evento '{event_name}' sul canale '{channel_id}'. Annuncio saltato.")

                        # --- EVENTO PRINCIPALE ---
                        main_event_start_local = event_datetime_local 
                        main_event_stop_local = event_datetime_local + timedelta(hours=2) # Durata fissa 2 ore

                        epg_content += f'  <programme start="{main_event_start_local.strftime("%Y%m%d%H%M%S")} {italian_offset_str}" stop="{main_event_stop_local.strftime("%Y%m%d%H%M%S")} {italian_offset_str}" channel="{channel_id}">\n'
                        epg_content += f'    <title lang="it">{event_desc}</title>\n'
                        epg_content += f'    <desc lang="it">{event_name}</desc>\n'
                        epg_content += f'    <category lang="it">{clean_text(category_name)}</category>\n'
                        epg_content += f'  </programme>\n'

                        # Aggiorna l'orario di fine dell'ultimo evento per questo canale in questa data
                        last_event_end_time_per_channel_on_date[channel_id] = main_event_stop_local

        epg_content += "</tv>\n"
        return epg_content

    def save_epg_xml(epg_content, output_file_path):
        """Salva il contenuto EPG XML su file"""
        try:
            with open(output_file_path, "w", encoding="utf-8") as file:
                file.write(epg_content)
            print(f"[✓] File EPG XML salvato con successo: {output_file_path}")
            return True
        except Exception as e:
            print(f"[!] Errore nel salvataggio del file EPG XML: {e}")
            return False

    def main_epg_generator(json_file_path, output_file_path="eventi.xml"):
        """Funzione principale per generare l'EPG XML"""
        print(f"[INFO] Inizio generazione EPG XML da: {json_file_path}")

        # Carica e filtra i dati JSON
        json_data = load_json_for_epg(json_file_path)

        if not json_data:
            print("[!] Nessun dato valido trovato nel file JSON.")
            return False

        print(f"[INFO] Dati caricati per {len(json_data)} date")

        # Genera il contenuto XML EPG
        epg_content = generate_epg_xml(json_data)

        # Salva il file XML
        success = save_epg_xml(epg_content, output_file_path)

        if success:
            print(f"[✓] Generazione EPG XML completata con successo!")
            return True
        else:
            print(f"[!] Errore durante la generazione EPG XML.")
            return False

    # Esempio di utilizzo
    if __name__ == "__main__":
        # Percorso del file JSON di input
        input_json_path = "daddyliveSchedule.json"  # Modifica con il tuo percorso

        # Percorso del file XML di output
        output_xml_path = "eventi.xml"

        # Esegui la generazione EPG
        main_epg_generator(input_json_path, output_xml_path)

# Funzione per il sesto script (vavoo_italy_channels.py)
def vavoo_italy_channels():
    print("Eseguendo il vavoo_italy_channels.py...")

    import requests
    import re
    import os
    import xml.etree.ElementTree as ET
    from dotenv import load_dotenv

    # Carica le variabili d'ambiente dal file .env
    load_dotenv()

    LINK_DADDY = os.getenv("LINK_DADDY", "https://daddylive.dad").strip()
    PROXY = os.getenv("PROXYIP", "").strip()
    EPG_FILE = "epg.xml"
    LOGOS_FILE = "logos.txt"
    OUTPUT_FILE = "channels_italy.m3u8"
    DEFAULT_TVG_ICON = ""

    BASE_URLS = [
        "https://vavoo.to"
    ]

    CATEGORY_KEYWORDS = {
        "Rai": ["rai"],
        "Mediaset": ["twenty seven", "twentyseven", "mediaset", "italia 1", "italia 2", "canale 5"],
        "Sport": ["inter", "milan", "lazio", "calcio", "tennis", "sport", "super tennis", "supertennis", "dazn", "eurosport", "sky sport", "rai sport"],
        "Film & Serie TV": ["crime", "primafila", "cinema", "movie", "film", "serie", "hbo", "fox", "rakuten", "atlantic"],
        "News": ["news", "tg", "rai news", "sky tg", "tgcom"],
        "Bambini": ["frisbee", "super!", "fresbee", "k2", "cartoon", "boing", "nick", "disney", "baby", "rai yoyo"],
        "Documentari": ["documentaries", "discovery", "geo", "history", "nat geo", "nature", "arte", "documentary"],
        "Musica": ["deejay", "rds", "hits", "rtl", "mtv", "vh1", "radio", "music", "kiss", "kisskiss", "m2o", "fm"],
        "Altro": ["focus", "real time"]
    }

    def fetch_epg(epg_file):
        try:
            tree = ET.parse(epg_file)
            return tree.getroot()
        except Exception as e:
            print(f"Errore durante la lettura del file EPG: {e}")
            return None

    def fetch_logos(logos_file):
        logos_dict = {}
        try:
            with open(logos_file, "r", encoding="utf-8") as f:
                for line in f:
                    match = re.match(r'\s*"(.+?)":\s*"(.+?)",?', line)
                    if match:
                        channel_name, logo_url = match.groups()
                        logos_dict[channel_name.lower()] = logo_url
        except Exception as e:
            print(f"Errore durante la lettura del file dei loghi: {e}")
        return logos_dict

    def normalize_channel_name(name):
        name = re.sub(r"\s+", "", name.strip().lower())
        name = re.sub(r"\.it\b", "", name)
        name = re.sub(r"hd|fullhd", "", name)
        return name

    def create_channel_id_map(epg_root):
        channel_id_map = {}
        for channel in epg_root.findall('channel'):
            tvg_id = channel.get('id')
            display_name = channel.find('display-name').text
            if tvg_id and display_name:
                normalized_name = normalize_channel_name(display_name)
                channel_id_map[normalized_name] = tvg_id
        return channel_id_map

    def fetch_channels(base_url):
        try:
            response = requests.get(f"{base_url}/channels", timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"Errore durante il download da {base_url}: {e}")
            return []

    def clean_channel_name(name):
        name = re.sub(r"\s*(\|E|\|H|\(6\)|\(7\)|\.c|\.s)", "", name)
        name = re.sub(r"\s*\(.*?\)", "", name)
        if "zona dazn" in name.lower() or "dazn 1" in name.lower():
            return "DAZN2"
        if "mediaset 20" in name.lower():
            return "20 MEDIASET"
        if "mediaset italia 2" in name.lower():
            return "ITALIA 2"
        if "mediaset 1" in name.lower():
            return "ITALIA 1"
        return name.strip()

    def filter_italian_channels(channels, base_url):
        seen = {}
        results = []
        for ch in channels:
            if ch.get("country") == "Italy":
                clean_name = clean_channel_name(ch["name"])
                if clean_name.lower() in ["dazn", "dazn 2"]:
                    continue
                count = seen.get(clean_name, 0) + 1
                seen[clean_name] = count
                if count > 1:
                    clean_name = f"{clean_name} ({count})"
                results.append((clean_name, f"{base_url}/play/{ch['id']}/index.m3u8"))
        return results

    def classify_channel(name):
        for category, words in CATEGORY_KEYWORDS.items():
            if any(word in name.lower() for word in words):
                return category
        return "Altro"

    def get_manual_channels():
        return [
            {"name": "EUROSPORT 1 (D)", "url": f"{LINK_DADDY}/embed/stream-878.php", "tvg_id": "eurosport.1.it", "logo": "https://raw.githubusercontent.com/tv-logo/tv-logos/main/countries/spain/eurosport-1-es.png", "category": "Sport"},
            {"name": "EUROSPORT 2 (D)", "url": f"{LINK_DADDY}/embed/stream-879.php", "tvg_id": "eurosport.2.it", "logo": "https://raw.githubusercontent.com/tv-logo/tv-logos/main/countries/spain/eurosport-2-es.png", "category": "Sport"},
            {"name": "ITALIA 1 (D)", "url": f"{LINK_DADDY}/embed/stream-854.php", "tvg_id": "italia.1.it", "logo": "https://raw.githubusercontent.com/tv-logo/tv-logos/main/countries/italy/italia1-it.png", "category": "Mediaset"},
            {"name": "LA7 (D)", "url": f"{LINK_DADDY}/embed/stream-855.php", "tvg_id": "la7.it", "logo": "https://raw.githubusercontent.com/tv-logo/tv-logos/main/countries/italy/la7-it.png", "category": "Altro"},
            {"name": "LA7D (D)", "url": f"{LINK_DADDY}/embed/stream-856.php", "tvg_id": "la7.it", "logo": "https://raw.githubusercontent.com/tv-logo/tv-logos/main/countries/italy/la7-it.png", "category": "Altro"},
            {"name": "RAI 1 (D)", "url": f"{LINK_DADDY}/embed/stream-850.php", "tvg_id": "rai1.it", "logo": "https://raw.githubusercontent.com/tv-logo/tv-logos/main/countries/italy/rai-1-it.png", "category": "Rai"},
            {"name": "RAI 2 (D)", "url": f"{LINK_DADDY}/embed/stream-851.php", "tvg_id": "rai2.it", "logo": "https://raw.githubusercontent.com/tv-logo/tv-logos/main/countries/italy/rai-2-it.png", "category": "Rai"},
            {"name": "RAI 3 (D)", "url": f"{LINK_DADDY}/embed/stream-852.php", "tvg_id": "rai3.it", "logo": "https://raw.githubusercontent.com/tv-logo/tv-logos/main/countries/italy/rai-3-it.png", "category": "Rai"},
            {"name": "RAI 3 (D)", "url": f"{LINK_DADDY}/embed/stream-853.php", "tvg_id": "rai3.it", "logo": "https://raw.githubusercontent.com/tv-logo/tv-logos/main/countries/italy/rai-3-it.png", "category": "Rai"},
            {"name": "RAI SPORT (D)", "url": f"{LINK_DADDY}/embed/stream-882.php", "tvg_id": "raisport.it", "logo": "https://raw.githubusercontent.com/tv-logo/tv-logos/main/countries/italy/rai-sport-it.png", "category": "Sport"},
            {"name": "RAI PREMIUM (D)", "url": f"{LINK_DADDY}/embed/stream-858.php", "tvg_id": "raipremium.it", "logo": "https://raw.githubusercontent.com/tv-logo/tv-logos/main/countries/italy/rai-premium-it.png", "category": "Rai"},
            {"name": "SKY SPORT GOLF (D)", "url": f"{LINK_DADDY}/embed/stream-574.php", "tvg_id": "sky.sport.golf.it", "logo": "https://raw.githubusercontent.com/tv-logo/tv-logos/main/countries/italy/sky-sport-golf-it.png", "category": "Sport"},
            {"name": "SKY SPORT MOTOGP (D)", "url": f"{LINK_DADDY}/embed/stream-575.php", "tvg_id": "sky.sport.motogp.it", "logo": "https://raw.githubusercontent.com/tv-logo/tv-logos/main/countries/italy/sky-sport-motogp-it.png", "category": "Sport"},
            {"name": "SKY SPORT TENNIS (D)", "url": f"{LINK_DADDY}/embed/stream-576.php", "tvg_id": "sky.sport.tennis.it", "logo": "https://raw.githubusercontent.com/tv-logo/tv-logos/main/countries/italy/sky-sport-tennis-it.png", "category": "Sport"},
            {"name": "SKY SPORT F1 (D)", "url": f"{LINK_DADDY}/embed/stream-577.php", "tvg_id": "sky.sport.f1.it", "logo": "https://raw.githubusercontent.com/tv-logo/tv-logos/main/countries/italy/sky-sport-f1-it.png", "category": "Sport"},
            {"name": "SKY SPORT FOOTBALL (D)", "url": f"{LINK_DADDY}/embed/stream-460.php", "tvg_id": "sky.sport.max.it", "logo": "https://raw.githubusercontent.com/tv-logo/tv-logos/main/countries/italy/sky-sport-football-it.png", "category": "Sport"},
            {"name": "SKY SPORT UNO (D)", "url": f"{LINK_DADDY}/embed/stream-461.php", "tvg_id": "sky.sport.uno.it", "logo": "https://raw.githubusercontent.com/tv-logo/tv-logos/main/countries/italy/sky-sport-uno-it.png", "category": "Sport"},
            {"name": "SKY SPORT ARENA (D)", "url": f"{LINK_DADDY}/embed/stream-462.php", "tvg_id": "sky.sport.arena.it", "logo": "https://raw.githubusercontent.com/tv-logo/tv-logos/main/countries/italy/sky-sport-arena-it.png", "category": "Sport"},
            {"name": "SKY UNO (D)", "url": f"{LINK_DADDY}/embed/stream-881.php", "tvg_id": "sky.uno.it", "logo": "https://raw.githubusercontent.com/tv-logo/tv-logos/main/countries/italy/sky-uno-it.png", "category": "Altro"},
            {"name": "SKY CINEMA COLLECTION (D)", "url": f"{LINK_DADDY}/embed/stream-859.php", "tvg_id": "skycinemacollectionhd.it", "logo": "https://raw.githubusercontent.com/tv-logo/tv-logos/main/countries/italy/sky-cinema-collection-it.png", "category": "Film & Serie TV"},
            {"name": "SKY CINEMA UNO (D)", "url": f"{LINK_DADDY}/embed/stream-860.php", "tvg_id": "sky.cinema.uno.it", "logo": "https://raw.githubusercontent.com/tv-logo/tv-logos/main/countries/italy/sky-cinema-uno-it.png", "category": "Film & Serie TV"},
            {"name": "SKY CINEMA ACTION (D)", "url": f"{LINK_DADDY}/embed/stream-861.php", "tvg_id": "sky.cinema.action.it", "logo": "https://raw.githubusercontent.com/tv-logo/tv-logos/main/countries/italy/sky-cinema-action-it.png", "category": "Film & Serie TV"},
            {"name": "SLY CINEMA COMEDY (D)", "url": f"{LINK_DADDY}/embed/stream-862.php", "tvg_id": "sky.cinema.comedy.it", "logo": "https://raw.githubusercontent.com/tv-logo/tv-logos/main/countries/italy/sky-cinema-comedy-it.png", "category": "Film & Serie TV"},
            {"name": "SKY CINEMA UNO +24 (D)", "url": f"{LINK_DADDY}/embed/stream-863.php", "tvg_id": "sky.cinema.uno.it", "logo": "https://raw.githubusercontent.com/tv-logo/tv-logos/main/countries/italy/sky-cinema-uno-it.png", "category": "Film & Serie TV"},
            {"name": "SKY CINEMA ROMANCE (D)", "url": f"{LINK_DADDY}/embed/stream-864.php", "tvg_id": "sky.cinema.romance.it", "logo": "https://raw.githubusercontent.com/tv-logo/tv-logos/main/countries/italy/sky-cinema-romance-it.png", "category": "Film & Serie TV"},
            {"name": "SKY CINEMA FAMILY (D)", "url": f"{LINK_DADDY}/embed/stream-865.php", "tvg_id": "sky.cinema.family.it", "logo": "https://raw.githubusercontent.com/tv-logo/tv-logos/main/countries/italy/sky-cinema-family-it.png", "category": "Film & Serie TV"},
            {"name": "SKY CINEMA DUE +24 (D)", "url": f"{LINK_DADDY}/embed/stream-866.php", "tvg_id": "sky.cinema.due.+24.it", "logo": "https://raw.githubusercontent.com/tv-logo/tv-logos/main/countries/italy/sky-cinema-due-plus24-it.png", "category": "Film & Serie TV"},
            {"name": "SKY CINEMA DRAMA (D)", "url": f"{LINK_DADDY}/embed/stream-867.php", "tvg_id": "sky.cinema.drama.it", "logo": "https://raw.githubusercontent.com/tv-logo/tv-logos/main/countries/italy/sky-cinema-drama-it.png", "category": "Film & Serie TV"},
            {"name": "SKY CINEMA SUSPENSE (D)", "url": f"{LINK_DADDY}/embed/stream-868.php", "tvg_id": "sky.cinema.suspense.it", "logo": "https://raw.githubusercontent.com/tv-logo/tv-logos/main/countries/italy/sky-cinema-suspense-it.png", "category": "Film & Serie TV"},
            {"name": "SKY SPORT 24 (D)", "url": f"{LINK_DADDY}/embed/stream-869.php", "tvg_id": "sky.sport24.it", "logo": "https://raw.githubusercontent.com/tv-logo/tv-logos/main/countries/italy/sky-sport-24-it.png", "category": "Sport"},
            {"name": "SKY SPORT CALCIO (D)", "url": f"{LINK_DADDY}/embed/stream-870.php", "tvg_id": "sky.sport.calcio.it", "logo": "https://raw.githubusercontent.com/tv-logo/tv-logos/main/countries/italy/sky-sport-calcio-it.png", "category": "Sport"},
            {"name": "SKY SPORT 251 (D)", "url": f"{LINK_DADDY}/embed/stream-871.php", "tvg_id": "sky.sport..251.it", "logo": "https://raw.githubusercontent.com/tv-logo/tv-logos/refs/heads/main/countries/italy/hd/sky-sport-hd-it.png", "category": "Sport"},
            {"name": "SKY SPORT 252 (D)", "url": f"{LINK_DADDY}/embed/stream-872.php", "tvg_id": "sky.sport..252.it", "logo": "https://raw.githubusercontent.com/tv-logo/tv-logos/refs/heads/main/countries/italy/hd/sky-sport-hd-it.png", "category": "Sport"},
            {"name": "SKY SPORT 253 (D)", "url": f"{LINK_DADDY}/embed/stream-873.php", "tvg_id": "sky.sport..253.it", "logo": "https://raw.githubusercontent.com/tv-logo/tv-logos/refs/heads/main/countries/italy/hd/sky-sport-hd-it.png", "category": "Sport"},
            {"name": "SKY SPORT 254 (D)", "url": f"{LINK_DADDY}/embed/stream-874.php", "tvg_id": "sky.sport..254.it", "logo": "https://raw.githubusercontent.com/tv-logo/tv-logos/refs/heads/main/countries/italy/hd/sky-sport-hd-it.png", "category": "Sport"},
            {"name": "SKY SPORT 255 (D)", "url": f"{LINK_DADDY}/embed/stream-875.php", "tvg_id": "sky.sport..255.it", "logo": "https://raw.githubusercontent.com/tv-logo/tv-logos/refs/heads/main/countries/italy/hd/sky-sport-hd-it.png", "category": "Sport"},
            {"name": "SKY SPORT 256 (D)", "url": f"{LINK_DADDY}/embed/stream-876.php", "tvg_id": "sky.sport..256.it", "logo": "https://raw.githubusercontent.com/tv-logo/tv-logos/refs/heads/main/countries/italy/hd/sky-sport-hd-it.png", "category": "Sport"},
            {"name": "SKY SPORT 257 (SS)", "url": f"https%3A//hls.kangal.icu/hls/sky257/index.m3u8&h_user-agent=Mozilla/5.0%20%28Windows%20NT%2010.0%3B%20Win64%3B%20x64%29%20AppleWebKit/537.36%20%28KHTML%2C%20like%20Gecko%29%20Chrome/133.0.0.0%20Safari/537.36&h_referer=https%3A//skystreaming.stream/&h_origin=https%3A//skystreaming.stream", "tvg_id": "sky.sport..257.it", "logo": "https://raw.githubusercontent.com/tv-logo/tv-logos/refs/heads/main/countries/italy/hd/sky-sport-hd-it.png", "category": "Sport"},
            {"name": "SKY SPORT 258 (SS)", "url": f"https%3A//hls.kangal.icu/hls/sky258/index.m3u8&h_user-agent=Mozilla/5.0%20%28Windows%20NT%2010.0%3B%20Win64%3B%20x64%29%20AppleWebKit/537.36%20%28KHTML%2C%20like%20Gecko%29%20Chrome/133.0.0.0%20Safari/537.36&h_referer=https%3A//skystreaming.stream/&h_origin=https%3A//skystreaming.stream", "tvg_id": "sky.sport..258.it", "logo": "https://raw.githubusercontent.com/tv-logo/tv-logos/refs/heads/main/countries/italy/hd/sky-sport-hd-it.png", "category": "Sport"},
            {"name": "SKY SPORT 259 (SS)", "url": f"https%3A//hls.kangal.icu/hls/sky259/index.m3u8&h_user-agent=Mozilla/5.0%20%28Windows%20NT%2010.0%3B%20Win64%3B%20x64%29%20AppleWebKit/537.36%20%28KHTML%2C%20like%20Gecko%29%20Chrome/133.0.0.0%20Safari/537.36&h_referer=https%3A//skystreaming.stream/&h_origin=https%3A//skystreaming.stream", "tvg_id": "sky.sport..259.it", "logo": "https://raw.githubusercontent.com/tv-logo/tv-logos/refs/heads/main/countries/italy/hd/sky-sport-hd-it.png", "category": "Sport"},
            {"name": "SKY SPORT 260 (SS)", "url": f"https%3A//hls.kangal.icu/hls/sky260/index.m3u8&h_user-agent=Mozilla/5.0%20%28Windows%20NT%2010.0%3B%20Win64%3B%20x64%29%20AppleWebKit/537.36%20%28KHTML%2C%20like%20Gecko%29%20Chrome/133.0.0.0%20Safari/537.36&h_referer=https%3A//skystreaming.stream/&h_origin=https%3A//skystreaming.stream", "tvg_id": "sky.sport..260.it", "logo": "https://raw.githubusercontent.com/tv-logo/tv-logos/refs/heads/main/countries/italy/hd/sky-sport-hd-it.png", "category": "Sport"},
            {"name": "SKY SPORT 261 (SS)", "url": f"https%3A//hls.kangal.icu/hls/sky261/index.m3u8&h_user-agent=Mozilla/5.0%20%28Windows%20NT%2010.0%3B%20Win64%3B%20x64%29%20AppleWebKit/537.36%20%28KHTML%2C%20like%20Gecko%29%20Chrome/133.0.0.0%20Safari/537.36&h_referer=https%3A//skystreaming.stream/&h_origin=https%3A//skystreaming.stream", "tvg_id": "sky.sport..261.it", "logo": "https://raw.githubusercontent.com/tv-logo/tv-logos/refs/heads/main/countries/italy/hd/sky-sport-hd-it.png", "category": "Sport"},
            {"name": "SKY SERIE (D)", "url": f"{LINK_DADDY}/embed/stream-880.php", "tvg_id": "sky.serie.it", "logo": "https://raw.githubusercontent.com/tv-logo/tv-logos/main/countries/italy/sky-serie-it.png", "category": "Film & Serie TV"},
            {"name": "20 MEDIASET (D)", "url": f"{LINK_DADDY}/embed/stream-857.php", "tvg_id": "20mediasethd.it", "logo": "https://raw.githubusercontent.com/tv-logo/tv-logos/main/countries/italy/20-it.png", "category": "Mediaset"},
            {"name": "DAZN 1 (D)", "url": f"{LINK_DADDY}/embed/stream-877.php", "tvg_id": "dazn.1.it.it", "logo": "https://upload.wikimedia.org/wikipedia/commons/d/d6/Dazn-logo.png", "category": "Sport"}
        ]

    def save_m3u8(organized_channels):
        if os.path.exists(OUTPUT_FILE):
            os.remove(OUTPUT_FILE)
        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            f.write('#EXTM3U\n\n')
            for category, channels in organized_channels.items():
                channels.sort(key=lambda x: x["name"].lower())
                for ch in channels:
                    tvg_name_cleaned = re.sub(r"\s*\(.*?\)", "", ch["name"])
                    f.write(f'#EXTINF:-1 tvg-id="{ch.get("tvg_id", "")}" tvg-name="{tvg_name_cleaned}" tvg-logo="{ch.get("logo", DEFAULT_TVG_ICON)}" group-title="{category}", {ch["name"]}\n')
                    f.write(f"{PROXY}{ch['url']}\n\n")

    def main():
        epg_root = fetch_epg(EPG_FILE)
        if epg_root is None:
            print("Impossibile recuperare il file EPG, procedura interrotta.")
            return
        logos_dict = fetch_logos(LOGOS_FILE)
        channel_id_map = create_channel_id_map(epg_root)
        all_links = []
        for url in BASE_URLS:
            channels = fetch_channels(url)
            all_links.extend(filter_italian_channels(channels, url))

        manual_channels = get_manual_channels()

        organized_channels = {category: [] for category in CATEGORY_KEYWORDS.keys()}

        for name, url in all_links:
            category = classify_channel(name)

            # Rimuovi il numero tra parentesi per il mapping tvg-id
            name_for_mapping = re.sub(r'\s*\(\d+\)$', '', name)

            organized_channels[category].append({
                "name": name,
                "url": url,
                "tvg_id": channel_id_map.get(normalize_channel_name(name_for_mapping), ""),
                "logo": logos_dict.get(re.sub(r'\s*\(\d+\)$', '', name.lower()), DEFAULT_TVG_ICON)
            })

        for ch in manual_channels:
            cat = ch.get("category") or classify_channel(ch["name"])
            organized_channels.setdefault(cat, []).append({
                "name": ch["name"],
                "url": ch["url"],
                "tvg_id": ch.get("tvg_id", ""),
                "logo": ch.get("logo", DEFAULT_TVG_ICON)
            })

        save_m3u8(organized_channels)
        print(f"File {OUTPUT_FILE} creato con successo!")

    if __name__ == "__main__":
        main()

# Funzione per il settimo script (world_channels_generator.py)
def world_channels_generator():
    # Codice del settimo script qui
    # Aggiungi il codice del tuo script "world_channels_generator.py" in questa funzione.
    print("Eseguendo il world_channels_generator.py...")
    # Il codice che avevi nello script "world_channels_generator.py" va qui, senza modifiche.
    import requests
    import re
    import os
    from collections import defaultdict
    from dotenv import load_dotenv

    # Carica le variabili d'ambiente dal file .env
    load_dotenv()

    PROXY = os.getenv("PROXYIP", "").strip()
    OUTPUT_FILE = "world.m3u8"
    BASE_URLS = [
        "https://vavoo.to"
    ]

    # Scarica la lista dei canali
    def fetch_channels(base_url):
        try:
            response = requests.get(f"{base_url}/channels", timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"Errore durante il download da {base_url}: {e}")
            return []

    # Pulisce il nome del canale
    def clean_channel_name(name):
        return re.sub(r"\s*(\|E|\|H|\(6\)|\(7\)|\.c|\.s)", "", name).strip()

    # Salva il file M3U8 con i canali ordinati alfabeticamente per categoria
    def save_m3u8(channels):
        if os.path.exists(OUTPUT_FILE):
            os.remove(OUTPUT_FILE)

        # Raggruppa i canali per nazione (group-title)
        grouped_channels = defaultdict(list)
        for name, url, country in channels:
            grouped_channels[country].append((name, url))

        # Ordina le categorie alfabeticamente e i canali dentro ogni categoria
        sorted_categories = sorted(grouped_channels.keys())

        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            f.write('#EXTM3U\n\n')

            for country in sorted_categories:
                # Ordina i canali in ordine alfabetico dentro la categoria
                grouped_channels[country].sort(key=lambda x: x[0].lower())

                for name, url in grouped_channels[country]:
                    f.write(f'#EXTINF:-1 tvg-name="{name}" group-title="{country}", {name}\n')
                    f.write(f"{PROXY}{url}\n\n")

    # Funzione principale
    def main():
        all_channels = []
        for url in BASE_URLS:
            channels = fetch_channels(url)
            for ch in channels:
                clean_name = clean_channel_name(ch["name"])
                country = ch.get("country", "Unknown")  # Estrai la nazione del canale, default Ã¨ "Unknown"
                all_channels.append((clean_name, f"{url}/play/{ch['id']}/index.m3u8", country))

        save_m3u8(all_channels)
        print(f"File {OUTPUT_FILE} creato con successo!")

    if __name__ == "__main__":
        main()

def removerworld():
    import os

    # Lista dei file da eliminare
    files_to_delete = ["channels_italy.m3u8", "eventi.m3u8", "eventi.xml"]

    for filename in files_to_delete:
        if os.path.exists(filename):
            try:
                os.remove(filename)
                print(f"File eliminato: {filename}")
            except Exception as e:
                print(f"Errore durante l'eliminazione di {filename}: {e}")
        else:
            print(f"File non trovato: {filename}")

def remover():
    import os

    # Lista dei file da eliminare
    files_to_delete = ["channels_italy.m3u8", "eventi.m3u8", "eventi.xml"]

    for filename in files_to_delete:
        if os.path.exists(filename):
            try:
                os.remove(filename)
                print(f"File eliminato: {filename}")
            except Exception as e:
                print(f"Errore durante l'eliminazione di {filename}: {e}")
        else:
            print(f"File non trovato: {filename}")

# Funzione principale che esegue tutti gli script
def main():
    try:
        schedule_success = schedule_extractor()
    except Exception as e:
        print(f"Errore durante l'esecuzione di schedule_extractor: {e}")

    eventi_en = os.getenv("EVENTI_EN", "no").strip().lower()
    world_flag = os.getenv("WORLD", "si").strip().lower()

    # EPG Eventi
    try:
        if eventi_en == "si":
            epg_eventi_generator_world()
        else:
            epg_eventi_generator()
    except Exception as e:
        print(f"Errore durante la generazione EPG eventi: {e}")
        return

    # Eventi M3U8
    try:
        if eventi_en == "si":
            eventi_m3u8_generator_world()
        else:
            eventi_m3u8_generator()
    except Exception as e:
        print(f"Errore durante la generazione eventi.m3u8: {e}")
        return

    # EPG Merger
    try:
        epg_merger()
    except Exception as e:
        print(f"Errore durante l'esecuzione di epg_merger: {e}")
        return

    # Canali Italia
    try:
        vavoo_italy_channels()
    except Exception as e:
        print(f"Errore durante l'esecuzione di vavoo_italy_channels: {e}")
        return

    # Canali World e Merge finale
    try:
        if world_flag == "si":
            world_channels_generator()
            merger_playlistworld()
            removerworld()
        elif world_flag == "no":
            merger_playlist()
            remover()
        else:
            print(f"Valore WORLD non valido: '{world_flag}'. Usa 'si' o 'no'.")
            return
    except Exception as e:
        print(f"Errore nella fase finale: {e}")
        return

    print("Tutti gli script sono stati eseguiti correttamente!")

if __name__ == "__main__":
    main()
