from django.shortcuts import render
from django.http import HttpResponse
import json
import base64
import json
from Crypto.Cipher import AES
import requests

class WXBizDataCrypt:
    def __init__(self, appId, sessionKey):
        self.appId = appId
        self.sessionKey = sessionKey

    def decrypt(self, encryptedData, iv):
        # base64 decode
        sessionKey = base64.b64decode(self.sessionKey)
        encryptedData = base64.b64decode(encryptedData)
        iv = base64.b64decode(iv)

        cipher = AES.new(sessionKey, AES.MODE_CBC, iv)

        decrypted = json.loads(self._unpad(cipher.decrypt(encryptedData)))

        if decrypted['watermark']['appid'] != self.appId:
            raise Exception('Invalid Buffer')

        return decrypted

    def _unpad(self, s):
        return s[:-ord(s[len(s)-1:])]

def get_session_key(APPID,SECRET,JSCODE):
    url = 'https://api.weixin.qq.com/sns/jscode2session?appid={appid}&secret={secret}&js_code={code}&grant_type=authorization_code'.format(appid=APPID,secret=SECRET,code=JSCODE)
    res = requests.get(url)
    #openid = res.json().get('openid')
    session_key = res.json().get('session_key')
    return session_key

def index(request):
    if(request.method == 'POST'):
        JSCODE = request.POST.get("code")
        encryptedData = request.POST.get("encryptedData")
        iv = request.POST.get("iv")
        APPID = "wx2bc1e3ba62de3c82"
        SECRET = "6049371aed80649d53635c0cf94e9699"
        session_key=get_session_key(APPID,SECRET,JSCODE)
        pc = WXBizDataCrypt(APPID, session_key)
        data = pc.decrypt(encryptedData, iv) #data中是解密的用户信息
        data=json.dumps(data)
        print(data)
        return HttpResponse(data)