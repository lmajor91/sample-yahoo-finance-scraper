#!/usr/bin/env python3

from bs4 import BeautifulSoup as soup
import requests
import pickle
import json

# reading in headers
headers = None
with open("headers.pickle", "rb") as f_in:
    headers = pickle.load(f_in)


def main():

    # the url
    url = "https://finance.yahoo.com/quote/BTC-USD/"

    # need to make a request to a website
    r = requests.get(url,
                     allow_redirects=False, headers=headers)

    if (r.status_code != requests.codes.ok):
        print(f"There was an error connecting to {url}")
        return False

    # need to pull out certain information
    dom = soup(r.text, "html.parser")

    # collecting information
    info = {
        "name": "bitcoin",
        "identifer": "BTC-USD"
    }

    table_selectors = [
            "div[data-test*=\"left\"] > table",
            "div[data-test*=\"right\"] > table"
    ]

    for sel in table_selectors:
        table = dom.css.select(sel)[0].find_all("tr")
        for tr in table:
            td = tr.css.select("[data-test]")[0]
            name = td.get("data-test").lower().replace("_", "-").replace("td-", "")[:-6]
            info[name] = td.text

    info["price"] = dom.css.select("[data-symbol=\"BTC-USD\"]")[0].get("value")

    # export in JSON format
    dump = json.dumps(info, indent=4)

    with open("bitcoin.json", "w") as f_out:
        f_out.write(dump)
        f_out.write("\n")

    # logging
    print(f"Scraped information from {url}")

    # return code
    return True


if __name__ == "__main__":
    main()
