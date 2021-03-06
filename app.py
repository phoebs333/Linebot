from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, StickerSendMessage
)

app = Flask(__name__)

line_bot_api = LineBotApi('21qStguiwvWS4PepkOwGHVLFfWPheLdhyzlgKXkoIAH1g1s5kqPGBJu++SMXY6PJJqHgbLjpyktqyIa9Af2Y/5CSdcT6P8dXTk+DnTVJXtmcsClfT4brjdW3u4XciWXnxtwSsxPpJLxrr12dEq2xwgdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('51a335c816c068d4135c7fa5b4404156')


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
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    msg = event.message.text
    r = 'What do you mean?'
    
    if 'Give me a sticker' in msg:
        sticker_message = StickerSendMessage(
            package_id='1',
            sticker_id='2'
        )

        line_bot_api.reply_message(
            event.reply_token,
            sticker_message)

        return

    if msg in ['hi', 'Hi']:
        r = 'Hi'
    elif msg == 'Did you eat?':
        r = 'Not yet.'
    elif msg == 'Who are you?':
        r = 'I am Chatbot.'
    elif 'reservation' in msg:
        r = 'Do you want to make a reservation?'
    

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=r))


if __name__ == "__main__":
    app.run()
