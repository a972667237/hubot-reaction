import time

from bearychat import RTMClient

from rtm_loop import RTMLoop

from settings import hubot_token

from processor import Process

client = RTMClient(hubot_token, "https://rtm.bearychat.com")

resp = client.start()

user = resp['user']
ws_host = resp['ws_host']

process = Process(hubot_token)
loop = RTMLoop(ws_host)
loop.start()
time.sleep(2)

while True:
    error = loop.get_error()

    if error:
        print(error)
        continue

    message = loop.get_message(True, 5)

    if not message or not message.is_chat_message():
        continue
    try:
        print("rtm loop received {0} from {1}".format(message['text'], message['uid']))
        if message.is_from(user):
            # continue for not reply message form itself
            continue
        if message.is_p2p():
            # do something with settings
            continue
        # do something with reaction or not
        process.add_reaction_to_message(message)

    except:
        print('something error')
        continue
