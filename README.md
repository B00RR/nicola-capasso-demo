# nicola-capasso-demo

Prototipo editoriale di presentazione per Nicola Capasso.

## Stato attuale approvato

Anteprima pubblica: https://b00rr.github.io/nicola-capasso-demo/

Aggiornamento approvato 05/10/2026: apertura fotografica anticipata, raccordo 85 ms, geometria stabile al resize mobile, guida separata dalle foto e passaggio immediato dalla griglia all'introduzione. Aggiunti i fogli condivisi mobile.css e azioni.css, con riempimento fluido bianco/antracite per CTA, Portfolio, Hompage, Prossima Storia e Tutte le storie. Etichette e destinazioni approvate conservate; navigazione compatta.

- Homepage `public/index.html` con 10 fotografie collegate alle rispettive storie e collegamento «Tutte le storie» dopo la griglia.
- Portfolio `public/portfolio.html` e 10 pagine dedicate, da `storia-01.html` a `storia-10.html`.
- Pagina 404 approvata `public/404.html`: «Fuori inquadratura.», numero davanti alla fotografia e collegamenti Hompage/Portfolio. Nessun nome, motto, etichetta aggiuntiva o didascalia. I percorsi assoluti del progetto mantengono font, foto e collegamenti funzionanti anche su URL inesistenti annidati e senza JavaScript; il salto al contenuto resta nella 404 corrente.
- Galleria essenziale: fotografie cliccabili senza didascalie, barre strumenti o intestazioni aggiuntive.
- Ritorni testuali a homepage e Portfolio; storia successiva solo testo, con ciclo dall’ultima alla prima; ingrandimento delle fotografie.
- Italiana Regular 400 per nome, titoli e collegamenti editoriali; Space Grotesk 300 desktop / 400 mobile per paragrafi e interfaccia. Font locali e licenze inclusi.
- Paragrafi a 16px, titoli responsive, spaziature riviste e a capo naturali su mobile.
- Testi dedicati al matrimonio e all’amore della coppia, con le ultime correzioni editoriali della fonte locale.
- Le 12 fotografie dell’animazione iniziale sono a colori e senza ombre esterne. Movimento e transizione all’introduzione conservati.
- Su mobile la dimensione del nome è proporzionata alla fotografia come su desktop; fotografia e composizione desktop invariate.
- Footer provvisorio e note di prototipo non presenti nelle pagine.

Le fotografie e le raccolte sono ancora segnaposto: non attestano dieci servizi fotografici distinti. Questa pubblicazione aggiorna il prototipo GitHub Pages, non il sito WordPress attivo su Aruba.

Dettagli e fonte locale: [docs/STATO-ATTUALE.md](docs/STATO-ATTUALE.md).

## Verifica e pubblicazione

Le modifiche visive sono verificate sulla fonte locale e sul pacchetto importato. La nuova 404 viene pubblicata tramite branch dedicato e PR, con verifiche verdi prima del merge; il precedente push diretto era autorizzato solo per quella sincronizzazione. Il workflow esistente resta attivo. `docs/MANIFEST-PUBBLICAZIONE.json` registra gli hash dei 34 file importati, comprese le 13 pagine. Restano tutte le verifiche delle 12 pagine precedenti, più test specifici HTTP 404 su percorsi annidati, font/foto, tastiera, riempimento, navigazione e JavaScript disabilitato. Anteprime rifiutate e backup restano locali. Verifiche Chromium/Edge, non Safari/iPhone reale. Nessuna build TypeScript è prevista per questo repository statico.

Per eseguire successivamente la verifica del repository:

```sh
python -m pip install playwright==1.55.0
python -m playwright install chromium
python .github/scripts/verify_site.py
```

Per un browser Chromium già installato è possibile impostare `BROWSER_PATH` al percorso dell’eseguibile.
