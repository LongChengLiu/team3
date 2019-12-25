# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import urllib
import requests
import os
import json
from shujku import Session,Recipe,Making

class RecipePipeline(object):
    def process_item(self, item, spider):
        pics = item['pic']
        vurl=item['vurl']
        vid=item['vid']
        making = item['making']
        Session.commit()
        name = urllib.parse.unquote((item['name']))
        video_list = []
        try:
            r3 = Making(dish_name=name, video_list=json.dumps(video_list))
            Session.add(r3)
            Session.commit()
        except:
            Session.rollback()
        r2 = Session.query(Making).filter_by(dish_name=name).first()
        r2.make_method = making
        Session.commit()
        os.makedirs('d:/爬取/{}'.format(name),exist_ok=True)
        video = requests.get(vurl)
        with open('d:/爬取/{}/{}.mp4'.format(name,vid),'wb') as f:
            f.write(video.content)
            r1 = Session.query(Making).filter_by(dish_name=name).first()
            vi_list = json.loads(r1.video_list)
            if vid not in vi_list:
                vi_list.append(vid)
            r1.video_list = json.dumps(vi_list)
            Session.commit()
        r4 = Session.query(Making).filter_by(dish_name=name).first()
        r4.image_count=len(pics)
        Session.commit()
        if os.path.exists('d:/爬取/{}/图片'.format(name)):
            return
        os.makedirs('d:/爬取/{}/图片'.format(name),exist_ok=True)
        a1 = -1
        for pic in pics:
            a1 += 1
            res = requests.get(pic).content
            with open('d:/爬取/{}/图片/{}.jpg'.format(name,a1),'wb') as f:
                f.write(res)
        if os.path.exists('d:/爬取/{}/making.txt'.format(name)):
            return
        with open('d:/爬取/{}/making.txt'.format(name,vid),'w') as f:
            f.write(making)





