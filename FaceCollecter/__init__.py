#!/usr/bin/env python
# -*- coding: utf-8 -*-

import url_fetch
import time

if __name__ == '__main__':
    start = time.time()
    membars = ["古川未鈴", "相沢梨紗", "夢眠ねむ", "成瀬瑛美", "最上もが", "藤咲彩音"]

    for value in membars:
        print('\n ---------- {0} fetch 開始 ----------'.format(value))
        fetcher = url_fetch.UrlFetch(value, 350)
        fetcher.fetch()
        print('\n ---------- {0} fetch 終了 ----------'.format(value))
    elapsed_time = time.time() - start
    print ("elapsed_time:{0}".format(elapsed_time)) + "[sec]"
