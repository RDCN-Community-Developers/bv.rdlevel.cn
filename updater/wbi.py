import time
from requests import Session
from urllib.parse import urlencode
from hashlib import md5

keyMapping = [
    46, 47, 18, 2, 53, 8, 23, 32, 15, 50, 10, 31, 58, 3, 45, 35, 27, 43, 5, 49,
    33, 9, 42, 19, 29, 28, 14, 39, 12, 38, 41, 13, 37, 48, 7, 16, 24, 55, 40,
    61, 26, 17, 0, 1, 60, 51, 30, 4, 22, 25, 54, 21, 56, 59, 6, 63, 57, 62, 11,
    36, 20, 34, 44, 52
]


class Wbi:
    def __init__(self, session: Session) -> None:
        self.session = session
        self.img_key: str = ''
        self.sub_key: str = ''
        self.mixin_key: str = ''

    def get_wbi_keys(self) -> tuple[str, str]:
        if self.img_key != '' and self.sub_key != '':
            return self.img_key, self.sub_key

        res = self.session.get('https://api.bilibili.com/x/web-interface/nav')
        res.raise_for_status()

        data = res.json()['data']['wbi_img']
        img_url: str = data['img_url']
        sub_url: str = data['sub_url']
        self.img_key = img_url.rsplit('/', 1)[-1].split('.')[0]
        self.sub_key = sub_url.rsplit('/', 1)[-1].split('.')[0]

        return self.img_key, self.sub_key
    
    def get_mixin_key(self) -> str:
        if self.mixin_key != '':
            return self.mixin_key

        if self.img_key == '' or self.sub_key == '':
            self.get_wbi_keys()

        combined = self.img_key + self.sub_key
        self.mixin_key = ''.join(combined[i] for i in keyMapping)[:32]

        return self.mixin_key
    
    def encode_query(self, query: dict) -> dict:
        if self.mixin_key == '':
            self.get_mixin_key()

        query['wts'] = round(time.time())
        query = dict(sorted(query.items()))
        query['w_rid'] = md5((urlencode(query) + self.mixin_key).encode('utf-8')).hexdigest()

        return query

        
    