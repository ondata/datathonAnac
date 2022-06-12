# Datathon Anac

# Introduzione
[AppaltiPop](http://appaltipop.it) è un progetto di [onData APS](https://www.ondata.it) realizzato grazie anche al sostegno di **Transparency International Italia** e **ParliamentWatch Italia**. Si tratta di una piattaforma che permette di visionare gli appalti pubblici e di ottenere informazioni di dettaglio relative al singolo appalto. AppaltiPop è stato rilasciato nel 2021 e sono stati riusati i dati sugli appalti pubblicati in XML da **ANAC** in base alla legge 190 opportunamente trasformati, raffinati e integrati con informazioni aggiuntive. I file XML pubblicati da ANAC sono stati inoltre trasformati e ripubblicati nello [standard OCDS](https://standard.open-contracting.org/latest/en/), uno standard internazionale specifico per i contratti pubblici. AppaltiPop consente di ricercare e visionare i singoli appalti in base a diversi criteri di ricerca. Al verificarsi di alcune condizioni, il sistema può assciare ad un singolo appalto una o più “red flags”. Sono essenzialmente dei “warning” che vengono assegnati sulla base di cinque criteri: il basso numero di offerenti, la bassa percentuale di offerte, la presenza di un singolo offerente, la prima gara vinta da parte di un offerente, o la presenza di aggiudicatari sconosciuti. E’ un modo per dare delle indicazioni di massima su quelle che possono essere delle eventuali criticità da poter approfondire per altre vie.

# Il Datathon ANAC

Anac di recente ha ampliato la sezione dedicata alla pubblicazione dei dati aperti, utilizzando anche lo standard OCDS per la loro pubblicazione. E per promuovere l'utilizzo dei dati aperti, ha lanciato una [competizione sui dati](https://www.anticorruzione.it/-/anac-lancia-un-datathon-per-l-utilizzo-delle-informazioni-della-banca-dati).


# La nostra proposta 

AppaltiPop consente al momento di consultare i dati sugli appalti di poco più di 30 comuni italiani. E' un sistema che sfrutta come fonte dati quelli pubblicati in formato xml da ANAC in base alla legge 190 e lo fa seguendo la pipeline mostrata in figura.

![image](https://user-images.githubusercontent.com/482417/173175284-8d867d65-68be-48a8-ae83-2cb40b8c1bb6.png)

I dati in formato xml vengono acquisiti e subiscono varie trasformazioni intermedie fino ad arrivare ad essere modellati secondo lo standard OCDS. I dati così ottenuti vengono da una parte pubblicati su una [sezione apposita di AppaltiPop](https://www.appaltipop.it/it/download) per il download, dall'altra vengono ulteriormente trasformati in base ad uno schema dati specifico utilizzato da AppaltiPop. E' in questo passaggio che vengono individuate e associate al singolo appalto le eventuali Red Flags.

La nostra proposta per il Datathon ANAC è stata quella di immaginare come connettere AppaltiPop direttamente al nuovo portale OCDS di ANAC, andando a rivedere la pipeline come mostrato in figura, eliminando le varie trasformazioni intermedie e partendo direttamente dai [file OCDS del portale ANAC](https://dati.anticorruzione.it/opendata/ocds). La possibilità di sfruttare i dati già in formato OCDS, consente infatti di ridisegnare la pipeline del dato mantenendo soltanto la parte all'interno del box rosso.  

![image](https://user-images.githubusercontent.com/482417/173175572-478ad3c4-14a7-4bb4-a913-8f75b0f2201c.png)

E poichè i dati oubblicati in OCDS da ANAC riguardano tutti i contratti relativi a tutte le stazioni appaltanti dal 2018 al 2021, si avrà la possibilità di estendere e arricchire la disponibilità di dati consultabili su AppaltiPop, creando nello stesso tempo i presupposti per l'introduzione di nuove Red Flags.


# Cosa abbiamo fatto

Siamo così partiti dai dati pubblicati da ANAC in formato OCDS. L'obiettivo è stato quello di creare uno script che potesse leggere i file OCDS, fare le necessarie trasformazioni e generare i dati da pubblicare secondo lo schema utilizzato su AppaltiPop. Il punto di partenza è stata la procedura già utilizzata per alimentare l'attuale AppaltiPop, procedura questa che è stata rivista in vari punti sulla base di una diversa organizzazione dei dati ANAC in OCDS. Va detto che per certi aspetti le informazioni sui contratti pubblicati in OCDS sono molto più ricche rispetto a quelle presenti sui file xml. Ad ogni modo, un primo obiettivo è stato quello di ricondurre le informazioni presenti nei file OCDS a quelle già gestite dal portale AppaltiPop. In questa fase infatti non abbiamo avuto la possibilità di agire sullo schema dati e sul Front End di AppaltiPop, operazione questra che sarebbe risultata piuttosto complessa e onerosa.

Il Notebook Python che abbiamo pubblicato qui sul repository consente di passare dai dati OCDS di ANAC ad un file Json necessario per alimentare il repository Elastic che sta alla base di AppaltiPop. 

# Criticità

Una forte criticià è stata l'assenza di dati relativi ai partecipanti ai vari bandi di gara. E' presente infatti esclusivamente l'informazione relativa agli aggiudicatari. Questo è stato un problema bloccante per quanto riguarda il calcolo delle red flags. Tutte le red flags implementate in AppaltiPop si basano infatti su una serie di informazioni relative proprio ai partecipanti. Calcolare infatti il basso numero di offerenti, la bassa percentuale di offerte, la presenza di un singolo offerente non ha infatti alcun significato quando mancano le info necessarie. Ovviamente gli aggiudicatari sono anche loro degli offerenti, ma il calcolo delle prime tre red flags perde di significato. Come perde di significato alche il calcolo del red flag quando si verifica la condizione "la prima gara vinta da parte di un offerente", che andrebbe assegnata a coloro che partecipano e vincono per la prima volta. Dai dati disponibili non riusciamo infatti a dedurre se il vincitore abbia partecipato in passato ad altre gare.

# Prossimi passi

Per il momento abbiamo mantenuto un calcolo fittizio delle Red Flags anche sui nuovi dati OCDS.  Nel caso in cui venissero inserite anche le informazioni sui partecipanti, allora potrà essere possibile rivedere la procedura complessiva di calcolo e di alimentazione del repository di AppaltiPop. Mantenendo la stessa GUI e lo stesso schema dati, AppaltiPop potrebbe quindi passare dai 30 comuni attuali a coprire tutte le stazioni appaltanti con uno sforzo comunque contenuto che onData è sicuramente in grado di sostenere. E poichè sono disponibili i dati dal 2018 al 2021, sarà possibile pensare anche a red flags ottenute sulla base di un'analisi di tipo longitudinale. Un ulteriore servizio sulla trasparenza per l'intera collettività. 





