from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import date
import json


def write_json(data):
    with open("prices.json", "w") as file:
        json.dump(data, file, indent=4)

def read_json():
    try:
        with open("prices.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return None


class price_entry():
    def __init__(self, dateString, price, source):
        self.date = dateString
        self.price = price
        self.source = source  # NEW: track which site the price came from

    def to_dict(self):
        return {"date": self.date,
                "price": self.price,
                "source": self.source}  # NEW


def get_tcgplayer_price(driver, wait):
    driver.get("https://www.tcgplayer.com/product/668541?Language=English")
    itemPrice = wait.until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, "span.spotlight__price")
        )
    )
    price_text = itemPrice.get_attribute("textContent").strip()
    print("TCGPlayer Price:", price_text)
    return price_text


def get_target_price(driver, wait):
    driver.get("https://www.target.com/p/pokemon-me2-5-ascended-heroes-booster-bundle-2-pack/-/A-1011165570#lnk=sametab")
    itemPrice = wait.until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, "[data-test='product-price']")
        )
    )
    price_text = itemPrice.get_attribute("textContent").strip()
    print("Target Price:", price_text)
    return price_text

options = webdriver.EdgeOptions()
options.add_experimental_option("detach", True)
options.add_argument("--start-maximized")

driver = webdriver.Edge(options=options)
wait = WebDriverWait(driver, 15)

today = str(date.today())

existing_data = read_json()
if existing_data is None:
    existing_data = []

tcg_price = get_tcgplayer_price(driver, wait)
existing_data.append(price_entry(today, tcg_price, "tcgplayer").to_dict())

target_price = get_target_price(driver, wait)
existing_data.append(price_entry(today, target_price, "target").to_dict())

write_json(existing_data)
print("Saved both prices!")