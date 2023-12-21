from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from fake_useragent import UserAgent

import os
import time
import pickle
import zipfile
import requests
from datetime import datetime

from channels import save_cookies, existence_check, save_link, invalid_data
from upload import upload_video
from config import use_proxy, write_comment
from comment import send_com


# Options for webdriver
def get_options(channel):
    options = Options()
    user_agent = UserAgent()

    if use_proxy:
        options.add_extension(using_proxy(channel["proxy"]))

    options.add_argument('--no-sandbox')
    options.add_argument('--disable-gpu')
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument(f"--user-agent={user_agent.random}")

    return options


def using_proxy(proxy):
    manifest_json = """
                {
                    "version": "1.0.0",
                    "manifest_version": 2,
                    "name": "Chrome Proxy",
                    "permissions": [
                        "proxy",
                        "tabs",
                        "unlimitedStorage",
                        "storage",
                        "<all_urls>",
                        "webRequest",
                        "webRequestBlocking"
                    ],
                    "background": {
                    "scripts": ["background.js"]
                    },
                    "minimum_chrome_version": "76.0.0"
                }
                """

    background_js = """
                let config = {
                    mode: "fixed_servers",
                    rules: {
                        singleProxy: {
                            scheme: "http",
                            host: "%s",
                            port: parseInt(%s)
                        },
                        bypassList: ["localhost"]
                    }
                };
                chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});

                chrome.webRequest.onAuthRequired.addListener(
                    function(details) {
                        return {
                            authCredentials: {
                                username: "%s",
                                password: "%s"
                            }
                        };
                    },
                    {urls: ["<all_urls>"]},
                    ["blocking"]
                );
                """ % (proxy[0], proxy[1], proxy[2], proxy[3])

    plugin_file = f"source/proxies/proxy.zip"
    if not os.path.exists(plugin_file):
        with zipfile.ZipFile(plugin_file, 'w') as zp:
            zp.writestr("manifest.json", manifest_json)
            zp.writestr("background.js", background_js)

    return plugin_file


def authorization(channel):
    req_url = f"http://localhost:3001/v1.0/browser_profiles/{channel['id']}/start?automation=1"
    response = requests.get(req_url)

    response_json = response.json()
    print(response_json)
    port = str(response_json["automation"]["port"])
    print(port)

    time.sleep(10)

    chrome_path = Service("chromedriver/chromedriver-windows-x64-dolphin.exe")
    options = webdriver.ChromeOptions()
    options.debugger_address = "127.0.0.1:" + port

    driver = webdriver.Chrome(service=chrome_path, options=options)
    driver.get("https://www.youtube.com/")
    time.sleep(3)

    try:
        # try:
        #     # Getting link to channel
        #     icon = WebDriverWait(driver, 10).until(
        #         ec.presence_of_element_located((By.XPATH, "//button[@id='avatar-btn']")))
        #     icon.click()
        #
        #     link_to_channel = WebDriverWait(driver, 10).until(
        #         ec.presence_of_element_located((By.XPATH, "/html/body/ytd-app/ytd-popup-container/tp-yt-iron-dropdown/div/ytd-multi-page-menu-renderer/"
        #                                                     "div[3]/div[1]/yt-multi-page-menu-section-renderer[1]/div[2]/ytd-compact-link-renderer[1]/a"))).get_attribute("href")
        #
        #     if not existence_check(channel["login"]):
        #         save_link(channel["login"], link_to_channel)
        #         driver.refresh()
        #         time.sleep(10)
        # except Exception as ex:
        #     print("Error: can't write link to links.json")


        driver.find_element(By.XPATH, "/html/body/ytd-app/div[1]/div/ytd-masthead/div[4]/div[3]/div[2]/ytd-topbar-menu-button-renderer[1]/div/a/yt-icon-button/button").click()
        studio = driver.find_element(By.XPATH, "/html/body/ytd-app/ytd-popup-container/tp-yt-iron-dropdown/div/ytd-multi-page-menu-renderer/div[3]/div[1]/yt-multi-page-menu-section-renderer/div[2]/ytd-compact-link-renderer[1]/a").get_attribute("href")

        driver.get(studio)

        upload_video(driver, channel)

        if write_comment:
            link_to_channel = driver.find_element(By.XPATH, "//a[@id='overlay-link-to-youtube']").get_attribute("href")
            driver.get(link_to_channel)
            time.sleep(3)

            send_com(driver, channel)

        driver.close()
        driver.quit()

    except Exception as ex:
        print("Something went wrong... The driver is ended his work!")
        driver.close()
        driver.quit()
