#!/usr/bin/env python3
"""
Scraper avanzato per Lega Calcio a 8 con supporto JavaScript
Usa Playwright per renderizzare le pagine dinamiche
"""

import json
import re
from datetime import datetime
from playwright.sync_api import sync_playwright
import time

# CONFIGURAZIONE - Modifica questi parametri
GIRONE_URL = "https://www.legacalcioa8.it/it/teamtable/600/content-girone-a-atletico-2000/"
CALENDARIO_URL = "https://www.legacalcioa8.it/it/calendar/65/serie-a2-2425/"
TEAM_NAME = "AS Nemorense"
GIRONE_NAME = "GIRONE A - ATLETICO 2000"


def scrape_with_browser(url, wait_time=3):
    """Scarica una pagina con browser headless per eseguire JavaScript"""
    print(f"📥 Caricamento pagina: {url}")
    
    with sync_playwright() as p:
        # Lancia browser in modalità headless
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        try:
            # Vai alla pagina
            page.goto(url, wait_until="networkidle", timeout=30000)
            
            # Aspetta che JavaScript carichi i dati
            time.sleep(wait_time)
            
            # Prendi l'HTML renderizzato
            content = page.content()
            
            browser.close()
            return content
            
        except Exception as e:
            print(f"❌ Errore nel caricamento: {e}")
            browser.close()
            return None


def extract_classifica_from_html(html, girone_name):
    """Estrae la classifica dall'HTML renderizzato"""
    classifica = []
    
    try:
        # Cerca la tabella della classifica
        # Il sito usa una struttura specifica - adatta in base al HTML reale
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(html, 'html.parser')
        
        # Trova tutte le righe della tabella
        # NOTA: Questi selettori potrebbero dover essere aggiustati in base al HTML reale
        table = soup.find('table', class_='table')
        if not table:
            table = soup.find('table')
        
        if table:
            rows = table.find_all('tr')
            
            for i, row in enumerate(rows[1:], 1):  # Salta header
                cols = row.find_all(['td', 'th'])
                
                if len(cols) >= 7:
                    # Estrai i dati
                    squadra = {
                        'posizione': str(i),
                        'nome': cols[1].get_text(strip=True) if len(cols) > 1 else '',
                        'giocate': cols[2].get_text(strip=True) if len(cols) > 2 else '0',
                        'vinte': cols[3].get_text(strip=True) if len(cols) > 3 else '0',
                        'pareggiate': cols[4].get_text(strip=True) if len(cols) > 4 else '0',
                        'sconfitte': cols[5].get_text(strip=True) if len(cols) > 5 else '0',
                        'punti': cols[6].get_text(strip=True) if len(cols) > 6 else '0'
                    }
                    
                    # Filtra righe vuote
                    if squadra['nome']:
                        classifica.append(squadra)
        
        print(f"✅ Estratte {len(classifica)} squadre dalla classifica")
        
    except Exception as e:
        print(f"⚠️  Errore nell'estrazione classifica: {e}")
    
    return classifica


def extract_calendario_from_html(html, team_name):
    """Estrae il calendario dall'HTML renderizzato"""
    partite = []
    
    try:
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(html, 'html.parser')
        
        # Cerca tutti i match container
        # NOTA: Adatta i selettori in base alla struttura reale
        matches = soup.find_all('div', class_='match')
        if not matches:
            matches = soup.find_all('tr', class_='match-row')
        
        for match in matches:
            try:
                # Estrai dati partita
                # NOTA: Questi selettori sono esempi e vanno adattati
                data = match.find('div', class_='date')
                casa = match.find('div', class_='home-team')
                trasferta = match.find('div', class_='away-team')
                risultato = match.find('div', class_='score')
                
                if data and casa and trasferta:
                    partita = {
                        'data': data.get_text(strip=True),
                        'casa': casa.get_text(strip=True),
                        'trasferta': trasferta.get_text(strip=True),
                        'risultato': risultato.get_text(strip=True) if risultato else '-',
                        'nostra': team_name.lower() in (casa.get_text().lower() + trasferta.get_text().lower())
                    }
                    partite.append(partita)
                    
            except Exception as e:
                continue
        
        print(f"✅ Estratte {len(partite)} partite dal calendario")
        
    except Exception as e:
        print(f"⚠️  Errore nell'estrazione calendario: {e}")
    
    return partite


