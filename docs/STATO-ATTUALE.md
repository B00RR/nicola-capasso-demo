# Stato attuale del prototipo

## Aggiornamento approvato 05/10/2026

La sincronizzazione include tutte le modifiche offline approvate fino ai pulsanti del diario delle 15:48: raccordo temporale 85 ms, geometria stabile mobile e fascia riservata alla guida; nome/foto da progress .01 e ritratto da .02; movimento .19–.34, rotazione .24–.38 e passaggio immediato all'introduzione alla griglia completa .38, senza scroll automatico.

mobile.css migliora leggibilità, navigazione affiancata e viewer. azioni.css applica il riempimento fluido bianco/antracite a tutte le CTA e ai tasti di navigazione approvati, preservando dimensioni compatte, focus visibile e movimento ridotto. I controlli fotografici/viewer non vengono trasformati in CTA. La fonte aveva superato 48 record pagina/configurazione, 132 stati di riempimento e interazioni delle 10 storie.

Manifesto dei 33 file importati: MANIFEST-PUBBLICAZIONE.json. Nessuna anteprima rifiutata, pagina demo dei tasti, backup o brochure è pubblicata. Push diretto su main autorizzato esplicitamente per questa sincronizzazione.

## Fonte approvata

La copia locale selezionata è `Prototipi Nicola Capasso/16 - Stato attuale portfolio e storie/sito/`.

Tutte le 12 pagine HTML sono importate in `public/`: l’unica modifica al contenuto è l’adattamento dei percorsi `../assets/` a `assets/`. Le fotografie, i font e il loader vengono copiati dalla stessa fonte. Il CSS completo della homepage contiene lo stile inline, mobile.css e azioni.css, nello stesso ordine e senza alterarne le regole.

Le versioni precedenti, i confronti grafici, le verifiche locali e i materiali di lavoro della brochure non vengono pubblicati. Il progetto WordPress e il suo riferimento congelato restano separati.

## Pagine e navigazione

- Homepage con 10 immagini collegate alle rispettive storie.
- Portfolio essenziale e 10 pagine storia con galleria e ingrandimento.
- Collegamento «Tutte le storie» dopo la griglia completa.
- «Hompage» in Portfolio e nelle storie; due ritorni «Portfolio» in ogni storia.
- «Prossima Storia» senza miniatura o titolo aggiuntivo, con ritorno dalla decima alla prima.
- Nessun ripristino di toolbar, didascalie, separatori, footer provvisorio o note di prototipo.

Le fotografie e le raccolte rimangono segnaposto. Le pagine non costituiscono un inventario verificato di dieci servizi matrimoniali.

## Tipografia e proporzioni

Italiana Regular 400 per nome, titoli e collegamenti editoriali; Space Grotesk 300 desktop / 400 mobile per il testo. Il nome conserva stroke `.016em` e tracking `.015em`: non viene simulato un peso Bold ufficiale del font.

I paragrafi delle storie e della sezione personale sono a 16px, con interlinea 1.75. Titoli e distanze sono responsive. I ritorni a capo editoriali restano su desktop e vengono lasciati fluire naturalmente su mobile.

Solo su mobile, la dimensione del nome iniziale è `calc(var(--portrait-height)*.17)`: il rapporto tra larghezza del nome e fotografia è circa 1.63, come nel desktop di riferimento. La fotografia non viene ridimensionata o riposizionata da questa correzione.

## Fotografie e testi

Le 12 immagini dell’animazione sono a colori e senza `box-shadow`; l’immagine centrale conserva il proprio trattamento. Movimento, sequenza, guida e transizione fotografica sono quelli della fonte locale approvata.

L’introduzione è: «Due mani unite, la luce di uno sguardo, l’amore che rende ogni istante soltanto vostro.»

Le storie parlano del matrimonio e dell’amore della coppia, non della proposta o delle fasi prematrimoniali. Sono incluse anche le correzioni puntuali successive: eliminazione del riferimento alle mani nella prima storia e in «La vostra promessa», e sostituzione della frase «con il cuore vicino al cuore».

## Verifiche già eseguite in locale

Durante il lavoro sono state controllate tutte le 12 pagine su desktop e mobile, comprese larghezze fino a 320px, schermi orizzontali e movimento ridotto. Sono stati verificati leggibilità, spaziature, overflow, immagini, navigazione e comportamento delle gallerie. Le modifiche successive al nome e alle ombre sono state confrontate con la versione precedente, preservando geometria della fotografia e animazione.

Questa sincronizzazione controlla la corrispondenza dei file importati con la fonte, sintassi e whitespace, poi esegue i test sul pacchetto reale. Il workflow GitHub Pages resta attivo; le aspettative per fogli condivisi, pesi mobile e scheduler animazione sono aggiornate. Commit remoto e deploy sono verificati separatamente sullo SHA effettivo. Verifiche Edge/Chromium su Windows e Chromium in CI, non Safari/iPhone reale. WordPress resta invariato.

Pubblicazione: https://b00rr.github.io/nicola-capasso-demo/

Il sito WordPress attivo su Aruba non viene modificato.
