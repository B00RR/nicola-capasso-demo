# Nicola Capasso — conversione WordPress

## Stato e vincoli confermati
- Hosting Aruba, WordPress. Configurazione effettiva da verificare prima di scegliere requisiti PHP/WP.
- Fonte autorevole: copia del prototipo approvato in riferimento-prototipo/sito/index.html.
- Il nuovo progetto deve usare esclusivamente identità e riferimenti del cliente: eliminare qualsiasi riferimento al designer/sito usato come ispirazione (nomi, URL, crediti, commenti, metadati e nomi di file/cartella). Prima della consegna verificare tema, plugin, documentazione e ZIP. Le copie originali esterne al nuovo progetto non vanno rinominate o eliminate senza autorizzazione.
- riferimento-prototipo/ contiene una copia identica dell'HTML e dei 15 asset referenziati. Non modificarla.
- Conservare aspetto, animazioni e comportamento del prototipo approvato.
- Non modificare mai il font Michroma del titolo animato Nicola Capasso senza una nuova autorizzazione esplicita.
- Le foto animate devono mantenere i colori originali (nessuna transizione B/N-colore). La foto centrale mantiene il trattamento attuale.
- Il cliente deve poter modificare testi e immagini di tutte le sezioni, foto centrale, sequenza animata e griglia homepage.
- Gestione ordinata, semplice, con riordino visuale e anteprima.
- Consentire ritaglio/rotazione e mostrare chiaramente la parte visibile/esclusa per ogni utilizzo dell'immagine.
- Non modificare il sito live. Sviluppare e verificare in ambiente separato.
- Procedere per step: conferma delle scelte prima dell'implementazione.
- Vincolo esplicito: non modificare in alcun modo il codice del tema attualmente attivo e non eliminarlo. Il nuovo tema deve avere una cartella/identità separata; conservare quello attuale per il ritorno alla versione precedente. Nessuna attivazione pubblica senza approvazione.
- Il tema conservato non sostituisce un backup completo di database, upload e configurazione: predisporre e verificare backup/ripristino prima della pubblicazione.
- Contatti: modulo richieste a info@nicolacapasso.photo; footer con Instagram, Facebook e WhatsApp. Link letti dal sito: Instagram https://instagram.com/nicolacapassofoto; WhatsApp https://wa.me/393398563098. Facebook non presente nei link della homepage letta: da recuperare nelle impostazioni o confermare, senza inventarlo.

## Pagine confermate
- Homepage.
- Portfolio.
- Contatti.
- Pagina 404 dedicata per URL inesistenti (template di errore, non pagina editoriale).
- Ogni foto della griglia homepage apre la relativa storia, cioè una galleria presente nel Portfolio.
- Le storie/gallerie sono contenuti gestibili dal cliente; la griglia homepage rimanda a questi contenuti.
- Anche nella sequenza animata iniziale il cliente può aggiungere, rimuovere, sostituire e riordinare le immagini. Non fissare il numero attuale come vincolo editoriale; definire e verificare il comportamento dell'animazione con quantità variabili.
- Ogni storia si apre in una pagina dedicata con URL proprio, collegata al Portfolio, non in un overlay.
- La pagina della storia contiene un pulsante esplicito «Torna al Portfolio» che conduce sempre al Portfolio, anche quando la storia viene aperta dalla homepage o da un link diretto; non usare la cronologia del browser come unica navigazione.

## Architettura confermata
Nuovo tema autonomo con frontend e animazioni; gestione dei contenuti direttamente nell'editor standard WordPress delle pagine e delle storie. Nessun pannello personalizzato separato e nessun plugin companion dedicato. Integrare nell'editor i controlli necessari per traduzione, gallerie e ritagli. Conservare codice e impostazioni del tema attualmente attivo; nessuna attivazione pubblica senza approvazione. Libreria Media WordPress per upload e originali; nessun contenuto cliente in Git.

