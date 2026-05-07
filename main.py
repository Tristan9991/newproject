from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
from datetime import date

def write_json(data):
    with open("prices.json", "w") as file:
        json.dump(data, file, indent=4)

class price_entry():
    def __init__(self, dateString, price):
        self.date = dateString
        self.price = price

    def to_dict(self):
        return {"date": self.date,
                "price": self.price}

def read_json():
    try:
        with open("prices.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return None

# set up options for EDGE browser
options = webdriver.EdgeOptions()

# detach means "detach from python" prevents auto-close
options.add_experimental_option("detach", True)

# headless means, do NOT open the Edge browser.
options.add_argument("headless")

# set up driver and apply the options above
driver = webdriver.Edge(options=options)

# URL to site I am scraping
driver.get("https://www.pokemoncenter.com/product/10-10311-114/pokemon-tcg-mega-evolution-ascended-heroes-booster-bundle-6-packs")

# print page title
print(f"\nWe are looking at the {driver.title}\n")

wait = WebDriverWait(driver, 10)

# this line says: do not do anything until this element is loaded.
itemPrice = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "[data-test='product-price']")))



data = read_json()
if data is None:
    data = []

today = str(date.today())
currentPrice = float(itemPrice.text.split("$")[1])
print(f"The current price is ${currentPrice}.")


if data:
    prices = [float(x["price"]) for x in data]
    lowestPrice = min(prices)
    highestPrice = max(prices)

    if currentPrice < lowestPrice:
        print("Very low price")
    elif currentPrice > highestPrice:
        print("Very high price")

data.append(price_entry(today, currentPrice).to_dict())
write_json(data)


startingPrice = 26.94
for x in data:
    if currentPrice != startingPrice:
        if currentPrice < startingPrice:
            print(f"The price decreased on {x.date}.")
        elif currentPrice > startingPrice:
            print(f"The price increased on {x.date}.")
    startingPrice = currentPrice