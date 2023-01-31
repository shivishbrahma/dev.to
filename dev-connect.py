from datetime import date, datetime
import urllib.parse
from dotenv import load_dotenv
import os
import json
import requests
import yaml

load_dotenv()

DEV_TO_API_KEY = os.environ["DEV_TO_API_KEY"]
API_URL = "https://dev.to/"

headers = {"api-key": DEV_TO_API_KEY}


class DEV_Post:
    def __init__(self, post) -> None:
        self.__id: int = post["id"]
        self.__title: str = post["title"]
        self.__desc: str = post["description"]
        self.__cover_img: str = post["cover_image"]
        self.__is_published: bool = post["published"]
        self.__published_ts: datetime = post["published_at"]
        self.__slug: str = post["slug"]
        self.__body: str = post["body_markdown"]
        self.__tags: list = post["tag_list"]

    def save(self, dir="content"):
        try:
            with open(os.path.join(dir, self.__slug) + ".md", "w+") as f:
                f.write("---\n")
                yaml.dump(
                    {
                        "id": self.__id,
                        "title": self.__title,
                        "published": self.__is_published,
                        "published_at": self.__published_ts,
                        "description": self.__desc,
                        "tags": self.__tags,
                        "cover_image": self.__cover_img,
                    },
                    f,
                )
                f.write("---\n")
                f.write(self.__body)
            return True
        except Exception as e:
            print(e)
            return False


def get_my_posts():
    url = urllib.parse.urljoin(API_URL, "/api/articles/me", allow_fragments=True)
    print(url)
    res = requests.get(url, headers=headers)
    posts = res.json()
    for post in posts:
        dev_post = DEV_Post(post)
        dev_post.save()

get_my_posts()