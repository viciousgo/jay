import json

import aiohttp
from .helpers import signature, device_id
from time import time as timestamp


class Client:
    def __init__(self, session: aiohttp.ClientSession, simple_account: dict = None):
        self.session = session
        self.logged = False
        self.sid = None
        self.community_id = None
        self.v1_api = "https://service.narvii.com/api/v1"
        self.uid = None
        self.email, self.password, self.device_id = simple_account["email"], simple_account["password"], \
                                                    simple_account["device_id"]
                                                    
    def v1_headers(self, data=None, content_type=None):
        headers = {
            "NDCDEVICEID": self.device_id,
            "Accept-Language": "ru-RU",
            "Content-Type": "application/json; charset=utf-8",
            "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 7.1.2; SM-G965N Build/star2ltexx-user 7.1.; com.narvii.amino.master/3.4.33602)",
            "Host": "service.narvii.com",
            "Accept-Encoding": "gzip",
            "Connection": "Upgrade"
        }

        if data is not None:
            headers["Content-Length"] = str(len(data))
            headers["NDC-MSG-SIG"] = signature(data)
        if self.sid is not None:
            headers["NDCAUTH"] = f"sid={self.sid}"
        if content_type is not None:
            headers["Content-Type"] = content_type
        return headers

    def web_headers(self, referer):
        headers = {
            "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/73.0.3683.86 Chrome/73.0.3683.86 Safari/537.36",
            "content-type": "application/json",
            "x-requested-with": "xmlhttprequest",
            "cookie": f"sid={self.sid}",
            "referer": referer}
        return headers

    async def login(self):
        data = json.dumps({
            "email": self.email,
            "v": 2,
            "secret": f"0 {self.password}",
            "deviceID": self.device_id,
            "clientType": 100,
            "action": "normal",
            "timestamp": int(timestamp() * 1000)
        })
        response = await (await self.session.post(f"{self.v1_api}/g/s/auth/login",
                                                  headers=self.v1_headers(data=data),
                                                  data=data)).text()
        response_json = json.loads(response)
        self.sid = response_json["sid"]
        self.logged = True
        return response_json
        
    async def login_sid(self, SID: str):
        """
        Login into an account with an SID

        **Parameters**
            - **SID** : SID of the account
        """
        uId = helpers.sid_to_uid(SID)
        self.authenticated = True
        self.sid = SID
        self.userId = uId
        self.account: objects.UserProfile = await self.get_user_info(uId)
        self.profile: objects.UserProfile = await self.get_user_info(uId)
        headers.sid = self.sid
        await self.startup()
    
    async def link_resolution(self, link):
        response = await self.session.get(f"{self.v1_api}/g/s/link-resolution?q={link}",
                                                  headers=self.v1_headers())
        return await response.json()

    async def send_message(self, chat_id, message, message_type, community_id):
        data = {
            "ndcId": f"x{community_id}",
            "threadId": chat_id,
            "message": {
                "content": message,
                "mediaType": 0,
                "type": message_type,
                "sendFailed": False,
                "clientRefId": 0}}

        data = json.dumps(data)
        r = await self.session.post(f"https://aminoapps.com/api/add-chat-message",
                                 headers=self.web_headers(
                                     referer=f"https://aminoapps.com/partial/main-chat-window?ndcId={community_id}"),
                                 data=data)
        print(await r.text())

    async def leave_chat(self, chat_id, community_id):
        data = {"ndcId": f"x{community_id}",
                "threadId": chat_id}
        data = json.dumps(data)
        await self.session.post(f"https://aminoapps.com/api/leave-thread",
                                 headers=self.web_headers(
                                     referer=f"https://aminoapps.com/partial/main-chat-window?ndcId={community_id}"),
                                 data=data)

    async def join_chat(self, chat_id, community_id):
        data = {"ndcId": f"x{community_id}",
                "threadId": chat_id}
        data = json.dumps(data)
        await self.session.post(f"https://aminoapps.com/api/join-thread",
                                headers=self.web_headers(
                                    referer=f"https://aminoapps.com/partial/main-chat-window?ndcId={community_id}"),
                                data=data)


    async def vicious_cohost(self, chat_id, user_id,community_id):
        data = {"ndcId": f"x{community_id}",
                "threadId": chat_id}
        data = json.dumps(data)
        r = await self.session.delete(f"https://aminoapps.com/api/co-host",
                                headers=self.web_headers(
                                    referer=f"https://aminoapps.com/partial/main-user-window?ndcId={community_id}"),
                                data=data)
        print(await r.text())