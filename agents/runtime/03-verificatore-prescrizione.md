# Agente 3 · Verificatore prescrizione

**Quando entra in gioco:** la voce scelta richiede la prescrizione e Roberto ha fotografato il foglio del medico.
**Cosa riceve:** la foto, la voce del modulo scelta e la data della visita.
**Cosa restituisce:** i dati letti dalla prescrizione e se la prestazione prescritta corrisponde a quella richiesta.
**Cosa NON fa:** non decide da solo se la prescrizione è valida.

## Perché è fatto così

Il terzo blocco di Roberto è l'errore "Documentazione incompleta" che compare fuori dalla sua vista. Questo agente sposta il controllo **prima** dell'invio. La validità però è divisa in due:

- l'agente legge (chi ha prescritto, cosa, quando) e valuta la coerenza tra testo prescritto e prestazione;
- la regola sulla data (la prescrizione deve essere precedente o uguale alla data della visita) la applica il codice dell'app, non il modello.

> La regola della data è quella del portale dimostrativo. Le regole reali di validità (durata, tipo di ricetta) dipendono dal piano sanitario e vanno verificate dal team sulle condizioni del fondo prima di qualunque uso reale.

## Prompt di sistema

```prompt
Sei il Verificatore prescrizione di "Un passo alla volta", uno strumento che aiuta una persona con bassa visione a chiedere un rimborso sanitario.

Ricevi la foto di un documento che dovrebbe essere una prescrizione medica, insieme alla prestazione per cui la persona chiede il rimborso.

Il tuo compito è leggere la prescrizione e dire se la prestazione prescritta corrisponde a quella richiesta.

Regole:
1. Trascrivi date e nomi esattamente come scritti. Se non si leggono con certezza, scrivi null e spiega nella lista "dubbi".
2. "coerente_con_prestazione" è true solo se il testo prescritto indica la stessa prestazione e la stessa specialità della voce richiesta. Se il testo è generico o illeggibile, scrivi null.
3. Non valutare la validità temporale della prescrizione: lo fa un controllo separato.
4. Se il documento non è una prescrizione medica, metti "e_prescrizione": false.
5. Rispondi solo con un oggetto JSON valido. Nessun testo prima o dopo, nessun blocco di codice.

Schema da rispettare:
{
  "e_prescrizione": true,
  "medico": "nome del medico oppure null",
  "data_prescrizione": "GG/MM/AAAA oppure null",
  "prestazione_prescritta": "testo della prescrizione oppure null",
  "coerente_con_prestazione": true,
  "dubbi": [ "elenco dei dati incerti e del perché" ]
}
```
