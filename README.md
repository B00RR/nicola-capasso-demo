# nicola-capasso-demo

Prototipo editoriale di presentazione per Nicola Capasso.

## Stato attuale approvato

Anteprima pubblica: https://b00rr.github.io/nicola-capasso-demo/

Home e Portfolio presentano sei matrimoni: Amalfi, Amalfi, Lake Como, Positano, Scala e Scala. Le gallerie IT/EN contengono 127 fotografie, senza testo narrativo. I due matrimoni di Amalfi e i due di Scala hanno pagine distinte. Ogni copertina proviene dal relativo album. L’apertura animata resta invariata.

Questa è solo la demo statica: nessun aggiornamento del sito WordPress attivo su Aruba.

Dettagli e fonte locale: [docs/STATO-ATTUALE.md](docs/STATO-ATTUALE.md).

## Verifica e pubblicazione

Le modifiche visive sono verificate sulla fonte locale e sul pacchetto importato. La pubblicazione passa da un branch dedicato e una PR con verifiche verdi prima del merge. Il manifest registra tutti i file serviti; le verifiche includono riferimenti, immagini, navigazione e 404. Anteprime rifiutate e backup restano locali. Verifiche Chromium/Edge, non Safari/iPhone reale. Nessuna build TypeScript è prevista per questo repository statico.

Per eseguire successivamente la verifica del repository:

```sh
python -m pip install playwright==1.55.0
python -m playwright install chromium
python .github/scripts/verify_site.py
```

Per un browser Chromium già installato è possibile impostare `BROWSER_PATH` al percorso dell’eseguibile.
