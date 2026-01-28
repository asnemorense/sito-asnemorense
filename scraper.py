#!/usr/bin/env python3
import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime
import re

# CONFIGURAZIONE - Girone A Atletico 2000
GIRONE_URL = "https://www.legacalcioa8.it/it/t-teamtable/87/serie-a2-2526/?desk=1"
CALENDARIO_URL = "https://www.legacalcioa8.it/it/t-calendar/87/serie-a2-2526/?desk=1"
TEAM_NAME_TARGET = "AS Nemorense" 

def clean_text(text):
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
    # Cerca la tabella principale
    table = soup.find('table', class_='table-score') or soup.find('table')
    if not table: 
        print("⚠️ Tabella classifica non trovata")
        return []
    
    rows = table.find_all('tr')
    for row in rows:
        cols = row.find_all(['td', 'th'])
        # La Lega Calcio a 8 usa: # | Squadra | PT | G | V | N | P ...
        if len(cols) >= 7:
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
    return classifica

def extract_calendario(soup, target_name):
    partite = []
    target_clean = target_name.lower()
    # Cerchiamo i match-item o righe che contengono i team
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
                
                # Controllo se è la nostra squadra
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
    print(f"🚀 Avvio scraping per: {TEAM_NAME_TARGET} (Girone A)")
    
    soup_cl = get_page(GIRONE_URL)
    classifica = extract_classifica(soup_cl) if soup_cl else []
    print(f"✅ Squadre trovate in classifica: {len(classifica)}")

    soup_cal = get_page(CALENDARIO_URL)
    calendario = extract_calendario(soup_cal, TEAM_NAME_TARGET) if soup_cal else []
    print(f"✅ Partite totali trovate nel calendario: {len(calendario)}")

    # Trova la prima partita futura (senza risultato)
    prossima = next((p for p in calendario if p['risultato'] == '-' and p['nostra']), None)
    if prossima:
        print(f"📅 Prossima partita trovata: {prossima['casa']} vs {prossima['trasferta']}")

    dati = {
        'ultimo_aggiornamento': datetime.now().isoformat(),
        'squadra': TEAM_NAME_TARGET,
        'classifica': classifica,
        'prossima_partita': prossima,
        'calendario': [p for p in calendario if p['nostra']][-10:] # Ultime 10 della nostra squadra
    }

    with open('dati-nemorense.json', 'w', encoding='utf-8') as f:
        json.dump(dati, f, ensure_ascii=False, indent=2)
    
    print(f"🏁 Aggiornamento completato con successo!")

if __name__ == "__main__":
    main()
