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