### UX editoriale richiesta
- Editor WordPress italiano chiaro e familiare: blocchi/sezioni riconoscibili per pagina, etichette comprensibili, selettore Media, Anteprima, Salva bozza e Aggiorna/Pubblica. Non creare una schermata di gestione alternativa.
- Il cliente non deve vedere codice, shortcode, nomi tecnici di campi o impostazioni SEO complesse. Funzioni avanzate separate; evitare una singola schermata sovraccarica.
- Foto: selezione da Media, anteprima dell'utilizzo, riordino visuale e controlli espliciti; proporre una modalità di riordino alternativa al trascinamento.
- Prima dell'implementazione completa approvare un prototipo dell'esperienza di modifica dentro l'editor WordPress.

### Editor WordPress e raccolta Media: requisiti confermati
- Le pagine del nuovo sito devono mostrare struttura e contenuti nell'editor standard WordPress, non un foglio bianco perché tutto è generato esclusivamente dal template PHP. Ricostruire sezioni, testi e immagini nell'editor, unico punto di gestione dei contenuti.
- Proporre blocchi/pattern e stili editoriali coerenti col frontend, con strutture protette dove necessario per non rompere il design e contenuti modificabili. Definire una sola fonte dati, senza copie editor/frontend che possano divergere. Verificare inserimento, salvataggio, riapertura e corrispondenza col risultato pubblico in staging.
- Distinguere la rappresentazione editoriale delle sezioni dalla riproduzione delle animazioni: dare un'anteprima frontend delle animazioni, senza promettere che l'editor le riproduca identicamente. Per Portfolio e storie rendere visibili ed editabili contenuti e gallerie; la 404 resta un template di errore con anteprima appropriata, non una pagina pubblicata artificiale.
- Usare le fotografie già presenti nella Libreria Media WordPress, non immagini stock o segnaposto per la consegna. Inventariare tutte le fotografie e rendere conto di ciascuna: assegnata a storia/coppia, ritratto/autore/altro uso, duplicato o da confermare. Non cancellare o escludere foto silenziosamente e non confondere loghi/iconografie con foto di coppie.
- Una storia Portfolio per coppia/servizio. Recuperare anzitutto associazioni dalle storie/gallerie esistenti, ID allegati, nomi file/cartelle, descrizioni e metadati affidabili; raggruppamenti dubbi vanno presentati per conferma, non inventati. Non affidarsi al solo riconoscimento dei volti.
- Conservare originali, allegati, URL, gallerie e contenuti del sito attuale. Predisporre la mappatura nel nuovo ambiente senza alterare il database live per organizzare i gruppi. Non ricaricare duplicati inutili.
- Verificare completezza programmaticamente sull'inventario persistito: numero foto censite, assegnate, duplicate e da confermare. Separare «tutte le foto organizzate» da «tutte le foto mostrate nella homepage»; non cambiare composizione/animazioni per pubblicare ogni immagine nella stessa pagina.

