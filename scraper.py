from serpapi import GoogleSearch
import requests
import logging
import sys, os
from bs4 import BeautifulSoup
import re

headers = {'Cache-Control': 'no-cache', 'Content-Type': 'application/json'}
# params = {'token': os.environ.get("BROWSERLESS_API_KEY")}
params = {'token': 'b19d64a7-6773-45bd-8b16-4e2bad27a3eb'}


def scrape_website_text(url: str) -> str:
    """Scrape the website text."""
    targets = {
        "url": url,
        "elements": [
            {"selector": "body"}
        ]
    }

    response = requests.post("https://chrome.browserless.io/scrape", params=params, headers=headers, json=targets)
    
    # Returns the main text on the webpage
    resp = response.json()
    webpage_text = resp['data'][0]['results'][0]['text']

    # Grabs the pitcure from the website
     
    return webpage_text


def get_imgs(url: str) -> str:
    """Get images from website."""
    resp = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
    soup = BeautifulSoup(resp.text, 'html.parser')
    images = soup.find_all('img')

    consolidated = []
    for image in images:
        alt_text = image.get("alt")
        img_src = image.get("src")
        if alt_text is not None:
            consolidated.append([alt_text, img_src])

    return consolidated


if __name__ == "__main__":
    # sample = "https://us.louisvuitton.com/eng-us/products/thistle-embroidered-wavy-denim-jacket-nvprod4160010v/1AB517"
    sample = "https://www.aritzia.com/en/product/gramercy-t-shirt/109006.html?dwvar_109006_color=1275"
    # print(scrape_website_text(sample))
    print(get_imgs(sample))
