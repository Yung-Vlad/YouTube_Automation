from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

import time
import random
import os

from config import downloaded_videos, delay, videos_by_acc, delay_for_upload

def send_com(driver, channel):
    # Send comment
    try:
        link_video = driver.find_element(By.XPATH,
                                         "/html/body/ytd-app/div[1]/ytd-page-manager/ytd-browse[1]/ytd-two-column-browse-results-renderer/div[1]/ytd-section-list-renderer/div[2]/ytd-item-section-renderer[1]/"
                                         "div[3]/ytd-reel-shelf-renderer/div[2]/yt-horizontal-list-renderer/div[2]/div/ytd-reel-item-renderer/div[1]/ytd-thumbnail/a").get_attribute(
            "href")
        driver.get(link_video)

        comment_btn = WebDriverWait(driver, 10).until(
            ec.presence_of_element_located((By.XPATH,
                                            "/html/body/ytd-app/div[1]/ytd-page-manager/ytd-shorts/div[3]/div[2]/ytd-reel-video-renderer[1]/div[3]/ytd-reel-player-overlay-renderer/div[2]/div[4]/ytd-button-renderer/yt-button-shape/label/button")))
        comment_btn.click()

        time.sleep(3)

        # input_field = driver.find_element(By.XPATH,
        #                                   "")
        # print(input_field)
        # input_field.click()
        # input_field.send_keys(channel["link"])

        driver.find_element(By.XPATH, "//*[@id='comment-dialog']/ytd-comment-dialog-renderer")

        # driver.find_element(By.XPATH,
        #                     "/html/body/ytd-app/div[1]/ytd-page-manager/ytd-shorts/div[3]/div[2]/ytd-reel-video-renderer[1]/div[1]/ytd-engagement-panel-section-list-renderer[1]/div[2]/ytd-section-list-renderer/div[2]/ytd-comments/ytd-item-section-renderer/div[1]/ytd-comments-header-renderer/div[5]/ytd-comment-simplebox-renderer/div[3]/ytd-comment-dialog-renderer/ytd-commentbox/div[2]/div/div[4]/div[5]/ytd-button-renderer[2]/yt-button-shape/button").click()
    except Exception as ex:
        print(ex)