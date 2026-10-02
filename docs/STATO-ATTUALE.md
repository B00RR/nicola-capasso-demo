# Stato attuale del prototipo

## Fonte approvata

La copia locale selezionata è `Prototipi Nicola Capasso/16 - Stato attuale portfolio e storie/sito/`.

Tutte le 12 pagine HTML sono importate in `public/`: l’unica modifica al contenuto è l’adattamento dei percorsi `../assets/` a `assets/`. Le fotografie, i font e il loader vengono copiati dalla stessa fonte. Il CSS completo della homepage viene esportato dal suo stile inline, senza alterarne le regole.

Le versioni precedenti, i confronti grafici, le verifiche locali e i materiali di lavoro della brochure non vengono pubblicati. Il progetto WordPress e il suo riferimento congelato restano separati.

## Pagine e navigazione

- Homepage con 10 immagini collegate alle rispettive storie.
- Portfolio essenziale e 10 pagine storia con galleria e ingrandimento.
- Collegamento «Tutte le storie» dopo la griglia completa.
- «Torna alla homepage» in Portfolio e nelle storie; due ritorni al Portfolio in ogni storia.
- «La prossima storia» senza miniatura o titolo aggiuntivo, con ritorno dalla decima alla prima.
- Nessun ripristino di toolbar, didascalie, separatori, footer provvisorio o note di prototipo.

Le fotografie e le raccolte rimangono segnaposto. Le pagine non costituiscono un inventario verificato di dieci servizi matrimoniali.

## Tipografia e proporzioni

Italiana Regular 400 per nome, titoli e collegamenti editoriali; Space Grotesk Light 300 per il testo. Il nome conserva stroke `.016em` e tracking `.015em`: non viene simulato un peso Bold ufficiale del font.

I paragrafi delle storie e della sezione personale sono a 16px, con interlinea 1.75. Titoli e distanze sono responsive. I ritorni a capo editoriali restano su desktop e vengono lasciati fluire naturalmente su mobile.

Solo su mobile, la dimensione del nome iniziale è `calc(var(--portrait-height)*.17)`: il rapporto tra larghezza del nome e fotografia è circa 1.63, come nel desktop di riferimento. La fotografia non viene ridimensionata o riposizionata da questa correzione.

## Fotografie e testi

Le 12 immagini dell’animazione sono a colori e senza `box-shadow`; l’immagine centrale conserva il proprio trattamento. Movimento, sequenza, guida e transizione fotografica sono quelli della fonte locale approvata.

L’introduzione è: «Due mani unite, la luce di uno sguardo, l’amore che rende ogni istante soltanto vostro.»

Le storie parlano del matrimonio e dell’amore della coppia, non della proposta o delle fasi prematrimoniali. Sono incluse anche le correzioni puntuali successive: eliminazione del riferimento alle mani nella prima storia e in «La vostra promessa», e sostituzione della frase «con il cuore vicino al cuore».

## Verifiche già eseguite in locale

Durante il lavoro sono state controllate tutte le 12 pagine su desktop e mobile, comprese larghezze fino a 320px, schermi orizzontali e movimento ridotto. Sono stati verificati leggibilità, spaziature, overflow, immagini, navigazione e comportamento delle gallerie. Le modifiche successive al nome e alle ombre sono state confrontate con la versione precedente, preservando geometria della fotografia e animazione.

Questa sincronizzazione non rilancia tali test locali, secondo la richiesta dell’utente. Controlla invece la corrispondenza dei file importati con la fonte e la presenza della revisione su `main`. Il workflow GitHub Pages esistente viene mantenuto; le sue aspettative obsolete (quattro fotografie e vecchio font delle CTA) sono aggiornate al prototipo corrente.

Pubblicazione: https://b00rr.github.io/nicola-capasso-demo/

Il sito WordPress attivo su Aruba non viene modificato.
