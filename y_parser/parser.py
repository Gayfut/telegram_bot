"""file for control parser and his specification"""
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import StaleElementReferenceException
from time import sleep

from y_parser.settings import (
    link_to_site,
    search_input_selector,
    search_request_text,
    video_elements_selector,
    title_selector,
    title_date_text_selector,
    views_selector,
    date_selector,
    like_bar_selector,
    like_bar_attribute,
    channel_selector,
    channel_text_selector,
)


class Parser:
    """control parser"""

    def __init__(self):
        self.__browser = webdriver.Firefox(options=self.__set_options())

    @staticmethod
    def __set_options():
        """return headless options for parser driver"""
        options = Options()
        options.add_argument("--headless")

        return options

    def start_parse(self):
        """start site parsing"""
        self.__open_site()
        self.__search_in_site()
        sleep(5)

        video_links = self.__get_links()
        info_about_videos = self.__get_info_about_videos(video_links)

        return info_about_videos

    def __open_site(self):
        """open site for parsing"""
        self.__browser.get(link_to_site)

    def __search_in_site(self):
        """search definite request in site"""
        search_input = self.__browser.find_element_by_css_selector(
            search_input_selector
        )
        search_input.send_keys(search_request_text)
        search_input.submit()

    def __get_links(self):
        """return video links"""
        video_elements = self.__browser.find_elements_by_css_selector(
            video_elements_selector
        )
        video_links = []

        for video_element in video_elements:
            try:
                video_link = video_element.get_attribute("href")
                video_links.append(video_link)
            except StaleElementReferenceException:
                continue

        return video_links

    def __get_info_about_videos(self, video_links):
        """return info about some videos"""
        info_about_videos = []

        self.__browser.execute_script("window.open('');")
        self.__browser.switch_to.window(self.__browser.window_handles[1])

        for video_link in video_links:
            info_about_video = self.__get_info_about_video(video_link)
            info_about_videos.append(info_about_video)

        self.__browser.close()
        self.__browser.switch_to.window(self.__browser.window_handles[0])

        return info_about_videos

    def __get_info_about_video(self, video_link):
        """return info about a one video"""
        self.__browser.get(video_link)
        sleep(2)

        title = (
            self.__browser.find_element_by_css_selector(title_selector)
            .find_element_by_css_selector(title_date_text_selector)
            .text
        )
        views = self.__browser.find_element_by_css_selector(views_selector).text
        date = (
            self.__browser.find_element_by_css_selector(date_selector)
            .find_element_by_css_selector(title_date_text_selector)
            .text
        )
        like_bar = self.__browser.find_element_by_css_selector(
            like_bar_selector
        ).get_attribute(like_bar_attribute)
        channel = (
            self.__browser.find_element_by_css_selector(channel_selector)
            .find_element_by_css_selector(channel_text_selector)
            .text
        )

        info_about_video = {
            "title": title,
            "views": views,
            "date": date,
            "like_bar": like_bar,
            "channel": channel,
            "link": video_link,
        }

        return info_about_video

    def stop_parse(self):
        """stop parsing"""
        self.__browser.quit()
