# Stato attuale del prototipo

## 05/10 17:34 — Pagina 404 approvata

La 404 «Fuori inquadratura.» è ora parte dello stato attuale approvato. Il numero 404 è davanti alla fotografia, senza spostamenti o cambiamenti di dimensione; nome in alto, motto, etichetta e didascalia sono rimossi. Restano il titolo, il testo esplicativo e le azioni Hompage/Portfolio con riempimento fluido. Fonte: `16 - Stato attuale portfolio e storie/sito/404.html`, verificata prima/dopo su 13 configurazioni; nessuna differenza di geometria dei contenuti rimasti.

Il pacchetto comprende 13 pagine e 34 file nel manifesto. I 33 file precedenti restano identici. Nella sola 404 pubblicata si adattano i percorsi delle immagini/font e delle due azioni al prefisso assoluto `/nicola-capasso-demo/` per funzionare su URL inesistenti a qualsiasi profondità, anche senza JavaScript. Non si aggiunge un elemento base: il collegamento `#contenuto` deve restare nella pagina di errore corrente. Nessuna modifica al design approvato o al CSS della homepage.

Pubblicazione autorizzata tramite una nuova PR; verifiche del pacchetto, CI e deploy sullo SHA effettivo. I test precedenti di homepage, Portfolio e dieci storie rimangono attivi, affiancati da verifiche dedicate della risposta HTTP 404 e dei relativi collegamenti. L'approvazione riguarda il prototipo GitHub Pages, non attivazione o modifica del tema WordPress/Aruba.

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
