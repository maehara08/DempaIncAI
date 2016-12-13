#!/usr/bin/env python
# -*- coding: utf-8 -*-

### 画像のURL一覧を取得するPy


import urllib
import requests
import json
import io
import imghdr
import uuid
import os
# from urlparse import urlparse


class UrlFetch:
    # Bing Search APIの仕様で決まっている1リクエストあたりの画像取得最大枚数
    ONE_SEARCH_LIMIT = 50
    # Bing Search API のURL
    ROOT_URL = 'https://api.datamarket.azure.com/Bing/Search/v1/Image?'
    # APIキー
    API_KEY = 'enZYoiUmzkA56Alz0QOcXYPbrLd1G0Ft3cdLrh7Cz6o'
    # 画像のダウンロードのタイムアウト(秒)
    TIMEOUT = 10
    # ダウンロードした画像を格納するディレクトリ名
    SAVE_DIR = 'images'

    def __init__(self, memberName, imageNumber):
        self.memberName = memberName
        self.SAVE_DIR = self.SAVE_DIR+"_"+memberName
        self.imageNumber = imageNumber
        if (imageNumber%self.ONE_SEARCH_LIMIT!=0):
            raise Exception('number must be divisible by {0}!!'.format(self.ONE_SEARCH_LIMIT))

    def fetch(self):
        for i in range(self.imageNumber//self.ONE_SEARCH_LIMIT):
            offset=i*self.ONE_SEARCH_LIMIT

            params = {
                'Query': "'{}'".format(self.memberName),
                'Market': "'{}'".format('ja-JP'),
                '$format': 'json',
                '$top': '{0:d}'.format(self.ONE_SEARCH_LIMIT),
                '$skip': '{0:d}'.format(offset),
            }

            url = self.ROOT_URL + urllib.urlencode(params)
            print(url)
            response_json = requests.get(url, auth=('', self.API_KEY))
            response = json.loads(response_json.text)

            for result in response['d']['results']:
                image_url = result['MediaUrl']
                try:
                    response_image = requests.get(image_url, timeout=self.TIMEOUT)
                    image_binary = response_image.content
                except:
                    print("erorr")
                    continue

                with io.BytesIO(image_binary) as fh:
                    image_type = imghdr.what(fh)

                if image_type == 'jpeg':
                    extension = '.jpg'
                elif image_type == 'png':
                    extension = '.png'
                else:
                    continue

                filename = str(uuid.uuid4()) + extension

                if not os.path.isdir(self.SAVE_DIR):
                    os.mkdir(self.SAVE_DIR)
                with open(os.path.join(self.SAVE_DIR, filename), 'wb') as f:
                    f.write(image_binary)
