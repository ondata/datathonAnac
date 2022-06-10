# Datathon Anac

# Introduzione
[AppaltiPop](http://appaltipop.it) è un progetto di onData APS realizzato grazie anche al sostegno di Transparency International Italia e ParliamentWatch Italia. Si tratta di una piattaforma che permette di visionare gli appalti pubblici e di ottenere informazioni di dettaglio relative al singolo appalto. Vengono riusati i dati pubblicati in XML da ANAC in base alla legge 190 opportunamente trasformati, raffinati e integrati con informazioni aggiuntive. I file XML pubblicati da ANAC vengono trasformati e ripubblicati nello [standard internazionale OCDS](https://standard.open-contracting.org/latest/en/). Oltre a permettere di ricercare e visionare i singoli appalti in base a diversi criteri di ricerca, al verificarsi di alcune condizioni, il sistema può associare ad un singolo appalto una o più “red flags”. Sono essenzialmente dei “warning” che vengono assegnati sulla base di cinque criteri come: il basso numero di offerenti, la bassa percentuale di offerte, la presenza di un singolo offerente, la prima gara vinta da parte di un offerente, o la presenza di aggiudicatari sconosciuti. E’ un modo per dare delle indicazioni sugli appalti che possono poi essere approfondite per altre vie.

# Il Datathon ANAC

Anac di recente ha ampliato la sezione dedicata alla pubblicazione dei dati aperti, utilizzando anche lo standard OCDS per la loro pubblicazione. E per promuovere l'utilizzo dei dati aperti, ha lanciato una [competizione sui dati](https://www.anticorruzione.it/-/anac-lancia-un-datathon-per-l-utilizzo-delle-informazioni-della-banca-dati).


# La nostra proposta 

AppaltiPop consente al momento di consultare i dati sugli appalti di poco più di 30 comuni italiani. E’ un sistema predisposto per gestire dati in formato OCDS, per cui la nostra proposta per il Datathon ANAC è stata quella di immaginare come connettere AppaltiPop direttamente al nuovo portale OCDS di ANAC.
Come fonte dati abbiamo infatti immaginato di utilizzare i dataset pubblicati in OCDS del portale ANAC (https://dati.anticorruzione.it/opendata/ocds) per alimentare il database utilizzato da AppaltiPop. L'obiettivo è quello di estendere e arricchire la disponibilità di dati consultabili attraverso la piattaforma, creando nello stesso tempo i presupposti per un’analisi più estesa delle Red Flags.


# Cosa abbiamo fatto

Siamo così partiti dai dati pubblicati da ANAC in formato OCDS. L'obiettivo è stato quello di creare uno script che potesse leggere i file OCDS, fare le necessarie trasformazioni e generare i dati da pubblicare secondo lo schema utilizzato su AppaltiPop. Il punto di partenza è stata la procedura già utilizzata per alimentare l'attuale AppaltiPop, procedura questa che è stata rivista in vari punti sulla base di una diversa organizzazione dei dati ANAC in OCDS.



# Criticità

Una prima criticià è stata sicuramente l'assenza di dati relativi ai partecipanti ai vari bandi di gara. E' presente esclusivamente l'informazione relativa agli aggiudicatari. Questo è stato un problema bloccante per quanto riguarda il calcolo delle red flags.
Calcolare infatti il basso numero di offerenti, la bassa percentuale di offerte, la presenza di un singolo offerente quando non ha infatti alcun significato quando non ci sono le info necessarie. Ovviamente gli aggiudicatari sono anche loro degli offerenti, ma il calcolo delle prime tre red flags perde di significato.
Come perde di significato alche il calcolo del red flag quando si verifica la condizione "la prima gara vinta da parte di un offerente", che andrebbe assegnata a coloro che partecipano e vincono per la prima volta. Dai dati disponibili non riusciamo infatti a dedurre se il vincitore abbia partecipato in passato ad altre gare.





