import random, re, time

from selenium import webdriver as wd
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup as bs

browser = wd.Chrome()

def wait(Expected_Conditions):
    return WebDriverWait(browser, 10).until(Expected_Conditions)

def random_sleep():
    sleep_time = random.uniform(1.0, 3.0)
    time.sleep(sleep_time)

def login():
    try:
        home_url = 'https://www.scribd.com/'
        browser.get(home_url)
        login = wait(EC.presence_of_element_located(
            (By.CSS_SELECTOR, '#global_header > div > a.header_login_btn.outline_btn.flat_btn')))
        login.click()
        ## fill up login form
        account_field = wait(EC.presence_of_element_located(
            (By.CSS_SELECTOR, '#login_or_email')))
        account_field.send_keys("haoyangliu96@gmail.com")

        pw_field = wait(EC.presence_of_element_located(
            (By.CSS_SELECTOR, '#login_password')))
        pw_field.send_keys("haoyangliu96")

        submit = wait(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, '#login_drop > div > div > div > div > div > '
                              'form > fieldset > div.button_container > button')))

        random_sleep()
        submit.click()
    except TimeoutException:
        login()

def download(url):
    time.sleep(3)
    browser.get(url)

    # wait(EC.presence_of_element_located(
    #     (By.CSS_SELECTOR, "#document_download_lb > div > div > div > div > div > "
    #                       "div > div.auto__base_component.auto__receipt_download.download_module "
    #                       "> div > div > div > div > div.button_container.flex_col > a"))).click()


if __name__ == '__main__':
    login()