### Bilinguismo e modalità di traduzione confermati
- Italiano e inglese sono requisiti essenziali. Se la lingua principale del browser/device non è italiana, il visitatore deve ricevere inglese automaticamente, senza dover usare uno switcher manuale. Non dedurre la lingua dall'IP.
- Proposta editoriale: Nicola scrive una sola volta in italiano; generare e salvare una traduzione inglese come bozza, senza tradurre a ogni visita. Mostrare stato «Inglese aggiornato / da aggiornare / errore» e anteprima, con modifica inglese facoltativa.
- Preservare eventuali correzioni inglesi manuali: non sovrascriverle silenziosamente. Non alterare nomi, contatti, località, URL o fatti commerciali durante la traduzione.
- Proposta salvataggio: prima salvare la bozza italiana, poi tradurre; pubblicare la coppia IT/EN aggiornata insieme. In caso di errore mantenere le versioni pubbliche precedenti, conservare la bozza e offrire «Riprova», senza perdere testo o bloccare il pannello.
- Scelta aggiornata del cliente: usare l'endpoint Google Translate senza chiave già presente nel vecchio tema; non creare account Google Cloud. La chiamata dal browser amministrativo è riuscita in due prove, mentre il percorso PHP Aruba esistente fallisce: proporre il percorso browser nel nuovo tema, unire tutti i segmenti, salvare traduzioni solo in WordPress con permessi/nonce, timeout ed errori non distruttivi. Non dichiarare risolta la causa lato server né garantire quota/disponibilità del servizio. Dettagli e risultati in docs/TEST-TRADUZIONE.md. Il tema attivo resta intatto.
- SEO: mantenere URL distinti e accessibili per IT/EN, HTML completo server-rendered e hreflang reciproci. Non forzare redirect su URL linguistici espliciti né usare diversità crawler/utente per aggirare indicizzazione. Progettare e testare l'ingresso neutro con scelta automatica tenendo conto delle raccomandazioni Google contro redirect basati sulla lingua.
- Cache: verificare separazione IT/EN e nessuna variante servita alla lingua sbagliata con Aruba.

Ritaglio per utilizzo: preservare originale; memorizzare inquadratura e rotazione per ogni posizione, non globalmente sulla foto. Anteprima della cornice reale; visualizzazione del fuori-cornice; ripristino. Desktop/mobile separabili dove i rapporti cambiano. Verificare se bastano punto focale e trasformazioni oppure servono derivati fisici. L'editor Media nativo cambia il file condiviso: non usarlo come unica soluzione per ritagli indipendenti.

## Sicurezza come requisito di consegna
- Il cliente gestisce i contenuti dal pannello WordPress, senza modificare codice. Prevedere permessi editoriali dedicati e minimi; gestione installazioni/aggiornamenti riservata all'amministratore/manutentore.
- Non promettere sicurezza assoluta, assenza futura di vulnerabilità o protezione totale dell'hosting. Dare garanzie verificabili su processo, controlli e difetti rilevati; nessuna vulnerabilità critica/alta nota irrisolta nel perimetro verificato al rilascio. Un test superato non prova l'assenza di altre vulnerabilità.
- Codice del nuovo tema e integrazioni editoriali: verificare capability e accesso al singolo contenuto per ogni scrittura, nonce contro CSRF (non come autorizzazione), permission_callback REST, validazione/sanitizzazione input, escaping contestuale output, API WordPress/query preparate, upload con tipi/dimensioni consentiti e originali protetti; nessun eval/codice arbitrario o segreto nel frontend/repository.
- Modulo contatti: validazione lato server, protezione anti-abuso con limiti di invio, gestione sicura header email, nessuna esposizione pubblica dei messaggi o dati personali; verificare invio e comportamento sotto abuso in ambiente di test.
- Verifiche pre-rilascio: revisione indipendente del codice, analisi dipendenze, test funzionali e negativi come anonimo/utente senza permessi/editor, tentativi XSS/CSRF/accesso indebito e upload non consentiti, compatibilità hosting e backup/ripristino. Eseguire test offensivi soltanto nell'ambiente di prova autorizzato, non sul sito live.
- Hardening installazione/hosting da verificare separatamente: HTTPS, aggiornamenti supportati, 2FA amministratori, firewall e limiti di login, esposizione file/permessi e log; nessuna modifica a credenziali o impostazioni live senza approvazione specifica.
- Definire prima della consegna responsabile, canale di distribuzione e processo degli aggiornamenti del nuovo tema, monitoraggio, frequenza backup e risposta incidenti. Non promettere aggiornamenti automatici senza averli implementati.
- Codice del tema attualmente attivo intoccabile; nessuna migrazione distruttiva dei suoi dati/impostazioni. Conservare il tema e verificare il ripristino completo, non solo il cambio tema.

