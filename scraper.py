#!/usr/bin/env python3
import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime

# URL specifici per il Girone A (Serie A2 25/26)
# Questi link caricano la versione "nuda" dei dati, più facile da leggere
GIRONE_URL = "https://www.legacalcioa8.it/it/t-teamtable/87/serie-a2-2526/1-girone-a/"
CALENDARIO_URL = "https://www.legacalcioa8.it/it/t-calendar/87/serie-a2-2526/1-girone-a/"
TEAM_NAME_TARGET = "AS Nemorense"

def get_data(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8'
    }
    try:
        response = requests.get(url, headers=headers, timeout=20)
        response.raise_for_status()
        return BeautifulSoup(response.text, 'html.parser')
    except Exception as e:
        print(f"❌ Errore di connessione: {e}")
        return None

def extract_classifica(soup):
    classifica = []
    # Cerchiamo la tabella dati ignorando le classi CSS che cambiano spesso
    table = soup.find('table')
    if not table: return []
    
    rows = table.find_all('tr')
    for row in rows:
        cols = row.find_all(['td', 'th'])
        # Struttura: Pos | Squadra | Punti | Giocate | V | N | P
        if len(cols) >= 7:
            pos = cols[0].text.strip().rstrip('.')
            if pos.isdigit():
                classifica.append({
                    'posizione': pos,
                    'nome': cols[1].text.strip(),
                    'punti': cols[2].text.strip(),
                    'giocate': cols[3].text.strip(),
                    'vinte': cols[4].text.strip(),
                    'pareggiate': cols[5].text.strip(),
                    'sconfitte': cols[6].text.strip()
                })
    return classifica

def main():
    print(f"🚀 Scraping Girone A per {TEAM_NAME_TARGET}...")
    
    # Estrazione Classifica
    soup_cl = get_data(GIRONE_URL)
    classifica = extract_classifica(soup_cl) if soup_cl else []
    print(f"📊 Squadre trovate: {len(classifica)}")

    # Estrazione Calendario (metodo semplificato)
    soup_cal = get_data(CALENDARIO_URL)
    calendario = []
    if soup_cal:
        items = soup_cal.find_all('div', class_='match-item')
        for item in items:
            try:
                casa = item.find('div', class_='team-home').text.strip()
                trasferta = item.find('div', class_='team-away').text.strip()
                ris = item.find('div', class_='match-score').text.strip() if item.find('div', class_='match-score') else '-'
                data = item.find('div', class_='match-date').text.strip()
                
                is_our = TEAM_NAME_TARGET.lower() in (casa + trasferta).lower()
                calendario.append({
                    'data': data, 'casa': casa, 'trasferta': trasferta,
                    'risultato': ris, 'nostra': is_our
                })
            except: continue
    
    prossima = next((p for p in calendario if p['risultato'] == '-' and p['nostra']), None)

    # Salvataggio finale
    output = {
        'ultimo_aggiornamento': datetime.now().isoformat(),
        'squadra': TEAM_NAME_TARGET,
        'classifica': classifica,
        'prossima_partita': prossima,
        'calendario': [p for p in calendario if p['nostra']]
    }

    with open('dati-nemorense.json', 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    
    print(f"✅ Dati salvati. Squadre in classifica: {len(classifica)}")

if __name__ == "__main__":
    main()
    
