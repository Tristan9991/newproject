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

def write_json(data):
    with open("prices.json", "w") as file:
        json.dump(data, file, indent=4)

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
driver.get("https://www.pokemoncenter.com/?srsltid=AfmBOopeiP4_hc4Nw96UuLoVo8GUvdAO2i97-Ma6EdH7bIo1FyHOXjAP")