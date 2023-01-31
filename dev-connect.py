from datetime import datetime
import urllib.parse
from dotenv import load_dotenv
from dateutil import parser
import os
import requests
import yaml
import json
import glob
import re

load_dotenv()

DEV_TO_API_KEY = os.environ["DEV_TO_API_KEY"]
API_URL = "https://dev.to/"

headers = {"api-key": DEV_TO_API_KEY}


class DEV_Post:
    """ """

    def __init__(self) -> None:
        self.__id: int = 0
        self.__title: str = ""
        self.__desc: str = ""
        self.__cover_img: str = ""
        self.__is_published: bool = False
        self.__published_ts: datetime = datetime.now()
        self.__slug: str = ""
        self.__body: str = ""
        self.__tags: list = []

    def load_json(self, post: dict):
        self.__id = post["id"]
        self.__title = post["title"]
        self.__desc = post["description"]
        self.__cover_img = post["cover_image"]
        self.__is_published = post["published"]
        self.__published_ts = parser.parse(post["published_at"])
        self.__slug = post["slug"]
        self.__tags = post["tag_list"]
        self.__body = post["body_markdown"]

    def load_md(self, post: str):
        yml_content = re.findall("---([\\s\\S]+)---", post)
        if len(yml_content) > 0:
            post_yml = yaml.safe_load(yml_content[0])
            self.__id = post_yml["id"]
            self.__title = post_yml["title"]
            self.__desc = post_yml["description"]
            self.__cover_img = post_yml["cover_image"]
            self.__is_published = post_yml["published"]
            self.__published_ts = post_yml["published_at"]
            self.__slug = post_yml["slug"]
            self.__tags = post_yml["tag_list"]

    def save_md(self, dir="content"):
        try:
            with open(
                os.path.join(dir, self.__slug) + ".md", "w+", encoding="utf-8"
            ) as f:
                f.write("---\n")
                yaml.dump(
                    {
                        "id": self.__id,
                        "title": self.__title,
                        "published": self.__is_published,
                        "published_at": self.__published_ts,
                        "description": self.__desc,
                        "tag_list": self.__tags,
                        "cover_image": self.__cover_img,
                        "slug": self.__slug,
                    },
                    f,
                    indent=4,
                )
                f.write("---\n")
                f.write(self.__body)
            return True
        except Exception as e:
            print(e)
            return False

    def __str__(self) -> str:
        return json.dumps(
            {
                "id": self.__id,
                "title": self.__title,
                "tags": self.__tags,
                "description": self.__desc,
                "slug": self.__slug,
                "published": self.__is_published,
                "published_at": str(self.__published_ts),
                "cover_image": self.__cover_img,
            },
            indent=4,
        )


def pull_my_posts():
    """ """
    url = urllib.parse.urljoin(API_URL, "/api/articles/me", allow_fragments=True)
    res = requests.get(url, headers=headers)
    posts = res.json()
    for post in posts:
        dev_post = DEV_Post()
        dev_post.load_json(post=post)
        dev_post.save_md()


def publish_my_posts():
    """ """
    md_posts = []
    for md_file in list(glob.glob(os.path.join("content", "*.md"))):
        with open(md_file, "r", encoding="utf-8") as f:
            dev_post = DEV_Post()
            dev_post.load_md(f.read())
            md_posts.append(md_posts)
    md_posts = list(filter(lambda post: post.is_published == True))
    # Check for updates
    # Check for published


def publish_my_post(post_name: str):
    pass


if __name__ == "__main__":
    # pull_my_posts()
    publish_my_posts()
