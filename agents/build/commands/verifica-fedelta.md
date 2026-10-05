---
description: Confronta ogni testo semplificato dell'app con l'informazione originale e segnala i cambi di significato
---

# /verifica-fedelta

Carica la skill `semplificare-senza-tradire`.

Raccogli da `app/index.html` tutti i testi rivolti a Roberto (oggetto `PASSI`, oggetto `ERRORI_NOTI` e funzione `fraseFattura`). Per ognuno individua l'informazione originale a cui corrisponde: un campo del modulo del portale, una voce del catalogo, un messaggio di errore o un dato della fattura.

Produci una tabella con: testo semplice, originale, cosa è stato tolto, esito (fedele / da rivedere / non fedele) e motivo.

Regole:
- Ogni testo che contiene un numero scritto a mano è "non fedele" per definizione: i numeri devono venire dai dati.
- Ogni promessa di esito ("ti rimborseranno", "è tutto a posto") è "non fedele".
- Non riscrivere i testi: segnala e proponi. La decisione finale è di una persona del team, che firma la revisione in `agents/revisione-umana.md`.
