import json
import sys
import time

import requests

session = requests.Session()
session.headers["User-Agent"] = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.51"
)


def provide():
    page = 1
    global session
    r = session.get("https://www.bilibili.com/")

    if "debug" in sys.argv:
        print(r.status_code)
        print(session.cookies.get_dict())

    while True:
        data = {
            "search_type": "video",
            "keyword": (
                "同步至节奏医生视频合集" if "debug" not in sys.argv else "节奏医生"
            ),
            "order": "pubdate",
            "tids": 4,
            "page": page,
        }
        page += 1

        result = session.get(
            "https://api.bilibili.com/x/web-interface/search/type", params=data
        ).json()
        if result["code"] != 0:
            raise ValueError(f"Result code {result['code']}: {result['message']}")

        for item in result["data"]["result"]:
            yield item


showlist_file_name = (
    "../docs/showlist.json" if "debug" not in sys.argv else "debug_showlist.json"
)


def load_showlist() -> dict:
    try:
        with open(showlist_file_name, "rt", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {
            "timestamp": int(time.time()) - 60 * 60 * 24,
            "authors": {},
        }


def save_showlist(config: dict):
    with open(showlist_file_name, "wt", encoding="utf-8") as f:
        json.dump(config, f, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    now = int(time.time())
    data = load_showlist()

    author_file_name = (
        "../docs/authors.txt" if "debug" not in sys.argv else "debug_authors.txt"
    )
    video_file_name = (
        "../docs/videos.txt" if "debug" not in sys.argv else "debug_videos.txt"
    )
    for video in provide():
        if video["senddate"] < data["timestamp"]:
            break

        if "tag" not in video["hit_columns"]:
            continue

        author_id = video["mid"]
        if str(author_id) not in data["authors"]:
            author_name = video["author"]
            print(f"Found new author {author_name} with id {author_id}.")
            data["authors"][str(author_id)] = {
                "id": author_id,
                "name": author_name,
                "videos": {},
            }

        bvid = video["bvid"]
        video_name = (
            video["title"].replace('<em class="keyword">', "").replace("</em>", "")
        )

        print(f"Found new video {video_name} with bvid {bvid} and author {author_id}.")
        data["authors"][str(author_id)]["videos"][bvid] = {
            "id": bvid,
            "title": video_name,
        }

    if "debug" not in sys.argv:
        data["timestamp"] = now
    save_showlist(data)
