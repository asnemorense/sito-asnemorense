#!/usr/bin/env python3
import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime
import re

# CONFIGURAZIONE - Girone A Atletico 2000
GIRONE_URL = "https://www.legacalcioa8.it/it/t-teamtable/87/serie-a2-2526/?desk=1"
CALENDARIO_URL = "https://www.legacalcioa8.it/it/t-calendar/87/serie-a2-2526/?desk=1"
TEAM_NAME_TARGET = "Nemorense" 

def clean_name(name):
    return re.sub(r'[^\w\s]', '', name).lower().strip()

def get_page(url):
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        return BeautifulSoup(response.text, 'html.parser')
    except Exception as e:
        print(f"❌ Errore connessione: {e}")
        return None

def extract_classifica(soup):
    classifica = []
    table = soup.find('table', class_='table-score') or soup.find('table')
    if not table: return []
    rows = table.find_all('tr')
    for row in rows:
        cols = row.find_all(['td', 'th'])
        if len(cols) >= 7 and cols[0].text.strip().isdigit():
            classifica.append({
                'posizione': cols[0].text.strip(),
                'nome': cols[1].text.strip(),
                'giocate': cols[2].text.strip(),
                'vinte': cols[3].text.strip(),
                'pareggiate': cols[4].text.strip(),
                'sconfitte': cols[5].text.strip(),
                'punti': cols[6].text.strip()
            })
    return classifica

def extract_calendario(soup, target_name):
    partite = []
    clean_target = clean_name(target_name)
    matches = soup.find_all('div', class_='match-item')
    for match in matches:
        try:
            data_el = match.find('div', class_='match-date')
            home_el = match.find('div', class_='team-home')
            away_el = match.find('div', class_='team-away')
            score_el = match.find('div', class_='match-score')
            if data_el and home_el and away_el:
                casa = home_el.text.strip()
                trasferta = away_el.text.strip()
                is_our = clean_target in clean_name(casa) or clean_target in clean_name(trasferta)
                partite.append({
                    'data': data_el.text.strip(),
                    'casa': casa,
                    'trasferta': trasferta,
                    'risultato': score_el.text.strip() if score_el else '-',
                    'nostra': is_our
                })
        except: continue
    return partite

def main():
    print(f"🚀 Avvio scraping per: {TEAM_NAME_TARGET}")
    soup_cl = get_page(GIRONE_URL)
    classifica = extract_classifica(soup_cl) if soup_cl else []
    soup_cal = get_page(CALENDARIO_URL)
    calendario = extract_calendario(soup_cal, TEAM_NAME_TARGET) if soup_cal else []
    prossima = next((p for p in calendario if p['risultato'] == '-' and p['nostra']), None)
    dati = {
        'ultimo_aggiornamento': datetime.now().isoformat(),
        'squadra': TEAM_NAME_TARGET,
        'classifica': classifica,
        'prossima_partita': prossima,
        'calendario': calendario[-10:]
    }
    with open('dati-nemorense.json', 'w', encoding='utf-8') as f:
        json.dump(dati, f, ensure_ascii=False, indent=2)
    print(f"✅ Aggiornamento completato")

if __name__ == "__main__":
    main()
