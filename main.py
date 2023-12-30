import uvicorn
from fastapi import FastAPI
import requests
from lxml.html import fromstring
import datetime

# http://127.0.0.1:8000/borsaitaliana/JE00BGBBD829
# http://localhost:8000/borsaitaliana/{ISIN}
# $.data[*].date
# yyyy-MM-dd
# $.data[*].close

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/borsaitaliana/{isin}")
def borsaitaliana(isin: str):
    r = requests.get("https://www.borsaitaliana.it/borsa/cw-e-certificates/eurotlx/scheda/{isin}.html?lang=it".format(isin = isin))
    
    print("Status: {} and reason: {}".format(r.status_code, r.reason))
    
    # print(r.text)
    
    tree = fromstring(r.text)
    
    price = tree.xpath('(//td)[10][1]/span/text()')
    price = price[0].replace('.','').replace(",",".")
    date = tree.xpath('(//td)[12][1]/span/text()')
    datenew = datetime.datetime.strptime(date[0], "%d/%m/%Y")
    
    
    print("{0}: price: {1} - date: {2}".format(datetime.datetime.now(),price,datenew.date()))
    
    return {"isin": isin,
        "totalCount": 1,
        "tradedInPercent": False,
        "data" : [
            {
                "close": price,
                "date": datenew.date(),
            }
        ]
    }

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)