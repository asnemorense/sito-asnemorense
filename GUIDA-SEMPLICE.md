# 📱 GUIDA SEMPLIFICATA - Per Chi Non È Esperto di Computer

## 🎯 Cosa Hai Bisogno

- Un computer (Windows, Mac o Linux)
- Una connessione internet
- 30 minuti di tempo

## 📋 PASSO 1: Scarica Tutto

1. Scarica tutti i file che ti ho dato in una cartella sul tuo computer
2. La cartella dovrebbe contenere:
   - `index.html` (il sito)
   - `dati-nemorense.json` (i dati)
   - `scraper.py` (lo script per aggiornare)
   - `README.md` (istruzioni dettagliate)

## 🌐 PASSO 2: Trova l'Indirizzo del Tuo Girone

1. Apri il browser (Chrome, Firefox, Safari...)
2. Vai su: **https://www.legacalcioa8.it/it/1/**
3. Cerca la scritta "SERIE A2 25/26"
4. Trova il tuo girone (quello dove gioca AS Nemorense)
5. Clicca sulla **CLASSIFICA**
6. **COPIA** l'indirizzo dalla barra in alto (es: `https://www.legacalcioa8.it/it/teamtable/456/serie-a2-2526-girone-e/`)
7. **SALVALO** su un foglio di carta o in un file di testo

8. Torna indietro e clicca sul **CALENDARIO**
9. **COPIA** anche questo indirizzo
10. **SALVALO** anche questo

## ✏️ PASSO 3: Modifica lo Script

### Su Windows:

1. Clicca col tasto destro su `scraper.py`
2. Seleziona "Apri con" → "Blocco note"
3. Cerca le righe che iniziano con `GIRONE_URL` e `CALENDARIO_URL`
4. Sostituisci gli indirizzi con quelli che hai copiato prima
5. Salva il file (Ctrl+S)

### Su Mac:

1. Clicca col tasto destro su `scraper.py`
2. Seleziona "Apri con" → "TextEdit"
3. Cerca le righe che iniziano con `GIRONE_URL` e `CALENDARIO_URL`
4. Sostituisci gli indirizzi con quelli che hai copiato prima
5. Salva il file (Cmd+S)

## 🚀 PASSO 4: Pubblica il Sito (GRATIS con GitHub)

### 4A. Crea un Account GitHub

1. Vai su **https://github.com/signup**
2. Inserisci:
   - Email
   - Password
   - Username (es: `asnemorense`)
3. Verifica la email
4. Completa la registrazione

### 4B. Scarica GitHub Desktop

1. Vai su **https://desktop.github.com/**
2. Scarica il programma per il tuo computer
3. Installalo (doppio click sul file scaricato)
4. Apri GitHub Desktop
5. Fai il login con l'account che hai creato

### 4C. Carica i Tuoi File

1. In GitHub Desktop, clicca **"File"** → **"New Repository"**
2. Compila:
   - **Name**: `sito-asnemorense`
   - **Description**: "Sito ufficiale AS Nemorense"
   - **Local Path**: Scegli la cartella dove hai i file
3. Clicca **"Create Repository"**
4. Clicca **"Publish repository"** in alto a destra
5. Togli la spunta da "Keep this code private" (vogliamo che sia pubblico)
6. Clicca **"Publish repository"**

### 4D. Attiva il Sito

1. Vai su **github.com** e fai il login
2. Clicca sul tuo repository `sito-asnemorense`
3. Clicca su **"Settings"** (in alto a destra)
4. Nel menu a sinistra, clicca **"Pages"**
5. Sotto "Source", seleziona:
   - **Branch**: `main`
   - **Folder**: `/ (root)`
6. Clicca **"Save"**
7. Aspetta 2-3 minuti
8. Ricarica la pagina
9. Vedrai un messaggio: **"Your site is live at https://tuousername.github.io/sito-asnemorense/"**

## 🎉 FATTO!

Il tuo sito è online! Puoi visitarlo all'indirizzo che ti ha dato GitHub.

## 🔄 Come Aggiornare i Dati (2 Metodi)

### Metodo 1: AUTOMATICO (Consigliato)

Il sito si aggiornerà da solo 2 volte al giorno (7:00 e 19:00).
**Non devi fare nulla!**

Per verificare:
1. Vai su github.com → tuo repository
2. Clicca sulla tab **"Actions"**
3. Vedrai gli aggiornamenti automatici

### Metodo 2: MANUALE

Se vuoi aggiornare subito:

1. Vai su github.com → tuo repository
2. Clicca sulla tab **"Actions"**
3. Clicca su **"Aggiorna Dati AS Nemorense"** a sinistra
4. Clicca **"Run workflow"** a destra
5. Clicca **"Run workflow"** di nuovo nel popup
6. Aspetta 1-2 minuti
7. Il sito è aggiornato!

## 📱 Come Condividere il Sito

Condividi questo link con tutti:

```
https://tuousername.github.io/sito-asnemorense/
```

Puoi:
- Postarlo su Facebook/Instagram
- Mandarlo via WhatsApp
- Metterlo nella bio Instagram
- Stamparlo sui volantini

## 💰 Costi

**TUTTO GRATIS!** ✅

- GitHub: gratis
- Hosting del sito: gratis
- Aggiornamenti automatici: gratis
- Non serve carta di credito

## ❓ Domande Frequenti

**Q: Il sito non si aggiorna**
A: Aspetta qualche minuto e ricarica la pagina (Ctrl+F5 o Cmd+Shift+R)

**Q: Non riesco a trovare l'URL del girone**
A: Vai su legacalcioa8.it, cerca "Serie A2 25/26", trova il tuo girone e copia l'indirizzo dalla barra del browser

**Q: GitHub Actions non funziona**
A: Probabilmente l'URL del girone nello script è sbagliato. Ricontrollalo.

**Q: Voglio cambiare i colori**
A: Apri `index.html`, cerca `:root` e modifica i colori. Poi ricarica su GitHub.

**Q: Posso usare un mio dominio (es: asnemorense.it)?**
A: Sì! Nelle impostazioni di GitHub Pages puoi aggiungere un dominio personalizzato.

## 🆘 Hai Bisogno di Aiuto?

Se qualcosa non funziona:

1. Rileggi attentamente questa guida
2. Controlla di aver fatto tutti i passaggi
3. Guarda se ci sono messaggi di errore
4. Cerca su Google l'errore specifico

## 📞 Contatti

Per problemi specifici con GitHub:
- Vai su: https://docs.github.com/en/pages

---

**In bocca al lupo con il sito dell'AS Nemorense! ⚽🔴⚪**
