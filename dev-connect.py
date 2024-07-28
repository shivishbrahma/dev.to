import datetime
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
from strip_markdown import strip_markdown
import string

load_dotenv()


def null_if(value, def_val):
    if value is None:
        return def_val
    return value


class DEVPost:
    """
    DEV Post class
    """

    def __init__(self, **kwargs) -> None:
        self.__id: int = -1
        self.__title: str = "Sample Title"
        self.__desc: str = "Body Content..."
        self.__cover_img: str = ""
        self.__is_published: bool = False
        self.__is_updated: bool = False
        self.__published_ts: datetime = None
        self.__slug: str = "post-slug"
        self.__body: str = "Body Content"
        self.__tags: list = []
        self.__series = None
        self.__created_ts = None
        self.__edited_ts = None

        post_def = {
            "id": -1,
            "title": "Sample Title",
            "description": "Body Content...",
            "cover_image": "",
            "published": False,
            "published_at": None,
            "slug": "post-slug",
            "body_markdown": "Body Content",
            "tags": [],
            "series": None,
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
                "tags",
                "series",
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
        return str(self.__tags)

    @property
    def published(self) -> str:
        return str(self.__is_published)

    @property
    def updated(self) -> str:
        return str(self.__is_updated)

    @property
    def published_ts(self):
        return self.__published_ts

    def load_json(self, post: dict):
        self.__id = post["id"]
        self.__title = post["title"]
        self.__desc = post["description"]
        self.__cover_img = post["cover_image"]
        if "published_timestamp" in post.keys() and "published" not in post.keys():
            post["published"] = post["published_timestamp"] is not None and post[
                "published_timestamp"
            ] not in ["null", ""]
        self.__is_published = null_if(post["published"], False)
        if post["published_at"] is not None:
            self.__published_ts = dateutil.parser.parse(str(post["published_at"]))
        if "series" in post.keys() and post["series"] is not None:
            self.__series = post["series"]
        if "collection_id" in post.keys() and post["collection_id"] is not None:
            self.__series = post["collection_id"]
        if "created_at" in post.keys() and post["created_at"] is not None:
            self.__created_ts = dateutil.parser.parse(str(post["created_at"]))
        if "edited_at" in post.keys() and post["edited_at"] is not None:
            self.__edited_ts = dateutil.parser.parse(str(post["edited_at"]))
        self.__slug = post["slug"]
        if "tag_list" in post.keys() and (
            "tags" not in post.keys() or post["tags"] is not None
        ):
            if isinstance(post["tag_list"], list):
                post["tags"] = post["tag_list"]
            elif isinstance(post["tag_list"], str):
                post["tags"] = post["tag_list"].split(", ")
        self.__tags = post["tags"]
        self.__body = post["body_markdown"].strip()

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
            self.__is_published = null_if(post_yml["published"], False)
            self.__published_ts = post_yml["published_at"]
            self.__slug = post_yml["slug"]
            self.__tags = (
                post_yml["tags"].split(",")
                if isinstance(post_yml["tags"], str)
                else post_yml["tags"]
            )
        if len(md_content) > 0:
            self.__body = md_content[0].strip()
        # logger.debug(self.__body)

    def save_md(self, dir="content"):
        try:
            file_path = os.path.join(dir, self.__slug) + ".md"
            with open(file_path, "w+", encoding="utf-8") as f:
                f.write("---\n")
                yaml_data = {
                    "id": self.__id,
                    "title": self.__title,
                    "published": self.__is_published,
                    "published_at": self.__published_ts,
                    "description": self.__desc,
                    "tags": self.__tags,
                    "cover_image": self.__cover_img,
                    "slug": self.__slug,
                }
                if self.__series is not None:
                    yaml_data["series"] = self.__series
                if self.__created_ts is not None:
                    yaml_data["created_at"] = self.__created_ts
                if self.__edited_ts is not None:
                    yaml_data["edited_at"] = self.__edited_ts
                yaml.dump(
                    yaml_data,
                    f,
                    indent=4,
                )
                f.write("---\n")
                f.write(self.__body)
                f.write("\n")
                logger.info(f"Article successfully saved to {file_path}!")
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
                "body": self.__body[:100] + "...",
            },
            indent=4,
        )

    def unpublish(self) -> bool:
        if not self.__is_published:
            url = urllib.parse.urljoin(API_URL, f"/api/articles/{self.__id}/unpublish")
            res = requests.put(url=url, headers=headers)
            if res.status_code == 204:
                logger.info("Article successfully unpublished!")
                return True
            else:
                logger.error(f"Error unpublishing article: {res.json()}")
                return False
        else:
            logger.error("Article is not unpublished! Try with different article")
            return False

    def publish(self) -> bool:
        if self.__is_published:
            url = urllib.parse.urljoin(API_URL, f"/api/articles/{self.__id}/unpublish")
        else:
            logger.error("Article is not published! Try with different article")
        return True

    def generate_description(self) -> str:
        """
        Convert markdown into simple text and return first 100 characters such that last word is complete
        """
        markdown_text = strip_markdown(self.__body).replace("\n", " ")
        if len(markdown_text) > 100:
            i = 100
            while i > len(markdown_text) or markdown_text[i] not in string.whitespace:
                i += 1
            markdown_text = markdown_text[:i] + "..."

        return markdown_text

    def update(self) -> bool:
        url = urllib.parse.urljoin(API_URL, f"/api/articles/{self.__id}")
        data = {
            "article": {
                "title": self.__title,
                "body_markdown": self.__body,
                "description": self.generate_description(),
                "published": self.__is_published,
                "tags": self.__tags,
            }
        }
        # logger.debug(data)
        res = requests.put(url=url, headers=headers, json=data)
        if res.status_code == 200:
            logger.info("Article successfully updated!")
            post = res.json()
            self.load_json(post)
            self.save_md()
            return True
        else:
            logger.error(f"Error updating article: {res.json()}")
            return False

    @staticmethod
    def load_post_local(id, filename=None):
        """
        Load post from local file
        """
        md_filename = filename
        if filename is None:
            with open(POSTS_METADATA, "r", encoding="utf-8") as f:
                posts = json.load(f)
                post = list(filter(lambda post: post["id"] == id, posts))
                if len(post) > 0:
                    md_filename = post[0]["filename"]

        post = DEVPost(id=id)
        post.load_md(
            open(os.path.join(CONTENT_DIR, md_filename), "r", encoding="utf-8").read()
        )
        return post

    @staticmethod
    def load_post_online(id):
        """
        Load post from dev.to
        """
        url = urllib.parse.urljoin(API_URL, f"/api/articles/{id}")
        res = requests.get(url, headers=headers)
        if res.status_code == 200:
            post = DEVPost(id=id)
            res_json = res.json()
            res_json["published"] = True
            post.load_json(res_json)
            return post
        else:
            logger.error(f"Error loading article: {res.json()}")
            return None


