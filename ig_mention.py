import os
try:
    from telegram.ext import Updater,CommandHandler,MessageHandler,Filters
except ImportError:
    os.system('pip install python-telegram-bot --upgrade')
    from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
try:
    from requests import get
except ImportError:
    os.system('pip install requests')
    from requests import get
try:
    from uuid import uuid4
except ImportError:
    os.system('pip install uuid')
    from uuid import uuid4
try:
    from json import loads
except ImportError:
    os.system('pip install json')
    from json import loads
def getid(session,user):
    headers = {
        "Host": "i.instagram.com",
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "en-US",
        "User-Agent": "Instagram 10.23.0 (iPhone11,2; iOS 12_1_4; ar_SA@calendar=gregorian; ar-SA; scale=3.00; gamut=wide; 1125x2001) AppleWebKit/420+",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Cookie": f"sessionid={session}"

    }
    id = get(f"https://i.instagram.com/api/v1/users/{user}/usernameinfo/", headers=headers).json()
    return id["user"]["pk"]
def show(session,id):
    Headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:102.0) Gecko/20100101 Firefox/102.0",
        "Accept": "*/*",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br",
        "X-CSRFToken": "hjCdOJzq7llBK5SLOASWmLOl6brvTOeK",
        "X-IG-App-ID": "936619743392459",
        "X-ASBD-ID": "198387",
        "X-IG-WWW-Claim": "hmac.AR3bjFtFQokEUHdyITbgTbt-6_X7NNIdTmaQC-ZkDK__1V_A",
        "Origin": "https://www.instagram.com",
        "Alt-Used": "i.instagram.com",
        "Connection": "keep-alive",
        "Referer": "https://www.instagram.com/",
        "Cookie": f"sessionid={session}",
        "Sec-Fetch-Dest": "empty",
    }
    req = get(f"https://i.instagram.com/api/v1/feed/user/{id}/story/", headers=Headers)
    response = loads(req.text)
    resp = response['reel']['items'][0]['story_bloks_stickers']
    return resp


def start(update, context):
    update.message.reply_text("Enter Link Story : \n\nor if you want to use your session account (for private accounts) enter link|session")
def work(update, context):
    stopped = False
    link = update.message.text
    if '|' in link:
        splt = link.split('|')
        link = splt[0]
        session = splt[1]
    else:
        session = 'your session'
    user = link.split('/')[4]
    #user = '7.9x.moved'
    id = getid(session,user)
    try:
        resp = show(session,id)
    except:
        update.message.reply_text("Error with tool (Try to enter sessionid)")
        stopped = True

    i = 0
    while stopped == False:
        try:
            update.message.reply_text(f"@{resp[i]['bloks_sticker']['sticker_data']['ig_mention']['username']}")
            i+=1
        except:
            break
    if i == 0:
        update.message.reply_text("No Usernames Mention :(")
    else:
        update.message.reply_text("Done . Follow Me Here @zyll :)")

updater = Updater("Token Bot",use_context=True)
updater.dispatcher.add_handler(CommandHandler("start",start))
updater.dispatcher.add_handler(MessageHandler(Filters.text,work))
updater.start_polling()
