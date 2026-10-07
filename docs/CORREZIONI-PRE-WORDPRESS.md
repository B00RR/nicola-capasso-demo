# Correzioni pre-WordPress — report delle verifiche locali

Questo report descrive lo stato al termine delle verifiche locali, prima dell'autorizzazione alla pubblicazione. Pubblicazione successivamente autorizzata tramite PR https://github.com/B00RR/nicola-capasso-demo/pull/5 ; stato di merge e deploy da verificare separatamente, non deducibile da questo report storico.

Base: `B00RR/nicola-capasso-demo`, `bae4b394481f44d616aff4f35162bf60103d7265`.
Branch isolato: `fix/pre-wordpress-audit`. Nessuna modifica al tema WordPress online; squadra e conversione restano ferme. Nessun push o nuovo deploy.

## Modifiche
- B1: contenuti `.reveal` visibili per impostazione predefinita; attivazione dell'animazione solo dopo inizializzazione riuscita e con preferenza di movimento normale. Fallback homepage no-JS e font locali via `@font-face` CSS sulle 32 pagine che dipendevano dal loader. Le due 404 avevano già font CSS e fallback propri.
- B2: dimensioni intrinseche della foto sguardo e `height:auto`; spazio riservato prima del download senza cambiare il ritaglio o il layout finale.
- B3: nomi accessibili dai titoli approvati sulle tre schede vuote in entrambe le homepage; nessuna foto o scritta visibile reintrodotta.
- O1: 36 derivati WebP qualità 95 (384/768/1152), `srcset/sizes` conservativi per crop e trasformazioni. JPEG esistenti mantenuti come fallback; album e originali intatti.
- O2: tre stylesheet condivisi per storie, Portfolio e Contatti, inseriti nella medesima posizione della cascata. Eliminati 193.509 byte di duplicazione CSS inline al netto dei fogli condivisi, non un risparmio equivalente per singolo accesso.

## Risultati reali
- Tutti i test esistenti PASS: sito/risorse/404, CTA e centratura solo-mobile, 254 fotografie/ordine/storie IT-EN, contatti statici, footer.
- Nuovo `verify_audit_fixes.py` PASS; aggiunto al workflow di verifica (non avviato su GitHub).
- No-JS IT/EN: foto/testo/CTA visibili, due font locali caricati, link alle storie 08–10 nominati. Simulato errore iniziale dello script: il testo sguardo rimane visibile.
- Download ritardato della foto: altezza 491,4375 px su mobile 390 e 620 px su desktop 1440 prima/dopo; spostamento della CTA 0 px nelle quattro prove IT/EN.
- Le 12 immagini selezionate dal browser a 390 px pesano 630.596 byte a DPR1 (-84,1%), 1.806.252 a DPR2 (-54,5%), 1.864.362 a DPR3 (-53,1%), contro 3.972.613 byte dei JPEG originali. Dipende da viewport/DPR e scelta del browser; non è un miglioramento equivalente del tempo totale di caricamento.
- 16 confronti di geometria/testi/tipografia fra baseline e copia corretta su Home, Portfolio, storia01 e Contatti, IT/EN, 390/1440: PASS con tolleranza <0,1 px. Posizioni/trasformazioni/ritagli delle 12 immagini animate invariati a 390/1440. Confronti visivi interni: nessun cambiamento evidente di composizione o qualità alla dimensione d'uso; i derivati non sono pixel-identici ai JPEG.
- Tutti i 276 asset preesistenti preservati byte per byte; nessuna fotografia originale cancellata o sovrascritta.
- `git diff --check`: PASS. Verifiche sintattiche Python e JavaScript PASS durante esecuzione/suite.

Evidenze: `AUDIT-FIXES.json`, `AUDIT-REGRESSION.json`, verifiche geometriche interne. Copia durevole proposta: `consegne/correzioni-pre-wordpress/sito/` nel progetto, senza promuoverla a baseline ufficiale prima della pubblicazione approvata.

La pubblicazione GitHub/Pages e la nuova baseline restano separate; il precedente errore di avvio del workflow non è stato risolto da questo intervento sul frontend. Non è una certificazione su iPhone/Safari reale o del futuro backend WordPress.
