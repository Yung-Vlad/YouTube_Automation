import json
import pickle
import os

from config import count_threads


def reading_json(file_path):
    if os.path.getsize(file_path) == 0:
        return None

    with open(file_path, encoding="UTF-8") as file:
        return json.load(file)


# Reading a json-file with channels info
def get_channels(i):
    channels = reading_json("source/channels.json")

    if channels:
        return channels[i * count_threads:(i + 1) * count_threads]


# Save cookies if not exists
def save_cookies(cookies, channel_login):
    pickle.dump(cookies, open(f"source/cookies/{channel_login}.pkl", "wb"))


def existence_check(channel_login):
    channels = reading_json("source/links.json")

    if channels:
        for channel in channels:
            if channel["login"] == channel_login:
                return True

    return False


def save_link(login, link):
    obj = {
        "login": login,
        "link": link
    }

    channels = reading_json("source/links.json")
    if not channels:
        channels = []

    channels.append(obj)

    with open("source/links.json", 'w', encoding="UTF-8") as file:
        json.dump(channels, file, indent=4, ensure_ascii=False)


def invalid_data(channel):
    channels = reading_json("source/invalid.json")
    if not channels:
        channels = [channel]
    elif channel not in channels:
        channels.append(channel)

    with open("source/invalid.json", 'w', encoding="UTF-8") as file:
        json.dump(channels, file, ensure_ascii=False, indent=4)
