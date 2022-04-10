import imp
from operator import rshift


import os
from selenium import webdriver
from dotenv import load_dotenv
from dateutil.parser import parse
from dateutil.relativedelta import relativedelta


class RShift:
    def __init__(self, url):
        self.url = url
        self.driver = webdriver.Chrome("./driver/chromedriver")
        self.driver.get(url)

    def login(self, user_id, user_password):
        elm_uid = self.driver.find_element_by_name("login_email")
        elm_uid.clear()
        elm_uid.send_keys(user_id)
        elm_pass = self.driver.find_element_by_name("login_pass")
        elm_pass.clear()
        elm_pass.send_keys(user_password)

        login_button = self.driver.find_element_by_tag_name("button")
        login_button.click()



def main():
    load_dotenv()
    user_id = os.getenv("USER_ID")
    user_password = os.getenv("USER_PASSWORD")
    rshift_url = os.getenv("RSHIFT_URL")
    rshift = RShift(rshift_url)
    rshift.login(user_id,user_password)

main()