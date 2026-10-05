# Un passo alla volta

Un assistente che accompagna una persona con bassa visione nella richiesta di rimborso di una spesa sanitaria, dalla foto della fattura fino all'invio della pratica.

**Tema 01 · Accessibilità digitale** · Team: Iana Stamati e Mauro Lunghi

> Prototipo dimostrativo. Non è affiliato né approvato da UniSalute. Il portale "Prima" è una ricostruzione semplificata ispirata all'area assicurati pubblica e non usa dati, servizi o materiali di UniSalute. Persone e documenti sono fittizi.

## La persona

Roberto, 63 anni, ex magazziniere, ha una retinopatia diabetica: vede in modo frammentato, con zone sfocate al centro. Usa lo zoom del telefono al 300% e non usa lo screen reader. Deve chiedere a UniSalute il rimborso di una visita oculistica privata da 122 euro (120 di visita e 2 di bollo).

Nel modulo online si blocca tre volte: il layout a due colonne esce dallo schermo con lo zoom, il menu "Tipologia prestazione" ha 40 voci con codici, e quando preme Invia gli errori compaiono in cima alla pagina, fuori dalla sua vista. Riprova tre volte e chiude l'app. Il rimborso non viene richiesto.

## Dove trovare i tre deliverable

| Deliverable | Dove | Cosa mostrare |
|---|---|---|
| **01 · Persona e barriera** | Presentazione, slide 2-3 · App, scheda "Prima" | "Riproduci il tentativo di Roberto" con "Simula la sua vista" attivo |
| **02 · Percorso assistito** | App, scheda "Dopo" · Presentazione, slide 4-6 | Percorso completo, poi variante "Non ce l'ho adesso" |
| **03 · Autonomia e limiti** | Presentazione, slide 7-9 e 11 · `agents/revisione-umana.md` | Tabella "semplificare senza tradire", limiti, registro di revisione |

## Struttura del repository

```
/
├── app/
│   ├── index.html                 l'app: portale "Prima" + assistente "Dopo" + registro di chi fa cosa
│   ├── server.js                  server locale: collega gli agenti a Claude tramite Claude Agent SDK
│   ├── package.json               dipendenza dal Claude Agent SDK
│   └── esempi/                    fattura e prescrizione fittizie, e lo script che le genera
├── agents/
│   ├── workflow.md                chi fa cosa a ogni passo, con diagramma e piani B
│   ├── revisione-umana.md         dove ha contribuito l'AI e dove serve revisione umana
│   ├── sync_prompts.py            copia prompt, catalogo ed esempi dentro l'app
│   ├── runtime/                   i 4 agenti che lavorano mentre Roberto usa l'app
│   │   ├── 01-lettore-fattura.md
│   │   ├── 02-classificatore-prestazione.md
│   │   ├── 03-verificatore-prescrizione.md
│   │   ├── 04-traduttore-errori.md
│   │   └── catalogo-prestazioni.json
│   └── build/                     la struttura agentica usata per costruire l'app
│       ├── CLAUDE.md              istruzioni di progetto per l'agente di coding
│       ├── commands/              /prova-percorso, /verifica-fedelta
│       └── skills/semplificare-senza-tradire/SKILL.md
├── presentation/
│   └── index.html                 presentazione HTML (frecce per navigare, N per le note, stampabile in PDF)
└── README.md
```

## Come avviarla

**Senza installare nulla.** Aprire `app/index.html` nel browser. Senza connessione all'AI l'app usa risposte preparate per i documenti di esempio e lo dichiara sullo schermo con l'etichetta "Risposta preparata".

**Con l'AI collegata, usando la licenza Claude Code (consigliato per la demo).**

L'app parla con Claude attraverso il [Claude Agent SDK](https://code.claude.com/docs/en/agent-sdk/overview), che usa il login di Claude Code già presente sul computer: non serve nessuna chiave API.

1. Verificare che Claude Code sia installato e collegato: aprire un terminale e scrivere `claude`. Se si apre la sessione senza chiedere di accedere, siete a posto. Altrimenti usare `/login` dentro Claude Code e accedere con il proprio account aziendale.
2. Installare l'SDK e avviare il server (serve Node 18 o superiore):

```bash
cd app
npm install
npm start
# poi aprire http://localhost:8080
```

Il terminale deve mostrare `Modalità: Claude Agent SDK con il login di Claude Code`. Ogni persona avvia il server con il proprio login: il repository non contiene e non deve contenere credenziali. L'uso conta sui limiti della licenza di chi avvia il server.

Gli agenti girano senza strumenti (niente accesso a file, terminale o web), con un solo turno di risposta e senza caricare le impostazioni del progetto: fanno esattamente quello che farebbe una chiamata diretta al modello. Il modello si sceglie con la variabile `MODELLO` (predefinito: `sonnet`).

**In alternativa, con una chiave API della Claude Platform.**

```bash
cd app
MODALITA=api ANTHROPIC_API_KEY=la-vostra-chiave npm start
```

**Sul telefono.** Aperta da smartphone (stessa rete del computer che esegue il server), l'app occupa tutto lo schermo e usa la fotocamera.

**Presentazione.** Aprire `presentation/index.html`. Frecce o clic per navigare, `N` per le note del relatore, stampa del browser per ottenere un PDF.

## Come funziona l'AI, in una riga per agente

| Agente | Fa | Non fa | Piano B senza AI |
|---|---|---|---|
| Lettore fattura | Trascrive i dati della foto in JSON | Scrivere frasi con importi | Roberto scrive i dati, uno per schermata |
| Classificatore | Propone 1 voce su 40 | Scegliere al posto di Roberto | Scelta guidata in 3 domande |
| Verificatore prescrizione | Legge medico, data e prestazione | Decidere la validità | Roberto inserisce la data; la regola la controlla |
| Traduttore errori | Spiega errori non previsti | Nascondere l'originale | Traduzioni revisionate per gli errori noti |

Principio comune: **l'AI propone, Roberto decide**. Numeri e date non passano mai da un testo scritto dal modello: vengono estratti, validati nel formato e formattati da funzioni fisse.

## Modificare i prompt

I prompt si modificano solo nei file `agents/runtime/*.md` (blocco ` ```prompt `). Poi:

```bash
python agents/sync_prompts.py
```

Lo script li copia in `app/index.html` insieme al catalogo e ai documenti di esempio, così i prompt mostrati in presentazione sono quelli che girano davvero.

## Prima del freeze

- [x] Inserire i nomi del team in `README.md` e in `presentation/index.html`
- [ ] Avviare il server con `npm start`, provare il percorso con l'AI collegata e sostituire `RISPOSTE_DEMO` in `app/index.html` con gli output reali ottenuti sui documenti di esempio
- [ ] Compilare le colonne "Chi" ed "Esito" in `agents/revisione-umana.md`
- [ ] Provare l'app su un telefono vero con zoom al 300%
- [ ] Verificare che l'uso del nome UniSalute in un repository pubblico sia consentito
