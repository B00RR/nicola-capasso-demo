# nicola-capasso-demo

Prototipo editoriale di presentazione per Nicola Capasso.

## Stato attuale approvato

La pagina principale è `public/index.html`.

Anteprima pubblica: https://b00rr.github.io/nicola-capasso-demo/

- Italiana Regular 400 per il nome e i titoli editoriali.
- Space Grotesk Light 300 per testo e interfaccia.
- Solo il nome ha un lieve ispessimento grafico, proporzionale alla dimensione del carattere su desktop e mobile.
- Fotografie animate a colori, passaggio compatto al manifesto, guida senza barra di avanzamento e freccia che scompare all'ingresso del secondo blocco.
- Font locali caricati tramite FontFace API, senza dichiarazioni CSS `@font-face` e senza richieste a servizi di font esterni.

Dettagli e fonte locale: [docs/STATO-ATTUALE.md](docs/STATO-ATTUALE.md).

## Verifica

```sh
python -m pip install playwright==1.55.0
python -m playwright install chromium
python .github/scripts/verify_site.py
```

Per usare un browser Chromium già installato, impostare `BROWSER_PATH` al percorso dell'eseguibile. La verifica copre sette viewport, movimento ridotto, font e pesi effettivamente caricati, proporzioni del nome, transizione fotografica, guida, immagini e pubblicazione sotto il percorso GitHub Pages del repository.

Le PR devono superare la verifica prima del merge. Il workflow pubblica `public/` su GitHub Pages soltanto da `main`; il sito WordPress su Aruba non viene modificato.