def pull_my_posts(id=None):
    """
    Pull all my posts from dev.to
    """
    url = urllib.parse.urljoin(API_URL, "/api/articles/me/all")
    res = requests.get(url, headers=headers)
    post_meta_list = []
    if os.path.exists(POSTS_METADATA):
        with open(POSTS_METADATA, "r", encoding="utf-8") as f:
            posts = json.load(f)
            for post in posts:
                post_meta_list.append(json.dumps(post))

    if res.status_code == 200:
        posts = res.json()
        posts_new = []
        for post in posts:
            post_meta = {"id": post["id"], "filename": post["slug"] + ".md"}
            if post["published"]:
                dev_post = DEVPost.load_post_online(id=post["id"])
            else:
                dev_post = DEVPost()
                dev_post.load_json(post=post)
            dev_post.save_md()
            posts_new.append(json.dumps(post_meta))

        post_meta_list.extend(posts_new)
        post_meta_list = list(set(post_meta_list))

        for i, post in enumerate(post_meta_list):
            post_meta_list[i] = json.loads(post)

        # Sort the posts by post_id
        post_meta_list = sorted(post_meta_list, key=lambda post: post["id"])

        with open(POSTS_METADATA, "w", encoding="utf-8") as f:
            json.dump(post_meta_list, f, indent=4)

        logger.info("Articles pulled successfully!")
    else:
        logger.error(f"Error pulling articles: {res.json()}")


def load_posts():
    posts_list = []
    post_meta_list = []

    if os.path.exists(POSTS_METADATA):
        with open(POSTS_METADATA, "r", encoding="utf-8") as f:
            posts = json.load(f)
            for post_meta in posts:
                post_meta_list.append(json.dumps(post_meta))
                posts_list.append(DEVPost.load_post_local(**post_meta))


def publish_my_posts():
    """"""
    md_posts = []
    for md_file in list(glob.glob(os.path.join(CONTENT_DIR, "*.md"))):
        with open(md_file, "r", encoding="utf-8") as f:
            dev_post = DEVPost()
            dev_post.load_md(f.read())
            md_posts.append(dev_post)
    md_posts = list(filter(lambda post: post.published, md_posts))
    # Check for updates
    # Check for published


def publish_my_post(post: DEVPost):
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


def create_new_post(title: str):
    """
    Create a new post template
    """
    publish_my_post(DEVPost(title=title, published=False))
    # pull_my_posts()


def update_my_post(post_id: int):
    """
    Update the post
    """
    post = DEVPost.load_post_local(id=post_id)
    post.update()


def show_my_post(post_id: int):
    """
    Show the post
    """
    post = DEVPost.load_post_local(id=post_id)
    print(post)


def main():
    arg_parser = ArgumentParser()
    arg_parser.add_argument(
        "--create", "-c", type=str, help="Create a new post template"
    )
    arg_parser.add_argument("--update", "-u", type=int, help="Update the post by id")
    arg_parser.add_argument("--pull", action="store_true", help="Pull posts")
    arg_parser.add_argument("--show", "-s", type=int, help="Show posts")

    args = arg_parser.parse_args()

    if args.create:
        create_new_post(args.create)
        sys.exit(0)

    if args.pull:
        pull_my_posts()

    if args.update:
        update_my_post(args.update)

    if args.show:
        show_my_post(args.show)

    # publish_my_posts()


if __name__ == "__main__":
    API_URL = "https://dev.to/"
    POSTS_METADATA = "posts.json"
    CONTENT_DIR = "content"

    headers = {
        "api-key": os.environ.get("DEV_TO_API_KEY"),
        "Content-Type": "application/json",
        "Accept": "application/vnd.forem.api-v1+json",
    }

    logger = logging.getLogger("dev_connect")
    logger.setLevel(os.environ.get("LOG_LEVEL", "INFO"))

    # Add color to the logging output
    coloredlogs.install(level="DEBUG", logger=logger)

    main()
