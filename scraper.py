from serpapi import GoogleSearch
import requests
import logging
import sys, os
from bs4 import BeautifulSoup
import re
from dotenv import load_dotenv

load_dotenv()

headers = {'Cache-Control': 'no-cache', 'Content-Type': 'application/json'}
params = {'token': os.environ.get("BROWSERLESS_API_KEY")}


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


def sustainability_search(query: str, location: str = "Canada"):
    """Search sustainability on google.
    Location is set to Canada by default.
    """
    search = GoogleSearch({
        "q": query,
        "location": location,
        "api_key": os.environ.get("SERP_API_KEY")
    })

    results = search.get_dict()

    # Get the relevant data
    imgs = results['inline_images']
    full_product = results['immersive_products']
    organic_results = results['organic_results']

    # Format the data
    formatted_results = {}
    num_items = min(len(imgs), len(full_product), len(organic_results))
    i = 0
    while i < num_items:
        formatted_results[i] = {}
        formatted_results[i]["brand"] = imgs[i]['source_name']
        formatted_results[i]["img"] = imgs[i]['original']
        formatted_results[i]["title"] = imgs[i]['title']
        formatted_results[i]["url"] = imgs[i]['source']
        formatted_results[i]["price"] = full_product[i]['price']
        formatted_results[i]["description"] = organic_results[i]['snippet']
        i += 1

    return formatted_results


if __name__ == "__main__":
    # sample = "https://us.louisvuitton.com/eng-us/products/thistle-embroidered-wavy-denim-jacket-nvprod4160010v/1AB517"
    sample = "https://www.aritzia.com/en/product/gramercy-t-shirt/109006.html?dwvar_109006_color=1275"
    # print(scrape_website_text(sample))
    # print(get_imgs(sample))
    print(sustainability_search("black square-neck long-sleeve bodysuit"))
