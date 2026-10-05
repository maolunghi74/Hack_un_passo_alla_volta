---
description: Percorre il percorso assistito come lo farebbe Roberto e segnala ogni punto in cui si bloccherebbe
---

# /prova-percorso

Apri `app/index.html` con un browser headless a 390×844 px e zoom di pagina al 300%. Percorri la scheda "Con l'assistente" dall'inizio alla fine in tre scenari:

1. **Percorso completo**: fattura di esempio, conferma, voce proposta accettata, prescrizione di esempio, conto confermato, invio.
2. **Prescrizione mancante**: come sopra, ma scegli "Non ce l'ho adesso" al passo della prescrizione.
3. **AI non disponibile**: blocca le chiamate di rete e ripeti lo scenario 1.

Per ogni schermata verifica e riporta in una tabella:

- c'è scorrimento orizzontale? (deve essere no)
- la domanda è nella parte visibile senza scorrere? (deve essere sì)
- il testo più piccolo è almeno 24px?
- il pulsante principale è alto almeno 64px?
- se compare un errore, è dentro la schermata attuale?
- "Ripeti" legge il testo della schermata?

Chiudi con l'elenco dei punti in cui Roberto si bloccherebbe e una proposta di correzione per ciascuno. Non correggere il codice senza conferma del team.
