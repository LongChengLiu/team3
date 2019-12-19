# -*- coding: utf-8 -*-
import scrapy
import re
import requests


class MakeRecipeSpider(scrapy.Spider):
    name = 'make_recipe'
    allowed_domains = ['baike.baidu.com']
    start_urls = ['http://baike.baidu.com/item/芹菜炒肉']

    def parse(self, response):
        data = re.findall('"secondKind":"3","secondId":(.*?),"mid":""', response.text)
        print(data)
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
        video = requests.get('https://baike.baidu.com/api/wikisecond/playurl?secondId=20538072',allow_redirects=False,headers=headers)
        print(video.text)
        with open('111.txt','w') as f:
            f.write(video.text)
