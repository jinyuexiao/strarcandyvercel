import os
os.system("pip install deep-translator")
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import os
from lottery import draw_lottery
from tarot import draw_tarot

app = Flask(__name__)

# 設定 LINE Bot API Token 和 Channel Secret
LINE_ACCESS_TOKEN = "XX++hVAb6YireyWjisyAabq4VMAqKHdWLBs8jmtnG3EuORVTgR24Lglz0liftfEwXKb3jiyA+SaJ4PzmbvFxKhT92pOAYufInnQlnztoGf8Lo/V6HEAUCMwRQrDhXPQrlH10bBuoy9ruAgLiN6o4XwdB04t89/1O/w1cDnyilFU="
LINE_CHANNEL_SECRET = "f1106eba87a65a45f359549f98c10db4"

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
        reply_text =  f"好的，您抽到：{draw_lottery()}"
    elif user_message in ["星星糖我要占卜", "塔羅牌占卜"]:
        reply_text = draw_tarot()
    elif user_message in ["謝謝星星糖", "謝謝"]:
        reply_text = "不客氣！天天順心！"
    else:
        reply_text = " 如果您想要星星糖幫您算算的話，請輸入：星星糖我要占卜 或 星星糖我要抽籤 "

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=reply_text)
    )

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
