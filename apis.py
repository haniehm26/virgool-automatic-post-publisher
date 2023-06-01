from requests import Session
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager


class VirgoolAPI:
    def __init__(self) -> None:
        self.session = Session()
        self.arcsjs_cookie = self.get_arcsjs_cookie()
        self.session.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/113.0",
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate, br",
            "Cookie": self.arcsjs_cookie["name"] + "=" + self.arcsjs_cookie["value"],
        }

    def get_arcsjs_cookie(self) -> dict:
        options = webdriver.ChromeOptions()
        options.add_argument("--no-sandbox")
        options.add_argument("--headless")
        driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
        driver.get("https://virgool.io/")
        cookie = WebDriverWait(driver, timeout=120).until(lambda d: d.get_cookie("__arcsjs"))
        arcsjs_cookie = {"name": cookie["name"], "value": cookie["value"]}
        driver.quit()
        return arcsjs_cookie

    # OK
    def login(self, username: str, password: str):
        session = self.session
        url = "https://virgool.io/api/v1.4/auth/login"
        payload = {"username": username, "password": password}
        response = session.post(url, data=payload, headers=session.headers)
        return response

    # OK
    def get_drafts(self):
        session = self.session
        arcsjs_cookie = self.arcsjs_cookie
        session.cookies.set(arcsjs_cookie["name"], arcsjs_cookie["value"], domain="virgool.io")
        url = "https://virgool.io/api/v1.4/posts/drafts"
        response = session.get(url, headers=session.headers, cookies=session.cookies)
        return response

    # OK
    def get_publishments(self):
        session = self.session
        arcsjs_cookie = self.arcsjs_cookie
        session.cookies.set(arcsjs_cookie["name"], arcsjs_cookie["value"], domain="virgool.io")
        url = "https://virgool.io/api/v1.4/posts/published"
        response = session.get(url, headers=session.headers, cookies=session.cookies)
        return response

    # OK
    def fetch_draft_editor_by_hash(self, post_hash: str):
        session = self.session
        arcsjs_cookie = self.arcsjs_cookie
        session.cookies.set(arcsjs_cookie["name"], arcsjs_cookie["value"], domain="virgool.io")
        url = "https://virgool.io/api/v1.4/editor/fetch/d/" + post_hash
        response = session.get(url, headers=session.headers, cookies=session.cookies)
        return response

    # OK
    def fetch_published_editor_by_hash(self, post_hash: str):
        session = self.session
        arcsjs_cookie = self.arcsjs_cookie
        session.cookies.set(arcsjs_cookie["name"], arcsjs_cookie["value"], domain="virgool.io")
        url = "https://virgool.io/api/v1.4/editor/fetch/p/" + post_hash
        response = session.get(url, headers=session.headers, cookies=session.cookies)
        return response

    # OK
    def fetch_post_by_hash(self, post_hash: str):
        session = self.session
        arcsjs_cookie = self.arcsjs_cookie
        session.cookies.set(arcsjs_cookie["name"], arcsjs_cookie["value"], domain="virgool.io")
        url = "https://virgool.io/api/v1.4/post/" + post_hash
        response = session.get(url, headers=session.headers, cookies=session.cookies)
        return response

    # OK BUT CAN NOT CHANGE TAGS YET
    def edit_post(self, pyload: dict, body: str, description: str = None, tags: list = None):
        data = {
            "post_id": pyload["id"],
            "hash": pyload["hash"],
            "title": pyload["title"],
            "primary_img": pyload["primary_img"],
            "customized_slug": "",
            "words_count": 0,
            "body": body,
            # "tag": pyload["tags"] if tags is None else tags,
            "tag": "" if tags is None else tags,
            "og_description": pyload["description"] if description is None else description,
        }
        session = self.session
        arcsjs_cookie = self.arcsjs_cookie
        session.cookies.set(arcsjs_cookie["name"], arcsjs_cookie["value"], domain="virgool.io")
        url = "https://virgool.io/api/v1.4/editor/draft"
        response = session.post(url, headers=session.headers, cookies=session.cookies, data=data)
        return response, data

    # OK
    def publish_post(self, pyload: dict):
        data = {
            "post_id": pyload["post_id"],
            "hash": pyload["hash"],
            "title": pyload["title"],
            "body": pyload["body"],
            "customized_slug": pyload["customized_slug"],
            "tag": pyload["tag"],
            "words_count": pyload["words_count"],
            "og_description": pyload["og_description"],
            "primary_img": pyload["primary_img"],
            "publication_hash": None,
        }
        session = self.session
        arcsjs_cookie = self.arcsjs_cookie
        session.cookies.set(arcsjs_cookie["name"], arcsjs_cookie["value"], domain="virgool.io")
        url = "https://virgool.io/api/v1.4/editor/publish"
        response = session.post(url, headers=session.headers, cookies=session.cookies, data=data)
        return response


def send_telegram_message(proxy: dict, bot_token: str, chat_id: str, text: str):
    session = Session()
    session.headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/113.0",
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate, br",
    }
    session.proxies = proxy
    url = (
        "https://api.telegram.org/bot"
        + bot_token
        + "/sendMessage?chat_id="
        + chat_id
        + "&text="
        + text
    )
    response = session.get(
        url, headers=session.headers, cookies=session.cookies, proxies=session.proxies
    )
    return response
