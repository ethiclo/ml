import requests

BASE_URL="http://127.0.0.1:5000"
PROD_URL="https://ml-production-3fc0.up.railway.app"

def test_create():
    resp = requests.post(BASE_URL + '/add_shopper/mdawes')
    print(resp.json())

def test_get_products():
    resp = requests.get(BASE_URL + '/get_my_products/mdawes')
    print(resp.json())

def test_add_url(url):
    endpoint = "/add_url"
    data = {
        "url": url,
        "email": "mdawes"
    }
    resp = requests.post(BASE_URL + endpoint, json=data)
    print(resp.json())

def test_get_sustainable_products():
    url = "https://www.nike.com/ca/t/fc-football-tracksuit-wB5QDv/DC9065-010"
    endpoint = "/get_sustainable_products"
    data = {
        "url": url,
        "email": "mdawes"
    }
    resp = requests.get(BASE_URL + endpoint, json=data)
    print(resp.json())

if __name__ == "__main__":
    # test_create()
    # url1 = "https://www.nike.com/ca/t/fc-football-tracksuit-wB5QDv/DC9065-010"
    # test_add_url(url1)
    # url2 = "https://www.nike.com/ca/t/alphafly-2-road-racing-shoes-1wG4D7/DZ4784-304"
    # test_add_url(url2)
    test_get_sustainable_products()
    # test_get_products()