## SEO integrata nel nuovo progetto
- Richiesta: miglioramento SEO sostanziale (ambizione «10X»), non promessa di moltiplicare traffico o posizioni. Definire baseline e KPI prima della pubblicazione: click/impression organiche, query non-brand, pagine indicizzate e richieste qualificate; usare Search Console se disponibile.
- Audit preliminare in sola lettura: URL, status HTTP, indicizzazione, canonical, titoli/descrizioni, sitemap, immagini e performance; verificare il gestore SEO esistente prima di scegliere plugin o logica custom ed evitare output duplicati.
- Nuovo tema: HTML significativo renderizzato sul server, gerarchia dei titoli, link interni homepage/Portfolio/storie, metadati specifici per pagina e campi SEO semplici integrati nell'editor.
- Foto: srcset/sizes e dimensioni coerenti, formati ottimizzati compatibili con hosting, testi alternativi appropriati al contesto senza keyword stuffing, caricamento prioritario dell'elemento LCP e differito delle immagini non critiche. Conservare qualità fotografica e animazioni approvate.
- Dati strutturati pertinenti e verificati; nessuna informazione commerciale, recensione, data o località inventata. Nessuna promessa di rich result.
- Bilinguismo confermato: prevedere URL IT/EN indicizzabili e hreflang coerenti.
- Preservare URL e segnali SEO esistenti: inventario prima della migrazione, redirect permanenti solo per URL davvero cambiati, nessuna pagina importante persa e 404 HTTP reale. Staging non pubblico/non indicizzabile; verificare rimozione del noindex in produzione.
- Copy naturale coerente con identità del fotografo, matrimoni/eventi e luoghi reali; nessuna pagina geografica artificiale o testo nascosto. Approvarlo prima di sostituire testi esistenti.
- Misurare performance mobile/desktop prima e dopo; obiettivi Core Web Vitals buoni (LCP <= 2,5 s; INP <= 200 ms; CLS <= 0,1), separando test di laboratorio da dati reali quando disponibili.
- Vincolo invariato: nessuna modifica al codice del tema attivo; sviluppo e test sul nuovo progetto separato, rollout solo approvato.

## Fasi
1. Inventario contenuti e vincoli visuali: mappare tutti i testi, le immagini, i link e le cornici dal prototipo. Stabilire cosa il cliente può cambiare senza rompere layout/animazione, soprattutto quantità delle foto animate.
2. Prototipo dell'editor pagine/storie e del ritaglio: approvare blocchi guidati, flusso di selezione, riordino, ritaglio/rotazione, traduzione, anteprima e salvataggio. Nessun pannello separato.
3. Ambiente WordPress separato: verificare requisiti Aruba, versioni e plugin esistenti; predisporre staging/local e backup prima di interventi remoti.
4. Tema: riprodurre il riferimento con contenuti statici, verificare desktop/mobile e animazioni prima di renderli dinamici.
5. Integrazioni dell'editor nel tema: collegare blocchi/campi e Media, traduzione, ordinamento e ritagli per utilizzo; validazione, escaping, permessi e nonce; salvataggio e ripristino.
6. Verifica completa: confronti visuali, foto verticali/orizzontali, quantità limite, testo lungo, responsive, accessibilità/reduced motion, prestazioni, cache Aruba, backup/restore. Testare modifica effettiva dall'editor, riapertura dei contenuti e corrispondenza col risultato pubblico.
7. Consegna: ZIP installabili versionati, guida cliente, checklist installazione e rollback. Pubblicazione soltanto dopo approvazione.

## Accettazione
- Rendering fedele al riferimento approvato.
- Tutti i testi e tutte le immagini gestibili senza codice.
- Inquadrature prevedibili con anteprima coerente al frontend.
- Ritaglio di una posizione non altera le altre né l'originale.
- Nessuna regressione di animazioni, responsive o Michroma.
- Nessuna scrittura sul sito live durante progettazione/sviluppo.

## Prossimo step
Inventario del prototipo e definizione del modello dei contenuti. Non è ancora iniziata l'implementazione del tema.
