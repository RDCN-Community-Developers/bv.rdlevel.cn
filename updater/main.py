import json
import os
import sys
import time

import requests

now = int(time.time())

session = requests.Session()
session.headers["User-Agent"] = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.51"
)
session.headers["X-Upload-Key"] = os.environ.get("X_UPLOAD_KEY", "x-upload-key")
if "debug" in sys.argv:
    print("key:", session.headers["X-Upload-Key"])

r = session.get("https://www.bilibili.com/")
if "debug" in sys.argv:
    print(r.status_code)
    print(session.cookies.get_dict())

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


showlist = load_showlist()


def provide_with_tag():
    page = 1

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
            if "tag" not in item["hit_columns"]:
                continue

            if item["senddate"] < showlist["timestamp"]:
                return

            yield {
                "author_id": item["mid"],
                "author_name": item["author"],
                "bvid": item["bvid"],
                "video_name": item["title"]
                .replace('<em class="keyword">', "")
                .replace("</em>", ""),
            }


def provide_with_id():
    ids = session.get("https://api.rdlevel.cn/bv/video").json()
    for id in ids:
        if id.lower().startswith("bv"):
            data = {
                "bvid": f"BV{id[2:]}",
            }
        elif id.lower().startswith("av"):
            data = {
                "aid": int(id[2:]),
            }
        else:
            continue

        result = session.get(
            "https://api.bilibili.com/x/web-interface/view", params=data
        ).json()
        if result["code"] != 0:
            raise ValueError(f"Result code {result['code']}: {result['message']}")
        item = result["data"]

        tag_result = session.get(
            "https://api.bilibili.com/x/tag/archive/tags", params=data
        ).json()
        if tag_result["code"] != 0:
            raise ValueError(
                f"Result code {tag_result['code']}: {tag_result['message']}"
            )
        detects = [*map(lambda x: x["tag_name"], tag_result["data"]), item["title"]]
        if "debug" in sys.argv:
            print(detects)
        if not any(
            map(lambda x: ("节奏医生" in x) or ("rhythm doctor" in x.lower()), detects)
        ):
            continue

        yield {
            "author_id": item["owner"]["mid"],
            "author_name": item["owner"]["name"],
            "bvid": item["bvid"],
            "video_name": item["title"],
        }

    session.delete("https://api.rdlevel.cn/bv/video")


def add_video(video: dict):
    author_id = video["author_id"]
    if str(author_id) not in showlist["authors"]:
        author_name = video["author_name"]
        print(f"Found new author {author_name} with id {author_id}.")
        showlist["authors"][str(author_id)] = {
            "id": author_id,
            "name": author_name,
            "videos": {},
        }

    bvid = video["bvid"]
    video_name = video["video_name"]

    print(f"Found new video {video_name} with bvid {bvid} and author {author_id}.")
    showlist["authors"][str(author_id)]["videos"][bvid] = {
        "id": bvid,
        "title": video_name,
    }


if __name__ == "__main__":
    for video in provide_with_tag():
        add_video(video)

    for video in provide_with_id():
        add_video(video)

    if "debug" not in sys.argv:
        showlist["timestamp"] = now
    save_showlist(showlist)
