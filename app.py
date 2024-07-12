from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *

app = Flask(__name__)

# Channel Access Token
line_bot_api = LineBotApi('7sree2Y4LNYwqPW1lIKwPlXxK87OCpp+atJqCBeAfM2bDO9aTYWkvFlqS8wKre7hUeLGpThCaE+oPG+jNojleHD0dz8dcWpTELybYunbJwPJGmB5KG+FyrC7vNaB5rPnXwEdQ5zXndMukF2lPofJ7AdB04t89/1O/w1cDnyilFU=')
# Channel Secret
handler = WebhookHandler('4aad751cb9049ffd46c09dd6fa771c68')

# 監聽所有來自 /callback 的 Post Request
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

# 處理訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    if event.message.text == "情緒":
        reply_text = "穩定"
    else:
        reply_text = "你好!請輸入"情緒"來獲得回覆!"
    message = TextSendMessage(text=reply_text)
    line_bot_api.reply_message(event.reply_token, message)


import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
