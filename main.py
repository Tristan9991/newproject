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
        self.source = source

    def to_dict(self):
        return {"date": self.date,
                "price": self.price,
                "source": self.source}


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
    driver.get("https://www.target.com/p/pok-233-mon-trading-card-game-mega-evolution-ascended-heroes-booster-bundle/-/A-95120834")
    itemPrice = wait.until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, "[data-test='product-price']")
        )
    )
    price_text = itemPrice.get_attribute("textContent").strip()
    print("Target Price:", price_text)
    return price_text


def compare_prices(tcg_price_text, target_price_text):
    def parse_price(price_text):
        print(f"Raw price text: '{price_text}'")
        cleaned = ''.join(c for c in price_text if c.isdigit() or c == '.')
        print(f"Cleaned price text: '{cleaned}'")
        if not cleaned:
            raise ValueError(f"Could not parse price from: '{price_text}'")
        return float(cleaned)

    tcg = parse_price(tcg_price_text)
    target = parse_price(target_price_text)
    difference = abs(tcg - target)

    print("Price Comparison")
    print(f"TCGPlayer: ${tcg:.2f}")
    print(f"Target: ${target:.2f}")

    if tcg < target:
        print(f"TCGPlayer is cheaper by ${difference:.2f}")
    elif target < tcg:
        print(f"Target is cheaper by ${difference:.2f}")
    else:
        print("Both prices are equal!")

    return tcg, target

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

compare_prices(tcg_price, target_price)