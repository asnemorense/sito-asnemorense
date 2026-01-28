# 🏆 Sito AS Nemorense - Aggiornamento Automatico

Sito web professionale per l'AS Nemorense con aggiornamento automatico dei dati dalla Lega Calcio a 8.

## 📁 File del Progetto

```
asnemorense/
├── index.html              # Sito web principale
├── dati-nemorense.json     # Dati aggiornati (classifica, calendario, ecc.)
├── scraper.py              # Script Python per estrarre i dati
├── .github/
│   └── workflows/
│       └── aggiorna-dati.yml  # Automazione GitHub Actions
└── README.md               # Questo file
```

## 🚀 Setup Rapido

### 1️⃣ Configurare lo Scraper

Prima di tutto, devi trovare l'URL del tuo girone su legacalcioa8.it:

1. Vai su https://www.legacalcioa8.it/it/1/
2. Cerca "SERIE A2 25/26" e trova il tuo girone (es: Girone E - Stella Azzurra)
3. Clicca sulla classifica e copia l'URL dalla barra degli indirizzi
4. Ripeti per il calendario

Esempio di URL:
```
Classifica: https://www.legacalcioa8.it/it/teamtable/XXX/serie-a2-2526-girone-e/
Calendario: https://www.legacalcioa8.it/it/calendar/XXX/serie-a2-2526-girone-e/
```

5. Apri il file `scraper.py` e modifica queste righe:

```python
GIRONE_URL = "https://www.legacalcioa8.it/it/teamtable/XXX/serie-a2-2526-girone-x/"
CALENDARIO_URL = "https://www.legacalcioa8.it/it/calendar/XXX/serie-a2-2526-girone-x/"
TEAM_NAME = "AS Nemorense"
```

### 2️⃣ Test Locale

Prova lo scraper sul tuo computer:

```bash
# Installa le dipendenze Python
pip install requests beautifulsoup4

# Esegui lo scraper
python scraper.py
```

Se funziona, verrà creato/aggiornato il file `dati-nemorense.json`.

### 3️⃣ Pubblica su GitHub Pages (GRATIS!)

**Opzione A: GitHub Desktop (più facile)**

1. Scarica GitHub Desktop: https://desktop.github.com/
2. Crea un account GitHub se non ce l'hai: https://github.com/signup
3. In GitHub Desktop:
   - File → New Repository
   - Nome: `asnemorense-sito`
   - Percorso: Scegli la cartella del progetto
   - Clicca "Create Repository"
4. Clicca "Publish repository" in alto a destra
5. Su GitHub.com:
   - Vai al tuo repository
   - Settings → Pages
   - Source: "Deploy from a branch"
   - Branch: "main" → Cartella: "/ (root)"
   - Save

**Opzione B: Da Terminale (per esperti)**

```bash
# Inizializza repository Git
git init
git add .
git commit -m "Initial commit"

# Crea repository su GitHub e carica
git remote add origin https://github.com/TUO_USERNAME/asnemorense-sito.git
git branch -M main
git push -u origin main

# Abilita GitHub Pages nelle impostazioni del repository
```

### 4️⃣ Automazione (Opzionale ma Consigliato)

Il file `.github/workflows/aggiorna-dati.yml` è già configurato per:
- ⏰ Aggiornare i dati automaticamente 2 volte al giorno (7:00 e 19:00)
- 🔄 Eseguire lo scraper
- 💾 Salvare i nuovi dati
- 🌐 Aggiornare il sito automaticamente

**Non devi fare nulla!** Una volta caricato su GitHub, funziona da solo.

Puoi anche eseguirlo manualmente:
1. Vai su GitHub.com → tuo repository
2. Tab "Actions"
3. Seleziona "Aggiorna Dati AS Nemorense"
4. Clicca "Run workflow"

## 📊 Struttura del File JSON

Il file `dati-nemorense.json` contiene:

```json
{
  "ultimo_aggiornamento": "2026-01-28T14:30:00",
  "squadra": "AS Nemorense",
  "prossima_partita": {
    "data": "Domenica 2 Febbraio 2026 • 15:00",
    "casa": "AS Nemorense",
    "trasferta": "FC Olimpia",
    "campo": "Atletico 2000 - Via dello Sport, 12"
  },
  "classifica": [...],
  "calendario": [...]
}
```

## 🎨 Personalizzazione del Sito

### Cambiare i Colori

Nel file `index.html`, cerca la sezione `:root` (circa riga 12) e modifica:

```css
:root {
    --primary: #6b0f1a;        /* Bordeaux principale */
    --primary-light: #8b1a2a;  /* Bordeaux chiaro */
    --accent: #ffffff;         /* Bianco */
    --anthracite: #3a3a3a;     /* Antracite */
}
```

### Cambiare il Logo

Nel file `index.html`, cerca `<div class="logo-shield">ASN</div>` e cambia le iniziali.

### Modificare Instagram

Nel file `index.html`, cerca tutti i link `https://www.instagram.com/asnemorense/` e sostituisci con il tuo profilo.

## 🔧 Risoluzione Problemi

### Il sito non si aggiorna
1. Verifica che il file `dati-nemorense.json` sia nella stessa cartella di `index.html`
2. Apri la console del browser (F12) e cerca errori
3. Assicurati che le URL nello scraper siano corrette

### Lo scraper non funziona
1. Verifica che le URL nel file `scraper.py` siano corrette
2. Controlla che il sito della Lega Calcio a 8 sia online
3. Prova a modificare lo script per adattarlo alla struttura del sito

### GitHub Actions fallisce
1. Vai su Actions → seleziona il workflow fallito
2. Leggi i log per capire l'errore
3. Probabilmente le URL dello scraper sono sbagliate

## 🌐 Accesso al Sito

Dopo la pubblicazione su GitHub Pages, il sito sarà disponibile all'indirizzo:

```
https://TUO_USERNAME.github.io/asnemorense-sito/
```

## 💡 Alternative di Hosting

Se preferisci non usare GitHub:

- **Netlify**: Trascina la cartella su netlify.app (GRATIS)
- **Vercel**: Connetti il repository GitHub (GRATIS)
- **Hosting tradizionale**: Carica via FTP i file HTML e JSON

## 📞 Supporto

Se hai problemi:
1. Verifica di aver seguito tutti i passaggi
2. Controlla che tutte le URL siano corrette
3. Leggi i messaggi di errore nella console del browser o nei log di GitHub

## 📝 Note Importanti

- ⚠️ Lo scraper dipende dalla struttura del sito legacalcioa8.it
- ⚠️ Se il sito cambia struttura, dovrai aggiornare lo scraper
- ✅ Il sito funziona anche senza aggiornamenti automatici (dati statici)
- ✅ Puoi modificare manualmente il file JSON se preferisci

## 🎯 Funzionalità

✅ Aggiornamento automatico di:
- 📊 Classifica completa del girone
- ⚽ Prossima partita da giocare
- 📅 Calendario con ultimi risultati
- 🕐 Data e ora ultimo aggiornamento

✅ Design professionale:
- 🎨 Colori bordeaux, bianco, antracite
- 📱 Completamente responsive (mobile e desktop)
- ⚡ Animazioni fluide
- 🔗 Link ai social media

## 📄 Licenza

Questo progetto è libero da usare e modificare per scopi personali.

---

**Buona fortuna AS Nemorense! ⚽🏆**
