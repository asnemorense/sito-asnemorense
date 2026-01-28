#!/usr/bin/env python3
"""
Scraper API-Based per Lega Calcio a 8
Intercetta le chiamate API nascoste utilizzate dall'app mobile
"""

import json
import requests
from datetime import datetime
import time

# CONFIGURAZIONE
TEAM_NAME = "AS Nemorense"
GIRONE_ID = "600"  # ID del Girone A - Atletico 2000
TOURNAMENT_ID = "65"  # ID Serie A2 24/25

# Base URL dell'API (probabilmente usata dall'app mobile)
API_BASE = "https://www.legacalcioa8.it/api"  # Da verificare
# Oppure potrebbe essere ospitata su enjore.com (il provider del software)
API_BASE_ALT = "https://api.enjore.com"


def try_api_endpoints():
    """Prova diversi endpoint API comuni"""
    
    possible_endpoints = [
        f"https://www.legacalcioa8.it/api/teamtable/{GIRONE_ID}",
        f"https://www.legacalcioa8.it/api/calendar/{TOURNAMENT_ID}",
        f"https://api.enjore.com/wl/legac8_com/teamtable/{GIRONE_ID}",
        f"https://api.enjore.com/wl/legac8_com/calendar/{TOURNAMENT_ID}",
        f"https://www.legacalcioa8.it/json/teamtable/{GIRONE_ID}",
        f"https://www.legacalcioa8.it/data/teamtable/{GIRONE_ID}.json",
    ]
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15',
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    }
    
    print("🔍 Cercando endpoint API...")
    print()
    
    for endpoint in possible_endpoints:
        try:
            print(f"📡 Provando: {endpoint}")
            response = requests.get(endpoint, headers=headers, timeout=10)
            
            if response.status_code == 200:
                print(f"✅ TROVATO! Status: {response.status_code}")
                print(f"📄 Content-Type: {response.headers.get('Content-Type', 'N/A')}")
                
                # Prova a parsare come JSON
                try:
                    data = response.json()
                    print(f"📊 Dati JSON ricevuti!")
                    print(f"Keys: {list(data.keys()) if isinstance(data, dict) else 'Array'}")
                    return endpoint, data
                except:
                    print(f"⚠️  Non è JSON valido")
                    print(f"Preview: {response.text[:200]}")
            else:
                print(f"❌ Status: {response.status_code}")
                
        except requests.exceptions.Timeout:
            print(f"⏱️  Timeout")
        except Exception as e:
            print(f"❌ Errore: {e}")
        
        print()
        time.sleep(0.5)
    
    return None, None


def scrape_with_network_analysis():
    """
    Guida per usare gli strumenti del browser per trovare le API
    """
    print("="*70)
    print("🔧 METODO: Analisi Network delle Chiamate API")
    print("="*70)
    print()
    print("Segui questi passaggi per trovare gli endpoint API reali:")
    print()
    print("1. Apri Chrome/Firefox")
    print("2. Vai su: https://www.legacalcioa8.it/it/teamtable/600/content-girone-a-atletico-2000/")
    print("3. Premi F12 per aprire DevTools")
    print("4. Vai sulla tab 'Network' (Rete)")
    print("5. Ricarica la pagina (F5)")
    print("6. Cerca chiamate che contengono 'api', 'json', 'data', 'teamtable'")
    print("7. Clicca su una chiamata → tab 'Response' per vedere i dati")
    print("8. Copia l'URL della chiamata che contiene i dati della classifica")
    print()
    print("Esempi di URL da cercare:")
    print("  - .../api/...")
    print("  - .../data/...")
    print("  - .../json/...")
    print("  - Qualsiasi richiesta che restituisce JSON")
    print()
    print("="*70)
    print()
    
    input("Premi INVIO quando hai trovato l'URL dell'API...")
    
    api_url = input("\n📝 Incolla l'URL dell'API qui: ").strip()
    
    if api_url:
        print(f"\n🔄 Provando a scaricare da: {api_url}")
        try:
            response = requests.get(api_url, timeout=10)
            if response.status_code == 200:
                data = response.json()
                print("✅ Dati scaricati correttamente!")
                return api_url, data
            else:
                print(f"❌ Errore: Status {response.status_code}")
        except Exception as e:
            print(f"❌ Errore: {e}")
    
    return None, None


def create_json_from_manual_data():
    """Crea il JSON finale dai dati estratti"""
    
    # Per ora usiamo dati di esempio
    # Quando troveremo l'API reale, useremo quei dati
    
    dati = {
        "ultimo_aggiornamento": datetime.now().isoformat(),
        "squadra": TEAM_NAME,
        "prossima_partita": {
            "data": "Domenica 2 Febbraio 2026 • 15:00",
            "casa": TEAM_NAME,
            "trasferta": "Prossimo Avversario",
            "campo": "Atletico 2000 - Via dello Sport, 12",
            "girone": "Serie A2 - Girone A"
        },
        "classifica": [
            {
                "posizione": "1",
                "nome": "Squadra Esempio 1",
                "giocate": "10",
                "vinte": "8",
                "pareggiate": "1",
                "sconfitte": "1",
                "punti": "25"
            },
            {
                "posizione": "2",
                "nome": TEAM_NAME,
                "giocate": "10",
                "vinte": "7",
                "pareggiate": "2",
                "sconfitte": "1",
                "punti": "23"
            }
        ],
        "calendario": [
            {
                "data": "Dom 26 Gen 2026 • 15:00",
                "casa": TEAM_NAME,
                "trasferta": "Squadra Avversaria",
                "risultato": "3-1",
                "nostra": True
            }
        ]
    }
    
    # Salva
    with open('dati-nemorense.json', 'w', encoding='utf-8') as f:
        json.dump(dati, f, ensure_ascii=False, indent=2)
    
    print("✅ File dati-nemorense.json creato!")
    return dati


def main():
    print()
    print("🎯 SCRAPER API AS NEMORENSE")
    print()
    
    print("Questo scraper cerca di trovare le API nascoste usate dal sito.")
    print()
    
    # Prova endpoint comuni
    endpoint, data = try_api_endpoints()
    
    if not endpoint:
        print()
        print("❌ Nessun endpoint API trovato automaticamente")
        print()
        print("🔍 Proviamo con l'analisi manuale delle chiamate di rete...")
        print()
        
        endpoint, data = scrape_with_network_analysis()
    
    if endpoint and data:
        print()
        print(f"✅ API trovata: {endpoint}")
        print()
        print("💾 Salvando i dati...")
        
        # Qui dovresti parsare i dati reali dall'API
        # Per ora usiamo la funzione con dati di esempio
        create_json_from_manual_data()
    else:
        print()
        print("⚠️  Non è stato possibile trovare l'API automaticamente")
        print()
        print("📝 SOLUZIONE ALTERNATIVA:")
        print("Usa il file 'aggiorna-dati.html' per inserire i dati manualmente")
        print("oppure usa lo scraper Playwright: 'scraper-playwright.py'")
        print()


if __name__ == "__main__":
    main()