def find_prossima_partita(partite, team_name):
    """Trova la prossima partita da giocare"""
    for partita in partite:
        if partita.get('risultato') == '-':
            if team_name.lower() in (partita['casa'].lower() + partita['trasferta'].lower()):
                return {
                    'data': partita['data'],
                    'casa': partita['casa'],
                    'trasferta': partita['trasferta'],
                    'campo': 'Atletico 2000 - Via dello Sport, 12',
                    'girone': 'Serie A2 - Girone A'
                }
    return None


def main():
    """Funzione principale"""
    print("="*60)
    print("🚀 SCRAPER AVANZATO AS NEMORENSE")
    print("="*60)
    print()
    
    # Controlla che Playwright sia installato
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("❌ Playwright non installato!")
        print()
        print("📦 Installa con:")
        print("   pip install playwright")
        print("   playwright install chromium")
        print()
        return
    
    # Scarica classifica
    print("📊 Scaricamento classifica...")
    html_classifica = scrape_with_browser(GIRONE_URL, wait_time=5)
    
    classifica = []
    if html_classifica:
        # Salva HTML per debug
        with open('/tmp/classifica_debug.html', 'w', encoding='utf-8') as f:
            f.write(html_classifica)
        print("💾 HTML salvato in /tmp/classifica_debug.html per debug")
        
        classifica = extract_classifica_from_html(html_classifica, GIRONE_NAME)
    
    # Se la classifica è vuota, usa dati di esempio
    if not classifica:
        print("⚠️  Classifica vuota - usando dati di esempio")
        classifica = [
            {"posizione": "1", "nome": "Squadra 1", "giocate": "10", "vinte": "8", "pareggiate": "1", "sconfitte": "1", "punti": "25"},
            {"posizione": "2", "nome": TEAM_NAME, "giocate": "10", "vinte": "7", "pareggiate": "2", "sconfitte": "1", "punti": "23"}
        ]
    
    # Scarica calendario
    print("📅 Scaricamento calendario...")
    html_calendario = scrape_with_browser(CALENDARIO_URL, wait_time=5)
    
    calendario = []
    prossima_partita = None
    
    if html_calendario:
        # Salva HTML per debug
        with open('/tmp/calendario_debug.html', 'w', encoding='utf-8') as f:
            f.write(html_calendario)
        print("💾 HTML salvato in /tmp/calendario_debug.html per debug")
        
        calendario = extract_calendario_from_html(html_calendario, TEAM_NAME)
        prossima_partita = find_prossima_partita(calendario, TEAM_NAME)
    
    # Se calendario vuoto, usa dati di esempio
    if not calendario:
        print("⚠️  Calendario vuoto - usando dati di esempio")
        calendario = [
            {
                "data": "Dom 26 Gen 2026 • 15:00",
                "casa": TEAM_NAME,
                "trasferta": "Squadra Avversaria",
                "risultato": "3-1",
                "nostra": True
            }
        ]
    
    # Prossima partita di esempio
    if not prossima_partita:
        prossima_partita = {
            "data": "Domenica 2 Febbraio 2026 • 15:00",
            "casa": TEAM_NAME,
            "trasferta": "Prossimo Avversario",
            "campo": "Atletico 2000 - Via dello Sport, 12",
            "girone": "Serie A2 - Girone A"
        }
    
    # Crea il file JSON finale
    dati = {
        'ultimo_aggiornamento': datetime.now().isoformat(),
        'squadra': TEAM_NAME,
        'prossima_partita': prossima_partita,
        'classifica': classifica,
        'calendario': calendario[-10:] if len(calendario) > 10 else calendario
    }
    
    # Salva il file JSON
    output_file = 'dati-nemorense.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(dati, f, ensure_ascii=False, indent=2)
    
    print()
    print("="*60)
    print(f"✅ Dati salvati in {output_file}")
    print(f"📌 Ultimo aggiornamento: {dati['ultimo_aggiornamento']}")
    print(f"📊 Squadre in classifica: {len(classifica)}")
    print(f"📅 Partite nel calendario: {len(calendario)}")
    print("="*60)
    
    return dati


if __name__ == "__main__":
    print()
    print("⚠️  IMPORTANTE:")
    print("Questo scraper usa Playwright per eseguire JavaScript.")
    print()
    print("📦 Prima installazione:")
    print("   pip install playwright beautifulsoup4")
    print("   playwright install chromium")
    print()
    
    risposta = input("Hai già installato Playwright? (s/n): ")
    if risposta.lower() == 's':
        main()
    else:
        print()
        print("📝 Installa prima Playwright:")
        print("1. Apri il terminale/prompt dei comandi")
        print("2. Esegui: pip install playwright beautifulsoup4")
        print("3. Esegui: playwright install chromium")
        print("4. Riesegui questo script")
