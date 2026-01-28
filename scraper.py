#!/usr/bin/env python3
import requests
import json
from datetime import datetime

# CONFIGURAZIONE DIRETTA API - Serie A2 25/26 Girone A
# Questi sono gli indirizzi diretti ai dati del sito
GIRONE_ID = "87" # Serie A2 25/26
GROUP_ID = "1"  # Girone A
TEAM_NAME_TARGET = "AS Nemorense"

def main():
    print(f"🚀 Avvio estrazione dati per {TEAM_NAME_TARGET}...")
    
    # 1. Recupero Classifica via API
    api_classifica = f"https://www.legacalcioa8.it/it/t-teamtable/{GIRONE_ID}/serie-a2-2526/{GROUP_ID}-girone-a/?format=json"
    
    headers = {'User-Agent': 'Mozilla/5.0'}
    classifica_data = []
    
    try:
        # Tentativo di recupero tramite endpoint ufficiale
        response = requests.get(api_classifica, headers=headers, timeout=15)
        # Se l'API JSON non risponde, usiamo un sistema di emergenza più aggressivo
        print("📊 Analisi classifica in corso...")
        
        # URL pubblico per lo scraping di emergenza se l'API fallisce
        URL_PUBBLICO = f"https://www.legacalcioa8.it/it/t-teamtable/{GIRONE_ID}/serie-a2-2526/{GROUP_ID}-girone-a/"
        resp = requests.get(URL_PUBBLICO, headers=headers)
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(resp.text, 'html.parser')
        
        # Ricerca forzata su ogni riga della tabella
        rows = soup.find_all('tr')
        for row in rows:
            cols = row.find_all(['td', 'th'])
            if len(cols) >= 7:
                pos = cols[0].text.strip().rstrip('.')
                if pos.isdigit():
                    classifica_data.append({
                        'posizione': pos,
                        'nome': cols[1].text.strip(),
                        'punti': cols[2].text.strip(),
                        'giocate': cols[3].text.strip(),
                        'vinte': cols[4].text.strip(),
                        'pareggiate': cols[5].text.strip(),
                        'sconfitte': cols[6].text.strip()
                    })
    except Exception as e:
        print(f"❌ Errore: {e}")

    # 2. Recupero Calendario
    calendario_data = []
    try:
        URL_CAL = f"https://www.legacalcioa8.it/it/t-calendar/{GIRONE_ID}/serie-a2-2526/{GROUP_ID}-girone-a/"
        resp_cal = requests.get(URL_CAL, headers=headers)
        soup_cal = BeautifulSoup(resp_cal.text, 'html.parser')
        matches = soup_cal.find_all('div', class_='match-item')
        
        for m in matches:
            home = m.find('div', class_='team-home').text.strip()
            away = m.find('div', class_='team-away').text.strip()
            score = m.find('div', class_='match-score').text.strip() if m.find('div', class_='match-score') else '-'
            date = m.find('div', class_='match-date').text.strip()
            
            is_our = TEAM_NAME_TARGET.lower() in home.lower() or TEAM_NAME_TARGET.lower() in away.lower()
            calendario_data.append({
                'data': date, 'casa': home, 'trasferta': away, 
                'risultato': score, 'nostra': is_our
            })
    except: pass

    print(f"✅ Squadre trovate: {len(classifica_data)}")
    
    # Salvataggio
    prossima = next((p for p in calendario_data if p['risultato'] == '-' and p['nostra']), None)
    dati = {
        'ultimo_aggiornamento': datetime.now().isoformat(),
        'squadra': TEAM_NAME_TARGET,
        'classifica': classifica_data,
        'prossima_partita': prossima,
        'calendario': [p for p in calendario_data if p['nostra']]
    }

    with open('dati-nemorense.json', 'w', encoding='utf-8') as f:
        json.dump(dati, f, ensure_ascii=False, indent=2)
    print("🏁 Procedura completata.")

if __name__ == "__main__":
    main()
