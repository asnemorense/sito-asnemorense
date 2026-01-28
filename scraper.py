#!/usr/bin/env python3
"""
Script per estrarre dati dalla Lega Calcio a 8
Estrae: classifica, prossima partita, calendario per AS Nemorense
"""

import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime
import re

# Configurazione - MODIFICA QUESTI PARAMETRI
GIRONE_URL = "https://www.legacalcioa8.it/it/t-teamtable/87/serie-a2-2526/"  # URL da trovare sul sito
CALENDARIO_URL = "https://www.legacalcioa8.it/it/t-calendar/87/serie-a2-2526/"
TEAM_NAME = "AS Nemorense"  # Nome esatto della squadra come appare sul sito


def get_page(url):
    """Scarica una pagina web"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        return BeautifulSoup(response.text, 'html.parser')
    except Exception as e:
        print(f"Errore nel caricamento di {url}: {e}")
        return None


def extract_classifica(soup):
    """Estrae la classifica dal sito"""
    classifica = []
    
    try:
        # Trova la tabella della classifica
        table = soup.find('table', class_='table-score')
        if not table:
            table = soup.find('table')
        
        if table:
            rows = table.find_all('tr')[1:]  # Salta l'header
            
            for row in rows:
                cols = row.find_all('td')
                if len(cols) >= 7:
                    squadra = {
                        'posizione': cols[0].text.strip(),
                        'nome': cols[1].text.strip(),
                        'giocate': cols[2].text.strip(),
                        'vinte': cols[3].text.strip(),
                        'pareggiate': cols[4].text.strip(),
                        'sconfitte': cols[5].text.strip(),
                        'punti': cols[6].text.strip()
                    }
                    classifica.append(squadra)
    except Exception as e:
        print(f"Errore nell'estrazione della classifica: {e}")
    
    return classifica


def extract_calendario(soup, team_name):
    """Estrae il calendario delle partite"""
    partite = []
    
    try:
        # Trova tutte le partite
        matches = soup.find_all('div', class_='match-item')
        
        for match in matches:
            try:
                data_elem = match.find('div', class_='match-date')
                squadra_casa_elem = match.find('div', class_='team-home')
                squadra_trasferta_elem = match.find('div', class_='team-away')
                risultato_elem = match.find('div', class_='match-score')
                
                if data_elem and squadra_casa_elem and squadra_trasferta_elem:
                    partita = {
                        'data': data_elem.text.strip(),
                        'casa': squadra_casa_elem.text.strip(),
                        'trasferta': squadra_trasferta_elem.text.strip(),
                        'risultato': risultato_elem.text.strip() if risultato_elem else '-',
                        'nostra': team_name in (squadra_casa_elem.text + squadra_trasferta_elem.text)
                    }
                    partite.append(partita)
            except:
                continue
                
    except Exception as e:
        print(f"Errore nell'estrazione del calendario: {e}")
    
    return partite


def find_prossima_partita(partite, team_name):
    """Trova la prossima partita da giocare"""
    oggi = datetime.now()
    
    for partita in partite:
        if partita['risultato'] == '-' and team_name.lower() in (partita['casa'].lower() + partita['trasferta'].lower()):
            return partita
    
    return None


def main():
    """Funzione principale"""
    print("🔄 Inizio estrazione dati dalla Lega Calcio a 8...")
    
    # Scarica la classifica
    print("📊 Scaricamento classifica...")
    soup_classifica = get_page(GIRONE_URL)
    classifica = []
    if soup_classifica:
        classifica = extract_classifica(soup_classifica)
        print(f"✅ Estratte {len(classifica)} squadre")
    
    # Scarica il calendario
    print("📅 Scaricamento calendario...")
    soup_calendario = get_page(CALENDARIO_URL)
    calendario = []
    prossima_partita = None
    if soup_calendario:
        calendario = extract_calendario(soup_calendario, TEAM_NAME)
        prossima_partita = find_prossima_partita(calendario, TEAM_NAME)
        print(f"✅ Estratte {len(calendario)} partite")
    
    # Crea il file JSON
    dati = {
        'ultimo_aggiornamento': datetime.now().isoformat(),
        'squadra': TEAM_NAME,
        'classifica': classifica,
        'prossima_partita': prossima_partita,
        'calendario': calendario[-10:]  # Ultime 10 partite
    }
    
    # Salva il file JSON
    output_file = 'dati-nemorense.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(dati, f, ensure_ascii=False, indent=2)
    
    print(f"✅ Dati salvati in {output_file}")
    print(f"📌 Ultimo aggiornamento: {dati['ultimo_aggiornamento']}")
    
    return dati


if __name__ == "__main__":
    # NOTA: Prima di usare questo script, devi:
    # 1. Trovare l'URL esatto del tuo girone su legacalcioa8.it
    # 2. Modificare le variabili GIRONE_URL e CALENDARIO_URL
    # 3. Verificare che il nome della squadra sia corretto in TEAM_NAME
    
    print("⚠️  IMPORTANTE:")
    print("Prima di eseguire lo script, modifica le URL nelle variabili:")
    print("- GIRONE_URL")
    print("- CALENDARIO_URL")
    print("- TEAM_NAME")
    print()
    print("Puoi trovare il tuo girone su: https://www.legacalcioa8.it/it/1/")
    print()
    
    risposta = input("Hai già configurato le URL? (s/n): ")
    if risposta.lower() == 's':
        main()
    else:
        print("\n📝 Guida rapida:")
        print("1. Vai su https://www.legacalcioa8.it/it/1/")
        print("2. Cerca 'SERIE A2 25/26' e trova il tuo girone")
        print("3. Copia l'URL della classifica e del calendario")
        print("4. Modifica le variabili all'inizio di questo file")
        print("5. Riesegui lo script")
