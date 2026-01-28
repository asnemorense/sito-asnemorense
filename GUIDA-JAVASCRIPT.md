# 🤖 GUIDA: Aggiornamento Automatico con JavaScript

## Il Problema del JavaScript Dinamico

Il sito della Lega Calcio a 8 carica i dati tramite JavaScript **dopo** che la pagina è stata caricata. Questo significa che uno scraper tradizionale vede solo l'HTML vuoto, non i dati.

## ✅ SOLUZIONE 1: Playwright (Consigliato per Automazione)

Playwright è un browser headless che esegue il JavaScript e poi estrae i dati.

### Installazione Locale (Per Test)

```bash
# Installa Playwright
pip install playwright beautifulsoup4

# Scarica browser Chromium
playwright install chromium
playwright install-deps
```

### Configurazione

1. **Apri `scraper-playwright.py`**
2. **Modifica queste righe:**

```python
GIRONE_URL = "https://www.legacalcioa8.it/it/teamtable/600/content-girone-a-atletico-2000/"
CALENDARIO_URL = "https://www.legacalcioa8.it/it/calendar/65/serie-a2-2425/"
TEAM_NAME = "AS Nemorense"
```

3. **Esegui lo scraper:**

```bash
python scraper-playwright.py
```

### Come Funziona

1. Playwright apre un browser Chrome invisibile
2. Carica la pagina e aspetta che JavaScript finisca
3. Estrae i dati dall'HTML renderizzato
4. Salva tutto in `dati-nemorense.json`

### Su GitHub Actions

Il workflow è già configurato! Una volta caricato su GitHub:
- Si esegue automaticamente 2 volte al giorno (7:00 e 19:00)
- Scarica Chromium
- Esegue lo scraper
- Aggiorna il file JSON
- Il sito si aggiorna automaticamente

---

## ✅ SOLUZIONE 2: Trovare l'API Nascosta (Più Veloce)

Molti siti che usano JavaScript hanno un'API nascosta che serve i dati.

### Come Trovarla

1. **Apri Chrome e vai su:**
   ```
   https://www.legacalcioa8.it/it/teamtable/600/content-girone-a-atletico-2000/
   ```

2. **Premi F12** (DevTools)

3. **Vai sulla tab "Network" (Rete)**

4. **Ricarica la pagina (F5)**

5. **Cerca chiamate di tipo XHR/Fetch** che contengono:
   - `api`
   - `json`
   - `data`
   - `teamtable`
   - `calendar`

6. **Clicca su una chiamata → Tab "Response"**
   - Se vedi JSON con i dati della classifica, **HAI TROVATO L'API!**

7. **Copia l'URL** della richiesta (click destro → Copy → Copy URL)

### Esempio di cosa cercare:

```
❌ https://www.legacalcioa8.it/it/teamtable/600/...  (HTML)
✅ https://api.enjore.com/wl/legac8_com/teamtable/600  (JSON!)
✅ https://www.legacalcioa8.it/api/teamtable/600.json  (JSON!)
```

### Usa lo Script API

1. **Esegui:**
   ```bash
   python scraper-api.py
   ```

2. **Lo script proverà vari endpoint comuni**

3. **Se non trova nulla, ti guiderà nell'analisi manuale**

4. **Incolla l'URL dell'API quando richiesto**

5. **Lo script scaricherà i dati direttamente!**

### Vantaggi dell'API

✅ **10x più veloce** di Playwright
✅ **Meno risorse** (no browser)
✅ **Più affidabile** (no rendering)
✅ **Più stabile** nel tempo

---

## ✅ SOLUZIONE 3: Aggiornamento Manuale (Sempre Funziona)

Se gli scraper automatici danno problemi, usa il sistema manuale:

1. **Apri `aggiorna-dati.html`** nel browser
2. **Inserisci i dati** (5 minuti)
3. **Genera JSON**
4. **Copia e incolla** in `dati-nemorense.json`
5. **Carica su GitHub**

---

## 🎯 Quale Soluzione Usare?

### Per GitHub Actions (Automazione Completa):
1. **Prima prova:** Trovare l'API nascosta (Soluzione 2)
2. **Se non funziona:** Usa Playwright (Soluzione 1)

### Per Aggiornamenti Manuali:
- **Usa `aggiorna-dati.html`** (Soluzione 3)

---

## 🔧 Troubleshooting

### Playwright non funziona

**Errore:** `playwright: command not found`

**Soluzione:**
```bash
pip install playwright
playwright install chromium
```

### GitHub Actions fallisce

1. **Vai su:** Repository → Actions → Workflow fallito
2. **Leggi i log** per vedere l'errore
3. **Possibili cause:**
   - URL errato in `scraper-playwright.py`
   - Struttura HTML del sito cambiata
   - Timeout (aumenta `wait_time` nello script)

### Lo scraper non trova i dati

1. **Apri i file di debug:**
   - `/tmp/classifica_debug.html`
   - `/tmp/calendario_debug.html`

2. **Controlla se contengono i dati**

3. **Se sì:** I selettori CSS nello script sono sbagliati
   - Apri `scraper-playwright.py`
   - Modifica la funzione `extract_classifica_from_html`
   - Adatta i selettori alla struttura reale

---

## 📊 Riepilogo

| Metodo | Velocità | Difficoltà | Affidabilità |
|--------|----------|------------|--------------|
| API nascosta | ⚡⚡⚡ | 🔧🔧 | ⭐⭐⭐⭐⭐ |
| Playwright | ⚡⚡ | 🔧🔧🔧 | ⭐⭐⭐⭐ |
| Manuale | ⚡ | 🔧 | ⭐⭐⭐⭐⭐ |

---

## 🆘 Hai Bisogno di Aiuto?

1. **Prova prima la Soluzione 2** (trovare l'API)
2. **Se non funziona, usa la Soluzione 1** (Playwright)
3. **Come backup, usa sempre la Soluzione 3** (manuale)

**Ricorda:** Il metodo manuale funziona SEMPRE e richiede solo 5 minuti a settimana!
