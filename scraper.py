from serpapi import GoogleSearch
import requests
import logging
import sys, os
from bs4 import BeautifulSoup
import re
# from dotenv import load_dotenv
import openai

# load_dotenv()

headers = {'Cache-Control': 'no-cache', 'Content-Type': 'application/json'}
params = {'token': os.environ.get("BROWSERLESS_API_KEY")}
openai.api_key = os.environ.get("OPENAI_API_KEY")


def scrape_website_text(url: str) -> str:
    """Scrape the website text."""
    # Get the company name
    company_name = re.search(r'(?<=www\.)\w+', url).group(0)

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

    # prompt = """
    #     You are a sustainability expert. You are given a product desciption and asked to pick out
    #     words that mark the products overall sustainability. For example, the material the product
    #     is made of, the manufacturing process, the packaging, the company that makes it, any
    #     certifications the product has, etc.

    #     Please pick out the words that mark the products overall sustainability: 
    #     {}
    # """.format(webpage_text[0:2500])

    find_price = r"\$[^\s]*"
    price = re.search(find_price, webpage_text).group(0)    

    # completion = openai.Completion.create(
    #     model="text-davinci-003",
    #     prompt=prompt,
    #     temperature=0.7,
    #     max_tokens=60,
    #     top_p=1.0,
    #     frequency_penalty=0.0,
    #     presence_penalty=1
    # )

    webpage_info = {
        "brand": company_name,
        "website_text": webpage_text[:2500],
        "price": price
    }
     
    return webpage_info


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

    # Return the last image
    return consolidated[-1]


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
    # sample = "https://www.nike.com/ca/t/fc-football-tracksuit-wB5QDv/DC9065-010"
    # print(scrape_website_text(sample))
    # print(get_imgs(sample))
    # print(sustainability_search("black square-neck long-sleeve bodysuit"))
    pass
