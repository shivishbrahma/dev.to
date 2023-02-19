from datetime import datetime
import urllib.parse
from dotenv import load_dotenv
import dateutil.parser
import os
import sys
import requests
import yaml
import json
import glob
import re
import logging
import coloredlogs
from argparse import ArgumentParser

load_dotenv()

API_URL = "https://dev.to/"

headers = {
    "api-key": os.environ.get("DEV_TO_API_KEY"),
    "Content-Type": "application/json",
}

logger = logging.getLogger('dev_connect')
logger.setLevel(os.environ.get("LOG_LEVEL"))

# Add color to the logging output
coloredlogs.install(level='DEBUG', logger=logger)

class DEV_Post:
    """ """

    def __init__(self, **kwargs) -> None:
        self.__id: int = -1
        self.__title: str = "Sample Title"
        self.__desc: str = "Body Content..."
        self.__cover_img: str = ""
        self.__is_published: bool = False
        self.__published_ts: datetime = datetime.now()
        self.__slug: str = "post-slug"
        self.__body: str = "Body Content"
        self.__tags: list = []

        post_def = {
            "id": -1,
            "title": "Sample Title",
            "description": "Body Content...",
            "cover_image": "",
            "published": False,
            "published_at": datetime.utcnow(),
            "slug": "post-slug",
            "body_markdown": "Body Content",
            "tag_list": [],
        }

        for key, val in kwargs.items():
            if key in [
                "id",
                "title",
                "description",
                "cover_image",
                "published",
                "published_at",
                "slug",
                "body_markdown",
                "tag_list",
            ]:
                post_def[key] = val
        self.load_json(post_def)

    @property
    def title(self) -> str:
        return self.__title

    @property
    def body(self) -> str:
        return self.__body

    @property
    def tags(self) -> str:
        return self.__tags

    @property
    def published(self) -> str:
        return self.__is_published

    @property
    def published_ts(self):
        return self.__published_ts

    def load_json(self, post: dict):
        self.__id = post["id"]
        self.__title = post["title"]
        self.__desc = post["description"]
        self.__cover_img = post["cover_image"]
        self.__is_published = post["published"]
        if post["published_at"] is not None:
            self.__published_ts = dateutil.parser.parse(str(post["published_at"]))
        self.__slug = post["slug"]
        self.__tags = post["tag_list"]
        self.__body = post["body_markdown"]

    def load_md(self, post: str):
        yml_content = re.findall("---([\\s\\S]+)---", post)
        md_content = re.findall("---[\\s\\S]+---([\\s\\S]+)", post)
        # logger.debug(yml_content)
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
        if len(md_content) > 0:
            self.__body = md_content[0].strip()
        logger.debug(self.__body)

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

    def unpublish(self) -> str:
        if not self.__is_published:
            url = urllib.parse.urljoin(API_URL, f"/api/articles/{self.__id}/unpublish")
            res = requests.put(url=url, headers=headers)
            if res.status_code == 204:
                logger.info("Article successfully unpublished!")
            else:
                logger.error(f"Error unpublishing article: {res.json()}")
        else:
            logger.error("Article is not unpublished! Try with different article")

    def publish(self) -> str:
        if self.__is_published:
            url = urllib.parse.urljoin(API_URL, f"/api/articles/{self.__id}/unpublish")
        else:
            logger.error("Article is not published! Try with different article")


def pull_my_posts():
    """ """
    url = urllib.parse.urljoin(API_URL, "/api/articles/me/all")
    res = requests.get(url, headers=headers)
    posts_dict = []
    if os.path.exists("posts.json"):
        with open("posts.json", "r", encoding="utf-8") as f:
            posts = json.load(f)
            for post in posts:
                posts_dict.append(json.dumps(post))

    if res.status_code == 200:
        posts = res.json()
        posts_new = []
        for post in posts:
            dev_post = DEV_Post()
            dev_post.load_json(post=post)
            dev_post.save_md()
            post_meta = {"id": post["id"], "filename": post["slug"] + ".md"}
            posts_new.append(json.dumps(post_meta))

        posts_dict.extend(posts_new)
        posts_dict = list(set(posts_dict))

        for i, post in enumerate(posts_dict):
            posts_dict[i] = json.loads(post)


        with open("posts.json", "w", encoding="utf-8") as f:
            json.dump(posts_dict, f, indent=4)

        logger.info("Articles pulled successfully!")
    else:
        logger.error(f"Error pulling articles: {res.json()}")


def publish_my_posts():
    """ """
    md_posts = []
    for md_file in list(glob.glob(os.path.join("content", "*.md"))):
        with open(md_file, "r", encoding="utf-8") as f:
            dev_post = DEV_Post()
            dev_post.load_md(f.read())
            md_posts.append(dev_post)
    md_posts = list(filter(lambda post: post.published, md_posts))
    # Check for updates
    # Check for published


def publish_my_post(post: DEV_Post):
    """
    Parse the posts and publish & update the post
    """
    url = urllib.parse.urljoin(API_URL, "/api/articles")
    data = {
        "article": {
            "title": post.title,
            "body_markdown": post.body,
            "published": post.published,
            "tags": post.tags,
        }
    }
    logger.debug(data)
    res = requests.post(url=url, headers=headers, json=data)

    if res.status_code == 201:
        logger.info("Article published successfully!")
    else:
        logger.error(f"Error publishing Article: {res.json()}")


def create_new_post(title):
    """
    Create a new post template
    """
    publish_my_post(DEV_Post(title=title))
    # pull_my_posts()


if __name__ == "__main__":
    arg_parser = ArgumentParser()
    arg_parser.add_argument(
        "--create", "-c", type=str, help="Create a new post template"
    )
    arg_parser.add_argument("--pull", action="store_true", help="Pull posts")

    args = arg_parser.parse_args()

    if args.create:
        create_new_post(args.create)
        sys.exit(0)

    if args.pull:
        pull_my_posts()

    publish_my_posts()
