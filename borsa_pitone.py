"""Borsa Pitone"""
# Borsa Pitone
# Simple localhost proxy for Portfolio Performance to access borsaitaliana.it
# securities quotes.
# Leggere il READMe.md per le istruzioni d'uso
#
# (C) 2024 by Francesco Usseglio Gaudi

import datetime
import uvicorn
from fastapi import FastAPI, Response
import requests
from lxml.html import fromstring


# http://localhost:8000/borsaitaliana/eurotlx/{ISIN}
# $.data[*].date
# yyyy-MM-dd
# $.data[*].close

app = FastAPI()


@app.get("/")
def read_root():
    """radice

    Returns:
        _type_: _description_
    """
    return {"Borsa": "Pitone"}


@app.get("/borsaitaliana/eurotlx/{isin}", status_code=200)
def borsaitaliana(isin: str, response: Response):
    """accede a borsaitaliana eurotlx per isin come argomento

    Args:
        isin (str): isin dello strumento da cercare
        response (Response): per gestire eventuali errori

    Returns:
        _type_: json in formato PP
    """
    if isin == "null":
        print(f"ERROR: ISIN '{isin}' è appunto null")
        response.status_code = 500
        return {"isin": isin, "data": "error, isin è null"}

    r = requests.get(
        f"https://www.borsaitaliana.it/borsa/cw-e-certificates/eurotlx/scheda/{isin}.html?lang=it",
        timeout=10)

    print(f"Status: {r.status_code} and reason: {r.reason}")

    if r.status_code != 200:
        print("ERROR: il server remoto ha dei problemi?")
        print("provare ad aprire in un browser:")
        print(
            f"https://www.borsaitaliana.it/borsa/cw-e-certificates/eurotlx/scheda/{isin}.html?lang=it")
        response.status_code = 500
        return {"isin": isin, "data": "remote server error", "error": r.reason}

    tree = fromstring(r.text)

    try:
        price = tree.xpath('(//td)[10][1]/span/text()')
        price = price[0].replace('.', '').replace(",", ".")
        date = tree.xpath('(//td)[12][1]/span/text()')
        datenew = datetime.datetime.strptime(date[0], "%d/%m/%Y")
    except IndexError:
        print("ERROR IndexError: 2 possibilità: l'ISIN non è corretto/non trovato "
              "oppure il formato pagina è cambiato e allora va modificato questo software")
        print("provare ad aprire in un browser:")
        print(
            f"https://www.borsaitaliana.it/borsa/cw-e-certificates/eurotlx/scheda/{isin}.html?lang=it")
        response.status_code = 404
        return {
            "isin": isin,
            "data": "remote server error",
            "error": "IndexError, price o data non trovati. Due possibilità: l'ISIN non è corretto/non trovato "
            "oppure il formato pagina è cambiato e allora va modificato questo software"
        }

    print(f"{datetime.datetime.now()}: price: {price} - date: {datenew.date()}")

    return {"isin": isin,
            "totalCount": 1,
            "tradedInPercent": False,
            "data": [
                {
                    "close": price,
                    "date": datenew.date(),
                }
            ]
            }


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000, use_colors=False)
