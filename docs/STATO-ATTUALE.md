# Stato attuale del prototipo

## Fonte approvata

La versione corrente locale si trova nella cartella `Prototipi Nicola Capasso/13 - Stato attuale tipografia omogenea/sito/index.html`.

`public/index.html` riproduce questa fonte: l'unica differenza nell'HTML è l'adattamento dei percorsi `../assets/` a `assets/` per la pubblicazione. Il loader dei font risolve i file rispetto al proprio URL, così funziona sia come anteprima locale sia sotto il percorso del repository su GitHub Pages.

In locale rimangono solo la versione corrente (cartella 13) e il backup immediatamente precedente (`12 - Prova nome leggermente più marcato/sito/index.html`). I vecchi prototipi e confronti sono stati rimossi dalla cartella di lavoro. Il progetto WordPress, con piani e riferimento congelato, è stato conservato separatamente nella cartella `Progetto WordPress Nicola Capasso` sul Desktop; non viene sostituito automaticamente dal prototipo attuale.

## Tipografia

- Nome e titoli di sezione: Italiana, peso reale 400.
- Testo e UI: Space Grotesk, peso reale 300.
- Nome leggermente più marcato tramite `-webkit-text-stroke: .016em currentColor`; non è un peso Bold ufficiale di Italiana.
- Tracking del nome: `.015em` sia su desktop sia su mobile.
- Nessun minimo fisso in pixel per lo stroke: il rapporto tra spessore aggiunto e dimensione del carattere resta uguale su tutti gli schermi.
- Dimensioni responsive e fotografia conservate: omogeneità del disegno tipografico non significa identica composizione o identico ingombro rispetto al ritratto su telefono e PC.
- Solo il nome riceve l'ispessimento; i titoli editoriali rimangono Regular senza stroke.

Il font viene caricato da due file locali attraverso `assets/fonts/load-fonts.js`, con le licenze OFL incluse. Questo caricamento richiede JavaScript, come le animazioni del prototipo. Non sono necessari servizi esterni di font.

Le regole tipografiche sono esportate in `public/tipografia.css`; il CSS completo è esportato in `public/stili-completi.css` e verificato uguale al CSS inline della pagina.

## Esperienza conservata

Fotografie animate a colori, nome scuro fisso senza inversione cromatica, transizione compatta al manifesto, guida visibile e senza barra di avanzamento. La scritta della guida sfuma con nome e ritratto; la freccia rimane nella sequenza e scompare quando entra il secondo blocco, ricomparendo scorrendo indietro. Rimangono invariati contenuti e ritagli delle fotografie.

## Verifiche di rilascio

La suite controlla i viewport 320×568, 390×844, 700×900, 701×900, 844×390, 1440×900 e 1920×1080, anche con movimento ridotto. Include font effettivamente caricati, pesi, tracking/stroke normalizzati, assenza di overflow, separazione tra ritratto/frase/guida, uscita e ritorno della freccia, continuità foto/testo, immagini e galleria, sintassi JavaScript e caricamento via HTTP sotto il percorso GitHub Pages.

Pubblicazione: https://b00rr.github.io/nicola-capasso-demo/

Questa pubblicazione riguarda il prototipo GitHub Pages, non il sito WordPress attivo su Aruba.
