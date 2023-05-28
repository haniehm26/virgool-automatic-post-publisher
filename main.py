import os

from dotenv import load_dotenv
from script import run_script


load_dotenv()
virgool_username = os.getenv("USERNAME")
virgool_password = os.getenv("PASSWORD")
telegram_bot_token = os.getenv("BOT_TOKEN")
telegram_chat_id = os.getenv("CHAT_ID")
proxy = os.getenv("PROXY")

draft_description = (
    "مطالب این پست از روی دوره آمار و احتمال دکتر علی شریفی زارچی از"
    + "دانشگاه صنعتی شریف نوشته شده.  تمامی جلسات این دوره در مکتب‌خونه موجوده."
)

telegram_tags = ["علی_شریفی_زارچی", "آمار_و_احتمال", "مکتبخونه"]

telegram_proxy = {"http": proxy, "https": proxy}

if __name__ == "__main__":
    run_script(
        virgool_username,
        virgool_password,
        draft_description,
        telegram_bot_token,
        telegram_chat_id,
        telegram_proxy,
        telegram_tags,
    )
