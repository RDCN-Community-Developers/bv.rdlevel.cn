import json
import sys
import time


def load_existed_authors() -> set:
    try:
        file_name = "../docs/authors.txt" if "debug" not in sys.argv else "debug_authors.txt"
        authors = list()
        with open(file_name, "rt", encoding="utf-8") as f:
            for line in f.read().splitlines():
                if len(line) <= 0 or line.isspace() or line.startswith("#"):
                    continue

                authors.append(line.split("|"))
        return authors
    except FileNotFoundError:
        return list()

def load_existed_videos() -> set:
    try:
        file_name = "../docs/videos.txt" if "debug" not in sys.argv else "debug_videos.txt"
        videos = list()
        with open(file_name, "rt", encoding="utf-8") as f:
            for line in f.read().splitlines():
                if len(line) <= 0 or line.isspace() or line.startswith("#"):
                    continue

                videos.append(line.split("|"))
        return videos
    except FileNotFoundError:
        return list()
            

def load_config() -> dict:
    try:
        with open("config.json", "rt", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {
            "timestamp": int(time.time()) - 60 * 60 * 24,
        }


if __name__ == "__main__":
    data = load_config()
    data["authors"] = {}
    for author in load_existed_authors():
        id = int(author[1])
        data["authors"][id] = {
            "id": id,
            "name": author[0],
        }
        if len(author) > 2:
            data["authors"][id]["avatar"] = author[2]
        data["authors"][id]["videos"] = {}

    for author_id, video_id, title in load_existed_videos():
        data["authors"][int(author_id)]["videos"][video_id] = {
            "id": video_id,
            "title": title,
        }

    with open("../docs/showlist.json", "wt", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
