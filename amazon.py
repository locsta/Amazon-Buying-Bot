from selenium_scraper import Scraper
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
import time
from datetime import datetime
import os
import pandas as pd
import json

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from pprint import pprint
from itertools import cycle
import pyautogui
import threading

def amazon():
    login_email = input("Enter your email for Amazon:")
    login_password = input("Enter your password for Amazon:")
    countries = ["fr", "it", "es", "de", "co.uk"]
    ps5 = {"item": "Playstation 5", "min_price": 498, "price_max":520,"link":"https://www.amazon.fr/PlayStation-%C3%89dition-Standard-DualSense-Couleur/dp/B08H93ZRK9"}
    items = [ps5]

    def browsers_creator():
        browsers = []
        i = 0
        for item in items:
            for country in countries:
                url = item["link"].replace(".fr", f".{country}")
                browser = Scraper(headless=False).open_browser()
                browser.get(url)
                try:
                    browser.find_element_by_id("sp-cc-accept").click()
                except:
                    pass
                browser.find_element_by_id("nav-link-accountList").click()
                browser.find_element_by_id("ap_email").send_keys(login_email)
                browser.find_element_by_id("continue").click()
                time.sleep(0.5)
                browser.find_element_by_id("ap_password").send_keys(login_password)
                browser.find_element_by_id("signInSubmit").click()
                # # Set browser size to the minimum
                # browser.set_window_size(1, 1)
                # # Move browser to the to right corner
                # browser.set_window_position(3390, i*95)
                i += 1
                browsers.append({"browser":browser, "min_price":item["min_price"], "price_max":item["price_max"], "item":item["item"], "country":country.upper()})
                time.sleep(12)
        return cycle(browsers)

    browsers_cycle = browsers_creator()

    def next_browser():
        return next(browsers_cycle)

    while True:
        obj = next_browser()
        browser = obj["browser"]
        price_max = obj["price_max"]
        min_price = obj["min_price"]
        item = obj["item"]
        country = obj["country"]
        browser.refresh()
        price = 9999999
        currency = "€"
        try:
            if country == "FR":
                price = float(browser.find_element_by_id("price_inside_buybox").text.replace("€", "").replace(",", ".").replace(" ", ""))
            if country == "IT" or country == "ES" or country == "DE":
                price = float(browser.find_element_by_id("price_inside_buybox").text.replace("€", "").replace(".", "").replace(",", "."))
            if country == "CO.UK":
                price = float(browser.find_element_by_id("price_inside_buybox").text.replace("£", "").replace(",", ""))
                currency = "£"
        except:
            pass
        try:
            captcha = browser.find_element_by_id("captchacharacters")
        except:
            captcha = None
        if captcha:
            print(f"Enter captcha for Amazon {country}")
            os.system("vlc /home/locsta/Downloads/screaming_goat.mp3")
            time.sleep(15)
        else:
            if price == 9999999:
                print(f"{item} not available on Amazon {country}")
            else:
                print(f"{item} current price is {price}{currency} on Amazon {country}")
            if price < price_max and price > min_price:
                os.system("vlc /home/locsta/Downloads/screaming_goat.mp3")
                print(f"FOUND {item} at {price}{currency}!!!")
                # Click on buy button
                WebDriverWait(browser, 3).until(EC.presence_of_element_located((By.ID, 'buy-now-button'))).click()
                browser.maximize_window()
                # Next page skip amazon prime offer
                try:
                    prime_promo = browser.find_element_by_id("prime-declineCTA")
                    if prime_promo:
                        prime_promo.click()
                except:
                    try:
                        browser.find_element_by_id("turbo-checkout-pyo-button").find_element_by_xpath('..').click()
                    except:
                        # Place order
                        time.sleep(5)
                        pyautogui.click((4030, 1048))
                        # pyautogui.moveTo((2600, 880))
                        try:
                            WebDriverWait(browser, 8).until(EC.presence_of_element_located((By.ID, 'placeYourOrder'))).click()
                        except:
                            pass
                        os.system("vlc /home/locsta/Downloads/screaming_goat.mp3")
                        return
            else:
                time.sleep(2)
                continue

if __name__ == '__main__':
    # execute only if run as the entry point into the program
    amazon()