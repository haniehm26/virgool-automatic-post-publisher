from apis import VirgoolAPI, send_telegram_message
from editor import edit_virgool_post_body, generate_telegram_channel_text
from tag_generator import extract_tags, prepare_body


def run_script(
    virgool_username: str,
    virgool_password: str,
    draft_description: str,
    telegram_bot_token: str,
    telegram_chat_id: str,
    telegram_proxy: dict,
    telegram_tags: list,
):
    virgool_api = VirgoolAPI()

    # LOGIN
    response = virgool_api.login(virgool_username, virgool_password)
    print("LOGIN:", response.status_code)

    # GET DRAFTS
    response = virgool_api.get_drafts()
    print("GET DRAFTS:", response.status_code)
    oldest_draft_hash = response.json()["data"][-1]["hash"]
    print("OLDEST DRAFT POST HASH:", oldest_draft_hash)

    # GET PUBLISHMENTS
    response = virgool_api.get_publishments()
    print("GET PUBLISHMENTS:", response.status_code)
    newest_published_hash = response.json()["data"][0]["hash"]
    print("NEWEST PUBLISHED POST HASH:", newest_published_hash)
    newest_published_short_url = response.json()["data"][0]["short_url"]
    print("NEWEST PUBLISHED POST SHORT URL:", newest_published_short_url)

    # GET OLDEST DRAFT POST
    response = virgool_api.fetch_draft_editor_by_hash(oldest_draft_hash)
    print("FETCH OLDEST DRAFT POST:", response.status_code)
    draft_post = response.json()["post"]
    draft_post_title = draft_post["title"]

    # EXTRACT TAGS FOR OLDEST DRAFT POST
    tags = extract_tags(prepare_body(draft_post["body"]))
    print("EXTRACTED TAGS FOR OLDEST DRAFT POST:", tags)

    # EDIT OLDEST DRAFT POST
    edited_body = edit_virgool_post_body(draft_post["body"], newest_published_short_url, True)
    response, edited_post = virgool_api.edit_post(
        pyload=draft_post, description=draft_description, body=edited_body
    )
    print("EDIT OLDEST DRAFT POST:", response.status_code)

    # PUBLISH OLDEST DRAFT POST
    # CAUTION: IF YOU RUN THE FOLLOWING CODES,
    # THE OLDEST DRAFT POST WILL BE PUBLISHED IN VIRGOOL
    response = virgool_api.publish_post(edited_post)
    print("PUBLISH OLDEST DRAFT POST:", response.status_code)

    # TAKE NEW PUBLISHED (OLDEST DRAFT) POST SHORT URL
    response = virgool_api.fetch_post_by_hash(oldest_draft_hash)
    print("FETCH NEW PUBLISHED (OLDEST DRAFT) POST SHORT URL:", response.status_code)
    new_published_short_url = response.json()["post"]["short_url"]
    print("NEW PUBLISHED (OLDEST DRAFT) POST SHORT URL:", new_published_short_url)

    # TAKE POST OF PREVIOUS SESSION
    response = virgool_api.fetch_published_editor_by_hash(newest_published_hash)
    print("FETCH PREVIOUS SESSION POST:", response.status_code)
    post = response.json()["post"]

    # EDIT BODY OF PREVIOUS SESSION POST AND ADD NEW PUBLISHED POST SHORT URL
    edited_body = edit_virgool_post_body(post["body"], new_published_short_url, False)
    response, edited_post = virgool_api.edit_post(pyload=post, body=edited_body)
    print("EDIT PREVIOUS SESSION POST:", response.status_code)

    # RE-PUBLISH PREVIOUS SESSION POST
    # CAUTION: IF YOU RUN THE FOLLOWING CODES,
    # THE OLDEST DRAFT WILL BE PUBLISHED IN VIRGOOL
    response = virgool_api.publish_post(edited_post)
    print("RE-PUBLISH PREVIOUS SESSION POST:", response.status_code)

    # GENERATE TELEGRAM MESSAGE TEXT
    session = draft_post_title.split("-")[1]
    subject = draft_post_title.split("-")[2]
    text = generate_telegram_channel_text(session, subject, new_published_short_url, telegram_tags)

    # TAKE NEW PUBLISHED POST SHORT URL AND SEND IT TO TELEGRAM CHANNEL
    response = send_telegram_message(telegram_proxy, telegram_bot_token, telegram_chat_id, text)
    print("SEND MESSAGE TO TELEGRAM CHANNEL:", response.status_code)
