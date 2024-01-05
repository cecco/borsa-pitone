# Borsa Pitone

Semplice proxy HTTP per l'applicazione Portfolio Performance, permette di ricevere l'ultima quotazione disponibile su borsa-italiana.it di alcuni strumenti (per adesso è limitato agli strumenti Euro-TLX). 
Come chiave di ricerca è utilizzato ISIN. 
Restituisce un JSON nel formato utilizzato dall'applicazione.

**NON** carica dati storici ma solo l'*ultimo disponile*

Questo software viene fornito senza alcun garanzia di funzionamento nè altre responsabilità di qualsiasi sorta: usare a proprio rischio e pericolo.

## Setup

1. Lanciare l'applicazione **borsa-pitone** *prima* di eseguire Portfolio Performance. 
2. all'interno di PP, selezionare (o creare lo strumento vuoto) avendo cura che sia presente il suo ISIN
3. Nella scheda *Quotazioni Storiche*:
    1. Feed quotazioni: Fornitore -> `JSON`
    2. URL del Feed: `http://localhost:8000/borsaitaliana/eurotlx/{ISIN}`
    3. Percorso a data: `$.data[*].date`
    4. Formato data: `yyyy-MM-dd`
    5. Percorso a chiusura: `$.data[*].close`

