from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.keys import Keys

import time
import random
import os

from config import downloaded_videos, delay, videos_by_acc, delay_for_upload,\
    add_description, write_comment, add_name_video


# Random selecting video
def select_video(channel):
    videos_list = os.listdir(channel["path_to_videos"])
    while True:
        video = random.choice(videos_list)

        if repeatability_check(video):
            break

    downloaded_videos.append(video)
    video = os.path.join(os.path.dirname(__file__), rf"source/videos/first/{video}")

    return video


# Check repeating videos
def repeatability_check(video):
    if video in downloaded_videos:
        return False

    return True


def upload_video(driver, channel):
    for _ in range(videos_by_acc):
        # Try to click continue
        try:
            cont_btn = WebDriverWait(driver, 10).until(
                ec.presence_of_element_located((By.XPATH, "/html/body/ytcp-warm-welcome-dialog/ytcp-dialog/tp-yt-paper-dialog/div[2]/div/ytcp-button")))
            cont_btn.click()
        except Exception as ex:
            pass

        try:
            # Add video
            create_btn = WebDriverWait(driver, 10).until(
                ec.presence_of_element_located((By.XPATH, "//ytcp-button[@id='create-icon']")))
            create_btn.click()

            upload_btn = WebDriverWait(driver, 10).until(
                ec.presence_of_element_located((By.XPATH, "/html/body/ytcp-app/ytcp-entity-page/div/ytcp-header/header/div/"
                                          "ytcp-text-menu/tp-yt-paper-dialog/tp-yt-paper-listbox/tp-yt-paper-item[1]")))
            upload_btn.click()
        except Exception as ex:
            pass


        # Try to create account
        try:
            driver.find_element(By.XPATH, "//*[@id='create-channel-button']").click()
            time.sleep(5)
            driver.find_element(By.XPATH,
                                "/html/body/ytd-app/div[1]/div/ytd-masthead/div[4]/div[3]/div[2]/"
                                "ytd-topbar-menu-button-renderer[1]/div/a/yt-icon-button/button").click()
            time.sleep(3)
            driver.find_element(By.XPATH,
                                "//ytd-compact-link-renderer[contains(@class, 'style-scope')"
                                " and contains(@class, 'yt-multi-page-menu-section-renderer')]").click()
            time.sleep(3)
        except Exception as ex:
            pass

        time.sleep(5)
        # Input video
        send_video = WebDriverWait(driver, 10).until(
            ec.presence_of_element_located((By.XPATH, "//input[@type='file']")))
        video = select_video(channel)

        send_video.send_keys(video)
        time.sleep(5)

        if add_description:
            input_description = driver.find_elements(By.XPATH, "//div[@slot='input']")[1]

            if add_name_video:
                input_description.send_keys(f"{video.split('/')[-1].split('.mp4')[0]}")
                time.sleep(1)
                input_description.send_keys(Keys.ENTER)
                time.sleep(1)

            input_description.send_keys(f"{channel['description']}")
            time.sleep(3)

        radio_btn = WebDriverWait(driver, 10).until(
            ec.presence_of_element_located((By.CSS_SELECTOR, "tp-yt-paper-radio-button[name='VIDEO_MADE_FOR_KIDS_NOT_MFK']")))
        radio_btn.click()

        # Click to add tags
        try:
            expand_button = WebDriverWait(driver, 10).until(
                ec.presence_of_element_located((By.XPATH, "//ytcp-button[@id='toggle-button']")))
            actions = ActionChains(driver)
            actions.move_to_element(expand_button).click().perform()
            time.sleep(3)

            input_tags = WebDriverWait(driver, 10).until(
                ec.presence_of_element_located((By.XPATH, "/html/body/ytcp-uploads-dialog/tp-yt-paper-dialog/div/ytcp-animatable[1]/ytcp-ve/ytcp-video-metadata-editor/div/ytcp-video-metadata-editor-advanced/div[5]/"
                                                        "ytcp-form-input-container/div[1]/div/ytcp-free-text-chip-bar/ytcp-chip-bar/div/input")))
            input_tags.send_keys(channel["tags"])
            time.sleep(3)
        except Exception as ex:
            print("Can't add the tags...")

        # Next buttons
        btn_next = WebDriverWait(driver, 10).until(
            ec.presence_of_element_located((By.XPATH, "//ytcp-button[@id='next-button']")))
        btn_next.click()
        btn_next = WebDriverWait(driver, 10).until(
            ec.presence_of_element_located((By.XPATH, "//ytcp-button[@id='next-button']")))
        btn_next.click()
        btn_next = WebDriverWait(driver, 10).until(
            ec.presence_of_element_located((By.XPATH, "//ytcp-button[@id='next-button']")))
        btn_next.click()

        publish_btn = WebDriverWait(driver, 10).until(
            ec.presence_of_element_located((By.CSS_SELECTOR, "tp-yt-paper-radio-button[name='PUBLIC']")))
        publish_btn.click()
        time.sleep(3)

        # Try to click "got it"
        try:
            driver.find_element(By.XPATH, "//*[@id='got-it-button']").click()
            time.sleep(3)
        except Exception as ex:
            pass

        # Done button
        done_btn = WebDriverWait(driver, 10).until(
            ec.presence_of_element_located((By.XPATH, "//ytcp-button[@id='done-button']")))
        done_btn.click()

        # Random delay
        time.sleep(random.randint(delay["from"], delay["to"]))

        try:
            cls_btn = WebDriverWait(driver, 10).until(
                ec.presence_of_element_located((By.XPATH, "//ytcp-button[text()='Close']")))
            cls_btn.click()
        except Exception as ex:
            pass

        try:
            cls_btn = WebDriverWait(driver, 10).until(
                ec.presence_of_element_located((By.XPATH, "/ytcp-video-share-dialog/ytcp-dialog/tp-yt-paper-dialog/div[3]/ytcp-button/div")))
            cls_btn.click()
        except Exception as ex:
            pass

        print("Uploaded successful!")

        link_to_channel = driver.find_element(By.XPATH, "//a[@id='overlay-link-to-youtube']").get_attribute("href")
        driver.get(link_to_channel)
        time.sleep(3)

        # Send comment
        if write_comment:
            try:
                link_video = driver.find_element(By.XPATH, "/html/body/ytd-app/div[1]/ytd-page-manager/ytd-browse[1]/ytd-two-column-browse-results-renderer/div[1]/ytd-section-list-renderer/div[2]/ytd-item-section-renderer[1]/"
                                                           "div[3]/ytd-reel-shelf-renderer/div[2]/yt-horizontal-list-renderer/div[2]/div/ytd-reel-item-renderer/div[1]/ytd-thumbnail/a").get_attribute("href")
                driver.get(link_video)

                comment_btn = WebDriverWait(driver, 10).until(
                    ec.presence_of_element_located((By.XPATH, "/html/body/ytd-app/div[1]/ytd-page-manager/ytd-shorts/div[3]/div[2]/ytd-reel-video-renderer[1]/div[3]/ytd-reel-player-overlay-renderer/div[2]/div[4]/ytd-button-renderer/yt-button-shape/label/button")))
                comment_btn.click()

                time.sleep(3)
                input_field = driver.find_element(By.XPATH, "/html/body/ytd-app/div[1]/ytd-page-manager/ytd-shorts/div[3]/div[2]/ytd-reel-video-renderer[1]/div[1]/ytd-engagement-panel-section-list-renderer[1]/div[2]/ytd-section-list-renderer/div[2]/ytd-comments/ytd-item-section-renderer/div[1]/ytd-comments-header-renderer/div[5]/ytd-comment-simplebox-renderer/div[3]/ytd-comment-dialog-renderer/ytd-commentbox/div[2]/div/div[2]/tp-yt-paper-input-container")
                input_field.click()
                input_field.send_keys(channel["link"])
                time.sleep(1)
                driver.find_element(By.XPATH, "/html/body/ytd-app/div[1]/ytd-page-manager/ytd-shorts/div[3]/div[2]/ytd-reel-video-renderer[1]/div[1]/ytd-engagement-panel-section-list-renderer[1]/div[2]/ytd-section-list-renderer/div[2]/ytd-comments/ytd-item-section-renderer/div[1]/ytd-comments-header-renderer/div[5]/ytd-comment-simplebox-renderer/div[3]/ytd-comment-dialog-renderer/ytd-commentbox/div[2]/div/div[4]/div[5]/ytd-button-renderer[2]/yt-button-shape/button").click()
            except Exception as ex:
                print(ex)

        time.sleep(delay_for_upload)
