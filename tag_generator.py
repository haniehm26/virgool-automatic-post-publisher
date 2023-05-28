from bs4 import BeautifulSoup


def prepare_body(body):
    soup = BeautifulSoup(body, "html.parser")
    paragraphs = soup.find_all("p", class_="md-block-unstyled")
    text = ""
    for p in paragraphs:
        text += p.get_text() + "\n"
    return text
