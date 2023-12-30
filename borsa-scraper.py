import requests
from lxml import html
from lxml.cssselect import CSSSelector
import json


url = "https://www.borsaitaliana.it/borsa/cw-e-certificates/eurotlx/scheda/JE00BGBBD829.html?lang=it"

resp = requests.get(url)

tree = html.fromstring(resp.content)

price = tree.xpath('(//td)[10][1]/span/text()')
date = tree.xpath('(//td)[12][1]/span/text()')


ret = {
    "isin": "JE00BGBBD829",
    "totalCount": 1,
    "tradedInPercent": False,
    "data": [
            {
                "close": price[0],
                "date": date[0],
            }
        ]
}

y = json.dumps(ret)

print(y)