# Istruzioni di progetto · Un passo alla volta

Queste istruzioni guidano l'agente di coding (Claude Code) mentre lavora sul repository. Copiare questo file nella root del progetto, o puntarlo da lì, prima di avviare una sessione.

## Per chi stiamo costruendo

Roberto, 63 anni, retinopatia diabetica: visione centrale frammentata, usa lo zoom del telefono al 300%, non usa lo screen reader. Deve chiedere a UniSalute il rimborso di una visita oculistica privata. Ogni scelta di codice si giudica con una domanda: **Roberto, da solo, con lo zoom attivo, riesce a fare questo passo?**

## Regole di prodotto (non negoziabili)

1. Una sola domanda per schermata. Mai scorrimento orizzontale a qualsiasi zoom.
2. Testo del percorso assistito: minimo 24px, contrasto almeno 7:1 (WCAG AAA), pulsanti alti almeno 64px a tutta larghezza.
3. Ogni testo mostrato a Roberto è anche leggibile ad alta voce con il pulsante "Ripeti".
4. Numeri, date e importi arrivano **solo** dai dati estratti e confermati, formattati da funzioni fisse. Il modello non scrive mai una frase che contiene un importo.
5. Il modello propone, Roberto decide. Nessun passo avanza senza un tocco di conferma.
6. Ogni volta che si semplifica una voce ufficiale, la voce ufficiale resta visibile sotto la versione semplice.
7. Nessun errore può comparire fuori dalla schermata che Roberto sta guardando.
8. Se l'AI non risponde o non è sicura, il percorso continua con inserimento a mano o scelta guidata: mai un vicolo cieco.

## Regole di codice

- L'app è un unico `app/index.html` senza dipendenze di build, apribile anche da file.
- I prompt degli agenti non si modificano in `app/index.html`: si modificano in `agents/runtime/*.md` e si sincronizzano con `python agents/sync_prompts.py`.
- Le chiamate al modello passano da `chiamaClaude()` nell'app e da `app/server.js`, che usa il Claude Agent SDK con il login Claude Code di chi avvia il server. Nessuna credenziale nel codice o nel repository.
- Nessun dato reale di persone: solo documenti fittizi in `app/esempi/`.

## Marchi

Il portale "prima" è una ricostruzione ispirata all'area assicurati pubblica di UniSalute, a scopo dimostrativo. Non copiare logo, immagini o asset del sito reale: il nome è reso come testo semplice e la pagina dichiara di non essere affiliata.

## Comandi disponibili

- `/prova-percorso` · percorre l'app come Roberto e segnala dove si blocca
- `/verifica-fedelta` · confronta ogni testo semplificato con l'originale

## Skill da caricare

- `skills/semplificare-senza-tradire` · da usare ogni volta che si scrive o si modifica un testo rivolto a Roberto
