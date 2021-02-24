from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from time import sleep

from y_parser.settings import link_to_site, search_input_selector, search_request_text, filter_button_selector

class Parser:

    def __init__(self):
        self.__browser = webdriver.Firefox()

    @staticmethod
    def __set_options():
        """return headless options for parser driver"""
        options = Options()
        options.add_argument("--headless")

        return options

    def start_parse(self):
        self.__open_site()
        self.__search_in_site()

        sleep(10)

    def __open_site(self):
        self.__browser.get(link_to_site)

    def __search_in_site(self):
        search_input = self.__browser.find_element_by_css_selector(search_input_selector)
        search_input.send_keys(search_request_text)
        search_input.submit()

    def stop_parse(self):
        self.__browser.quit()