import os
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
from lottery import draw_lottery
from tarot import draw_tarot

app = Flask(__name__)

LINE_ACCESS_TOKEN = os.environ.get("LINE_ACCESS_TOKEN")
LINE_CHANNEL_SECRET = os.environ.get("LINE_CHANNEL_SECRET")

line_bot_api = LineBotApi(LINE_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_message = event.message.text.strip()

    if user_message == "星星糖我要抽籤":
        reply_text = f"好的，您抽到：{draw_lottery()}"
    elif user_message in ["星星糖我要占卜", "塔羅牌占卜"]:
        reply_text = draw_tarot()
    elif user_message in ["謝謝星星糖", "謝謝"]:
        reply_text = "不客氣！天天順心！"
    else:
        reply_text = "如果您想要星星糖幫您算算的話，請輸入：星星糖我要占卜 或 星星糖我要抽籤"

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=reply_text)
    )
