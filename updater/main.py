import json
import sys
import time

import requests

session = requests.Session()
session.headers[
    "User-Agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.51"


def provide() -> dict:
    page = 1
    global session
    r = session.get("https://www.bilibili.com/")

    if "debug" in sys.argv:
        print(r.status_code)
        print(session.cookies.get_dict())

    while True:
        data = {
            "search_type": "video",
            "keyword": "同步至节奏医生视频合集" if "debug" not in sys.argv else "节奏医生",
            "order": "pubdate",
            "tids": 4,
            "page": page,
        }
        page += 1

        result = session.get("https://api.bilibili.com/x/web-interface/search/type", params=data).json()
        if result["code"] != 0:
            raise ValueError(f"Result code {result['code']}: {result['message']}")

        for item in result["data"]["result"]:
            yield item


def load_existed_authors() -> set:
    try:
        file_name = "../docs/authors.txt" if "debug" not in sys.argv else "debug_authors.txt"
        authors = set()
        with open(file_name, "rt", encoding="utf-8") as f:
            for line in f.read().splitlines():
                if len(line) <= 0 or line.isspace() or line.startswith("#"):
                    continue

                authors.add(line.split('|')[1])
        return authors
    except FileNotFoundError:
        return set()


def load_config() -> dict:
    try:
        with open("config.json", "rt", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {
            "timestamp": int(time.time()) - 60 * 60 * 24,
        }


def save_config(config: dict):
    with open("config.json", "wt", encoding="utf-8") as f:
        json.dump(config, f)


if __name__ == '__main__':
    authors_existed = load_existed_authors()
    config = load_config()

    author_file_name = "../docs/authors.txt" if "debug" not in sys.argv else "debug_authors.txt"
    video_file_name = "../docs/videos.txt" if "debug" not in sys.argv else "debug_videos.txt"
    with open(author_file_name, "at", encoding="utf-8") as author_file, open(video_file_name, "at",
                                                                             encoding="utf-8") as video_file:
        for video in provide():
            if video["senddate"] < config["timestamp"]:
                break

            if "tag" not in video["hit_columns"]:
                continue

            author_id = video["mid"]
            if author_id not in authors_existed:
                author_name = video["author"].replace("|", "·")
                print(f"Found new author {author_name} with id {author_id}.")
                author_file.write(f"{author_name}|{author_id}\n")
                authors_existed.add(author_id)

            bvid = video["bvid"]
            video_name = video["title"].replace("<em class=\"keyword\">", "").replace("</em>", "").replace("|", "·")

            print(f"Found new video {video_name} with bvid {bvid} and author {author_id}.")
            video_file.write(f"{author_id}|{bvid}|{video_name}\n")

    config["timestamp"] = int(time.time())
    save_config(config)
