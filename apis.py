from requests import Session


class VirgoolAPI:
    def __init__(self) -> None:
        self.session = Session()
        self.session.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/113.0",
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate, br",
        }

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
        url = "https://virgool.io/api/v1.4/posts/drafts"
        response = session.get(url, headers=session.headers, cookies=session.cookies)
        return response

    # OK
    def get_publishments(self):
        session = self.session
        url = "https://virgool.io/api/v1.4/posts/published"
        response = session.get(url, headers=session.headers, cookies=session.cookies)
        return response

    # OK
    def fetch_draft_editor_by_hash(self, post_hash: str):
        session = self.session
        url = "https://virgool.io/api/v1.4/editor/fetch/d/" + post_hash
        response = session.get(url, headers=session.headers, cookies=session.cookies)
        return response

    # OK
    def fetch_published_editor_by_hash(self, post_hash: str):
        session = self.session
        url = "https://virgool.io/api/v1.4/editor/fetch/p/" + post_hash
        response = session.get(url, headers=session.headers, cookies=session.cookies)
        return response

    # OK
    def fetch_post_by_hash(self, post_hash: str):
        session = self.session
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
        url = "https://virgool.io/api/v1.4/editor/draft"
        response = session.post(url, headers=session.headers, cookies=session.cookies, data=data)
        return response, data
