from bs4 import BeautifulSoup


def edit_virgool_post_body(draft_body: str, short_url: str, is_draft: bool):
    soup = BeautifulSoup(draft_body, "html.parser")
    index = -2 if is_draft else -1
    paragraph_text = soup.find_all("p", class_="md-block-unstyled")[index].get_text()
    link = f'<a class="md-inline-link" href="{short_url}" target="_blank" rel="noopener nofollow">'
    start_paragraph = '<p class="md-block-unstyled">'
    paragraph_tag = f"{start_paragraph}{paragraph_text}{'</p>'}"
    paragraph_text = paragraph_text if is_draft else paragraph_text.split("-")[0]
    edited_paragraph = f"{start_paragraph}{link}{paragraph_text}{'</a></p>'}"
    edited_body = draft_body.replace(paragraph_tag, edited_paragraph)
    return edited_body


def generate_telegram_channel_text(session: str, subject: str, short_url: str, tags: list):
    hashtag = "%23"
    text = session + "دوره آمار و احتمال با موضوع"
    text += subject + " در ویرگول منتشر شد:\n"
    text += short_url + "\n\n"
    for tag in tags:
        text += hashtag + tag + "\n"
    text += "\n\n"
    text += "📚 @honio_notes"
    return text
