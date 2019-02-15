from bearychat import RTMClient
from bearychat import openapi
from wenzhi import Wenzhi
import re
import requests

class Process:
    def __init__(self, hubot_token):
        self.client = RTMClient(hubot_token, 'https://api.bearychat.com/v1')
        self.openapi_client = openapi.Client(hubot_token)
        self.wenzhi = Wenzhi({
          'Region': 'sz',
          'SecretId': 'AKID1CC0byI4nJbfW95jgPvEKAk36sOdjLo0',
          'SecretKey': '6xXrvkNmxvfBTXN0PaXGl25vXv51jDUa',    
        })

    def _get(self, *args, **argv):
        return self.client.get(*args, **argv).resp.json()

    def _post(self, *args, **argv):
        return self.client.post(*args, **argv).resp.json()

    def reaction_choicer(self, message):
        print(message['text'])
        action_param = {
            'content': message['text'],
            'type': 4
        }
        res = self.wenzhi.send('TextSentiment', action_param)
        p = res.json()['positive']
        if p > 0.8:
            return ':+1:'
        elif p < 0.2:
            return ':hug:'
        else:
            return ':doge:'


    def add_reaction_to_message(self, message):
        reaction = self.reaction_choicer(message)
        vchannel_id = message['vchannel_id']
        key = message['key']
        self.openapi_client.reaction.create(json={
          'vchannel_id': vchannel_id,
          'key': key,
          'reaction': reaction
        })
