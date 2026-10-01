# Test rapido del traduttore del tema attivo

Tema letto: nicola-capasso-photo-v1324, versione dichiarata 1.3.24.
Nessun file del tema o contenuto del sito modificato. Richieste AJAX di sola traduzione autorizzate dall'utente; nessun salvataggio editoriale.

## Test attraverso WordPress / Aruba

Quattro richieste al gestore esistente nc_translate_text, con testi di prova non personali:

| Testo | HTTP | Esito | Tempo ms |
|---|---|---|---|
| Raccontami il vostro matrimonio. | 500 | Risposta di traduzione non valida. | 860 |
| Fotografo matrimoni in Costiera Amalfitana. Lavoro anche all’estero. Raccontami la vostra storia. | 500 | Risposta di traduzione non valida. | 824 |
| Nicola Capasso fotografa ad Amalfi e Ravello, con discrezione e attenzione ai dettagli. | 500 | Risposta di traduzione non valida. | 789 |
| Raccontami il vostro matrimonio. | 500 | Risposta di traduzione non valida. | 732 |

La traduzione non funziona nel percorso WordPress testato. Non è nota la risposta HTTP/body ricevuta da Aruba verso Google: non attribuire il fallimento a quota, blocco IP o firewall senza ulteriori prove. Questo campione non misura disponibilità a lungo termine.

## Confronto dall'ambiente locale

Richieste dirette allo stesso endpoint Google, senza chiave, con client=gtx, sl=it, tl=en, dt=t:
- Frase breve: HTTP 200, 624 ms, risposta «Tell me about your wedding.».
- Tre frasi: HTTP 200, 964 ms, tre segmenti separati: «Wedding photographer on the Amalfi Coast. », «I also work abroad. », «Tell me your story.».

Il gestore PHP letto prende soltanto $data[0][0][0]. Per la risposta multi-frase osservata questo conserverebbe soltanto il primo segmento: difetto di completezza distinto dal fallimento attuale su Aruba. Il JS attuale mostra un errore generico se data.data è una stringa anziché un oggetto con message.

## Limiti

Non è stata trovata una quota ufficiale documentata per il percorso translate_a/single?client=gtx. Non applicare a questo percorso i limiti di Google Cloud Translation.
La documentazione Google Cloud dichiara per la traduzione NMT standard i primi 500.000 caratteri mensili gratuiti come credito, e quote configurabili per le API ufficiali v2/v3. Riferimenti: https://cloud.google.com/products/translate/pricing e https://docs.cloud.google.com/translate/quotas .

## Conclusione del primo test

Il percorso via PHP/Aruba fallisce nel percorso live testato e il parser troncherebbe una risposta a più segmenti. Il tema attivo non va modificato senza nuova autorizzazione esplicita.

## Aggiornamento: percorso browser verificato

Il cliente rifiuta la creazione di Google Cloud e sceglie di mantenere l'endpoint senza chiave. Una prova comparativa con User-Agent WordPress e User-Agent diagnostico dal PC restituisce HTTP 200 in entrambi i casi: non attribuire il difetto a User-Agent senza prova lato Aruba.

Due richieste effettuate direttamente dal browser sulla sessione WordPress, con credentials=omit e referrerPolicy=no-referrer, senza salvare contenuti:
- «Raccontami il vostro matrimonio.»: HTTP 200, 218 ms; un segmento; «Tell me about your wedding.».
- «Fotografo matrimoni in Costiera Amalfitana. Lavoro anche all’estero. Raccontami la vostra storia.»: HTTP 200, 461 ms; tre segmenti; «Wedding photographer on the Amalfi Coast. I also work abroad. Tell me your story.».

Il browser può leggere la risposta cross-origin nel contesto testato. Questo prova una strada alternativa funzionante senza passare dalla chiamata PHP di Aruba, ma non identifica il motivo preciso del precedente errore server e non è una garanzia di disponibilità futura. La versione PHP attiva è rimasta intatta.

Proposta per il nuovo tema: traduzione nel pannello amministrativo via browser allo stesso endpoint fisso; unire tutti i segmenti; controllare risposta HTTP/struttura; timeout, una richiesta alla volta e recupero errori; nessuna rotazione IP/proxy o aggiramento di blocchi; conservare le traduzioni già salvate e le bozze in caso di errore. Il salvataggio WordPress mantiene autorizzazioni, nonce e validazione; non tradurre a ogni visita. Prima di pubblicare verificare anche CSP, browser supportati, privacy e trattamento dei testi inviati a Google. Nessun account Cloud richiesto per questa modalità, nessuna promessa di disponibilità o quota ufficiale.
