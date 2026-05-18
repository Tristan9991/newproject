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
    def __init__(self, dateString, price):
        self.date = dateString
        self.price = price

    def to_dict(self):
        return {"date": self.date,
                "price": self.price}


options = webdriver.EdgeOptions()
options.add_experimental_option("detach", True)
options.add_argument("--start-maximized")

driver = webdriver.Edge(options=options)
driver.get("https://www.tcgplayer.com/product/668541?Language=English")

wait = WebDriverWait(driver, 15)

itemPrice = wait.until(
    EC.presence_of_element_located(
        (By.CSS_SELECTOR, "span.spotlight__price")
    )
)

price_text = itemPrice.get_attribute("textContent").strip()
print("TCGPlayer Price:", price_text)

price_text = itemPrice.get_attribute("textContent").strip()
print(f"the price is: {price_text}")

today = str(date.today())
new_entry = price_entry(today, price_text).to_dict()

existing_data = read_json()
if existing_data == None:
    existing_data = []

existing_data.append(new_entry)
write_json(existing_data)

print("saved the price!!")