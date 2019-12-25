# -*- coding: utf-8 -*-
import scrapy
import re
import requests
import json
from recipe.items import RecipeItem
from shujku import Session,Recipe,Making
import re


def get_keyword():
    key_words = []
    with open('keywords.txt', 'r', encoding='utf8') as f:
        while 1:
            key_word = f.readline()
            if not key_word:
                break
            key_words.append(key_word.strip())
    return key_words


class MakeRecipeSpider(scrapy.Spider):
    name = 'make_recipe'
    allowed_domains = ['baike.baidu.com']
    key_words = get_keyword()
    # start_urls = ['http://baike.baidu.com/item/水煮鱼']
    r1 = Session.query(Making).filter_by().all()

    list_all = [j.dish_name for j in r1]
    print('li',list_all)
    print('ke',key_words)
    for i in key_words:
        if i in list_all:
            key_words.remove(i)
    print('ke',key_words)
    start_urls = [f'http://baike.baidu.com/item/{i.strip()}' for i in key_words]
    def parse(self, response):
        name = response.url.split('/')[-1]
        if response.url.split('/')[-1].isdigit():
            name = response.url.split('/')[-2]
        item = RecipeItem()
        # method =
        datas = re.findall('"secondKind":"3","secondId":(.*?),"mid":""', response.text)
        flags = ['菜品制作', '做法一', '做法', '制作过程', '制作方法', '做法', '烹饪方法', '制作工艺']
        methods = []
        for flag in range(8):
            print(name)
            pattern1 = re.compile('</span>{}</h2>.*?编辑(.*?)<div class="album-list">'.format(flags[flag]),re.S)
            ''''< h2 class ="title-text" > < span class ="title-prefix" > 红烧肉 < / span > 做法 < / h2 >
            < a class ="edit-icon j-edit-link" data-edit-dl="1" href="javascript:;" > < em class ="cmn-icon wiki-lemma-icons wiki-lemma-icons_edit-lemma" > < / em > 编辑 < / a >
            < / div >'''
            methods = pattern1.findall(response.text)
            if methods:
                break

        # pattern = re.compile(r'</span>做法一</h2>.*?</em>编辑</a>(.*?)<h2',re.S)
        # pattern = re.compile(r'</span>做法</h2>.*?</em>编辑</a>(.*?)<h2',re.S)
        # pattern = re.compile(r'</span>制作过程</h2>.*?</em>编辑</a>(.*?)<h2',re.S)
        # pattern = re.compile(r'</span>做法</h2>.*?</em>编辑</a>(.*?)<h2',re.S)
        # pattern = re.compile(r'</span>烹饪方法</h2>.*?</em>编辑</a>(.*?)<h2',re.S)
        # pattern = re.compile(r'</span>制作工艺</h2>.*?</em>编辑</a>(.*?)<h2',re.S)

        method = methods[0]
        pre = re.compile('>(.*?)<')
        text1 = '\n'.join(pre.findall(method)).strip()
        if not methods:
            text1 = '没有此做法'
        pattern2 = re.compile(r'data-src="(.*?)"')
        pics = pattern2.findall(response.text)

        # print(method)
        # print('_____',text)
        # print(datas)
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Cookie': '''BIDUPSID=43B9F2F65CAF41BADFD2656732682F1F; PSTM=1575013007; BAIDUID=43B9F2F65CAF41BA9F402338117B188B:FG=1; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; pgv_pvi=4406757376; BK_SEARCHLOG=%7B%22key%22%3A%5B%22%E8%BE%A3%E7%99%BD%E8%8F%9C%22%2C%22%E5%93%94%E5%93%A9%E5%93%94%E5%93%A9%22%2C%22%E7%82%92%E8%BE%A3%E7%99%BD%E8%8F%9C%22%2C%22%E9%A9%B1%E5%8A%A8%E7%B2%BE%E7%81%B5%22%5D%7D; delPer=0; PSINO=1; pgv_si=s7153703936; Hm_lvt_55b574651fcae74b0a9f1cf9c8d7c93a=1576738142,1576739659,1576740148,1576740223; Hm_lpvt_55b574651fcae74b0a9f1cf9c8d7c93a=1576740223; H_PS_PSSID=1461_21110_30211_18560_30284_22157''',
            'Host': 'baike.baidu.com',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'}
        item['making'] = text1
        item['pic'] = pics
        for data in datas:
            res = requests.get('https://baike.baidu.com/api/wikisecond/playurl?secondId={}'.format(data),
                               allow_redirects=False, headers=headers)
            # print(res.text)
            data1 = json.loads(res.text)
            if data1:
                video_url = data1['list']['hlsUrl']
            else:
                video_url = None
            # print(video_url)
            item['vid'] = data
            item['vurl'] = video_url
            item['name'] = name
            # video = requests.get(video_url)
            # with open('111.mp4','wb') as f:
            #     f.write(video.content)
            yield item