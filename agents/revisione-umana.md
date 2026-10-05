# Dove ha contribuito l'AI e dove serve revisione umana

Questo registro risponde al vincolo della challenge "indicare dove l'AI ha contribuito e dove è stata necessaria revisione umana". Le righe con esito vuoto vanno compilate dal team durante le 3 ore: una revisione non fatta si lascia vuota, non si spunta.

## 1. AI nel prodotto (mentre Roberto usa l'app)

| Dove | Cosa fa l'AI | Cosa NON le lasciamo fare | Rete di sicurezza |
|---|---|---|---|
| Lettura fattura | Trascrive dati dalla foto in JSON | Scrivere frasi con importi | Frasi composte dal codice; Roberto conferma |
| Voce del modulo | Propone 1 voce su 40 con spiegazione | Scegliere al posto di Roberto | Codice validato sul catalogo; scelta guidata senza AI |
| Prescrizione | Legge medico, data, prestazione; valuta coerenza | Decidere la validità temporale | Regola fissa sulla data |
| Errori non previsti | Traduce in linguaggio semplice | Nascondere l'originale, promettere esiti | Originale sempre visibile |

## 2. AI nella costruzione (agentic coding)

| Artefatto | Prodotto con | Revisione umana richiesta | Chi | Esito |
|---|---|---|---|---|
| Struttura dell'app e flusso a passi | Claude (agentic coding) | Prova del percorso completo a zoom 300% su telefono reale | | |
| Prompt dei 4 agenti | Claude, su istruzioni del team | Lettura riga per riga; prova su almeno 5 fatture diverse | | |
| Catalogo delle 40 voci | Claude (ricostruzione dimostrativa) | Confronto con il catalogo reale del piano, se disponibile | | |
| Testi rivolti a Roberto | Claude con skill `semplificare-senza-tradire` | `/verifica-fedelta` + lettura ad alta voce da parte di un membro del team | | |
| Traduzioni degli errori noti (`ERRORI_NOTI`) | Claude | Confronto con il significato dell'errore originale | | |
| Regola "prescrizione obbligatoria" e regola sulla data | Team, implementata da Claude | Verifica sulle condizioni del piano sanitario | | |
| Documenti di esempio (fattura, prescrizione) | Script Python generato da Claude | Verifica che non contengano dati reali | | |

## 3. Decisioni prese da persone, non dall'AI

- Chi è Roberto e quale barriera affrontare.
- Cosa non si semplifica mai: importi, date, obblighi, esiti.
- Che l'AI propone e Roberto decide, a ogni passo.
- Quali casi restano fuori perimetro (ricoveri, cure dentarie a più sedute, cambio IBAN).
