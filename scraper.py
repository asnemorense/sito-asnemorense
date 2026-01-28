#!/usr/bin/env python3
import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime

# CONFIGURAZIONE - Inserisci i tuoi link tra le virgolette
GIRONE_URL = "https://www.legacalcioa8.it/it/t-teamtable/87/serie-a2-2526/5-girone-e/"  
CALENDARIO_URL = "https://www.legacalcioa8.it/it/t-calendar/87/serie-a2-2526/5-girone-e/"
TEAM_NAME = "AS Nemorense" 

def get_page(url):
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        return BeautifulSoup(response.text, 'html.parser')
    except Exception as e:
        print(f"Errore caricamento: {e}")
        return None

def extract_classifica(soup):
    classifica = []
    try:
        table = soup.find('table', class_='table-score') or soup.find('table')
        if table:
            rows = table.find_all('tr')[1:]
            for row in rows:
                cols = row.find_all('td')
                if len(cols) >= 7:
                    classifica.append({
                        'posizione': cols[0].text.strip(),
                        'nome': cols[1].text.strip(),
                        'giocate': cols[2].text.strip(),
                        'vinte': cols[3].text.strip(),
                        'pareggiate': cols[4].text.strip(),
                        'sconfitte': cols[5].text.strip(),
                        'punti': cols[6].text.strip()
                    })
    except: pass
    return classifica

def extract_calendario(soup, team_name):
    partite = []
    try:
        matches = soup.find_all('div', class_='match-item')
        for match in matches:
            try:
                data = match.find('div', class_='match-date').text.strip()
                casa = match.find('div', class_='team-home').text.strip()
                trasferta = match.find('div', class_='team-away').text.strip()
                risultato = match.find('div', class_='match-score').text.strip() if match.find('div', class_='match-score') else '-'
                partite.append({
                    'data': data, 'casa': casa, 'trasferta': trasferta,
                    'risultato': risultato, 'nostra': team_name.lower() in (casa + trasferta).lower()
                })
            except: continue
    except: pass
    return partite

def main():
    print("🔄 Avvio aggiornamento dati...")
    soup_classifica = get_page("https://www.legacalcioa8.it/it/t-teamtable/87/serie-a2-2526/5-girone-e/")
    classifica = extract_classifica(soup_classifica) if soup_classifica else []
    
    soup_calendario = get_page("https://www.legacalcioa8.it/it/t-calendar/87/serie-a2-2526/5-girone-e/")
    calendario = extract_calendario(soup_calendario, TEAM_NAME) if soup_calendario else []
    
    prossima = next((p for p in calendario if p['risultato'] == '-' and p['nostra']), None)
    
    dati = {
        'ultimo_aggiornamento': datetime.now().isoformat(),
        'squadra': TEAM_NAME,
        'classifica': classifica,
        'prossima_partita': prossima,
        'calendario': calendario[-10:]
    }
    
    with open('dati-nemorense.json', 'w', encoding='utf-8') as f:
        json.dump(dati, f, ensure_ascii=False, indent=2)
    print("✅ Dati salvati con successo!")

if __name__ == "__main__":
    main()
