import requests
import random
import time
import hmac
import hashlib
import binascii
from urllib.parse import urlencode

class Wenzhi:
    def __init__(self, param, method="POST"):
        self.param = param
        '''
           in_param_list:
             region: &eg: 'gz'
             secretId:
             secretKey:
             action: &eg: 'TextSentiment'
             action-param: ""
        '''
        self.domain = "https://wenzhi.api.qcloud.com/v2/index.php"
        self.method = method
    def _build_param(self):
        def __build_signature(params):
            srcStr = self.method + self.domain[8:] + '?' + "&".join(k.replace("_",".") + "=" + str(params[k]) for k in sorted(params.keys()))
            hashed = hmac.new(self.param['SecretKey'].encode('utf-8'), srcStr.encode('utf-8'), hashlib.sha1)
            return binascii.b2a_base64(hashed.digest())[:-1].decode('utf-8')
        timestamp = int(time.time())
        nonce = random.randint(0, 999999)
        build_param = {
            "Action": self.param['Action'],
            "Nonce": nonce,
            "Region": self.param['Region'],
            "SecretId": self.param['SecretId'],
            "Timestamp": timestamp,
        }
        for param_key in self.param['action-param']:
            build_param[param_key] = self.param['action-param'][param_key]
        build_param["Signature"] = __build_signature(build_param)
        return build_param
    def send(self, action, action_param):
        self.param['Action'] = action
        self.param['action-param'] = action_param
        req = requests.post(self.domain, data=self._build_param(), timeout=10, verify=False)
        return req

if __name__ == "__main__":
    action_param = {
        'content': u'Dior新款，秋冬新款娃娃款甜美圆领配毛领毛呢大衣外套、码数：SM、P330',
    }
    param = {
        'Region': 'sz',
        'SecretId': 'AKID1CC0byI4nJbfW95jgPvEKAk36sOdjLo0',
        'SecretKey': '6xXrvkNmxvfBTXN0PaXGl25vXv51jDUa',
    }
    w = Wenzhi(param)
    res = w.send('TextSentiment', action_param)
    print (res.json())
