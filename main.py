from selenium import webdriver

import threading
import time

from channels import get_channels
from auth import authorization
from config import use_proxy


def change_ip(link_to_change_ip):
    with webdriver.Chrome() as driver:
        driver.get(link_to_change_ip)
        time.sleep(5)


if __name__ == '__main__':
    i = 0
    while True:
        channels = get_channels(i)
        if not channels:
            print("Channels is ended!")
            break

        threads = []

        for channel in channels:
            thread = threading.Thread(target=authorization, args=(channel, ))
            thread.start()
            threads.append(thread)

        for thread in threads:
            thread.join()

        if use_proxy:
            change_ip(channels[0]["changeLinkProxy"])

        i += 1
