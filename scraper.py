#!/usr/bin/env python3
import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime
import re

# CONFIGURAZIONE - Serie A2 25/26 - Girone A (Atletico 2000)
GIRONE_URL = "https://www.legacalcioa8.it/it/t-teamtable/87/serie-a2-2526/1-girone-a/"
CALENDARIO_URL = "https://www.legacalcioa8.it/it/t-calendar/87/serie-a2-2526/1-girone-a/"
TEAM_NAME_TARGET = "AS Nemorense" 

def clean_text(text):
    """Pulisce il testo da spazi e caratteri speciali."""
    return text.strip().replace('\xa0', ' ')

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
    # Cerchiamo tutte le tabelle per sicurezza
    tables = soup.find_all('table')
    if not tables: 
        print("⚠️ Nessuna tabella trovata nella pagina!")
        return []
    
    for table in tables:
        rows = table.find_all('tr')
        for row in rows:
            cols = row.find_all(['td', 'th'])
            # La classifica della Lega Calcio a 8 ha almeno 7 colonne
            if len(cols) >= 7:
                # Puliamo la posizione (es: "1." diventa "1")
                pos_raw = clean_text(cols[0].text).rstrip('.')
                if pos_raw.isdigit():
                    classifica.append({
                        'posizione': pos_raw,
                        'nome': clean_text(cols[1].text),
                        'punti': clean_text(cols[2].text),
                        'giocate': clean_text(cols[3].text),
                        'vinte': clean_text(cols[4].text),
                        'pareggiate': clean_text(cols[5].text),
                        'sconfitte': clean_text(cols[6].text)
                    })
        if classifica: 
            print(f"✅ Classifica estratta con successo ({len(classifica)} squadre)")
            break 
    return classifica

def extract_calendario(soup, target_name):
    partite = []
    target_clean = target_name.lower()
    matches = soup.find_all('div', class_='match-item')
    
    for match in matches:
        try:
            data_el = match.find('div', class_='match-date')
            home_el = match.find('div', class_='team-home')
            away_el = match.find('div', class_='team-away')
            score_el = match.find('div', class_='match-score')
            
            if data_el and home_el and away_el:
                casa = clean_text(home_el.text)
                trasferta = clean_text(away_el.text)
                risultato = clean_text(score_el.text) if score_el else '-'
                is_our = target_clean in casa.lower() or target_clean in trasferta.lower()
                
                partite.append({
                    'data': clean_text(data_el.text),
                    'casa': casa,
                    'trasferta': trasferta,
                    'risultato': risultato,
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
    print(f"📅 Partite trovate nel calendario: {len(calendario)}")

    prossima = next((p for p in calendario if p['risultato'] == '-' and p['nostra']), None)

    dati = {
        'ultimo_aggiornamento': datetime.now().isoformat(),
        'squadra': TEAM_NAME_TARGET,
        'classifica': classifica,
        'prossima_partita': prossima,
        'calendario': [p for p in calendario if p['nostra']][-10:]
    }

    with open('dati-nemorense.json', 'w', encoding='utf-8') as f:
        json.dump(dati, f, ensure_ascii=False, indent=2)
    
    print(f"🏁 Aggiornamento completato alle {datetime.now().strftime('%H:%M:%S')}")

if __name__ == "__main__":
    main()
