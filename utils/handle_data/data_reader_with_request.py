import json
import logging
import os
import random
import sys
import traceback
from time import sleep

import pandas as pd
import requests

parent_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

sys.path.append(parent_path)

# 引入django配置文件
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dj_scientific_research_influence.settings")
# 启动django
import django

django.setup()

from science.models import Paper, Scholar, Keywords

RESOURCE_NAME = 'RESOURCE'  # 资源文件夹
RESOURCE_SUCCESS_NAME = 'SUCCESS'  # 下级成功文件夹

SUCCESS_PATH = os.path.join(RESOURCE_NAME, RESOURCE_SUCCESS_NAME)

SEP = 'aaa'  # 分隔符


class Scanner:
    def __init__(self):
        self.li_error_url = []

        # 创建资源文件夹
        if not os.path.exists(RESOURCE_NAME):
            os.mkdir(RESOURCE_NAME)

        if not os.path.exists(SUCCESS_PATH):
            os.mkdir(SUCCESS_PATH)

    def run(self):
        for file_name in os.listdir(RESOURCE_NAME):
            if file_name.endswith('.csv'):  # 找到 csv文件
                # 文件路径
                file_path = os.path.join(RESOURCE_NAME, file_name)

                # 处理单个 csv文件
                self.handle_file(csv_file_path=file_path)

    def handle_file(self, csv_file_path):
        """处理 csv文件"""
        df = pd.read_csv(csv_file_path, encoding='gbk')

        for index, line in df[20:500].iterrows():
            # 拿到url，发起请求

            url = line['url']
            title = str(line['title']).strip()

            print(index)
            # print('title:', title)
            print('     url:', url)

            # 判断数据库是否存在，
            #       存则忽略，
            #       不存在则发起请求，获取结果，并添加数据库
            if Paper.objects.filter(title=title).first():
                print('     ———————— 存在，忽略 ————————')
                continue

            try:
                # 发起 url 请求
                resp = requests.get(url)
                jo = resp.json()
                json_str = json.dumps(jo, ensure_ascii=False)  # 保存多一份完整的原始json字符串，方便恢复数据

                # json提取内容
                contents = jo['contents'][0]
                li_author = jo['author']

                sno = contents['sno']
                title = contents['lypm']

                title_en = contents['blpm']
                keywords = [
                    key.strip(SEP).strip().strip('”').strip('“').strip()
                    for key in contents['byc'].split(';')
                    if key.strip(SEP).strip().strip('”').strip('“').strip()
                ]
                project = contents['xmlb']  # 项目
                periodical = contents['qkmc']  # 期刊名称
                authors = [
                    {
                        'name': author_item['zzmc'],
                        'organization': author_item['jgmc'],  # 机构
                        'json_str': json.dumps(author_item, ensure_ascii=False)  # 保存多一份完整的原始json字符串，方便恢复数据
                    }
                    for author_item in li_author
                ]

                print('         sno:', sno)
                print('         title:', title)
                print('         title_en:', title_en)
                print('         keywords:', keywords)
                print('         project:', project)
                print('         periodical:', periodical)
                print('         authors:', authors)
                print('         json_str:', json_str)

                # 插入一条记录
                # self.cursor.execute('insert into paper')
                db_paper = Paper.objects.create(
                    title=title,
                    title_en=title_en,
                    project=project,
                    periodical=periodical,
                    sno=sno,
                    json_str=json_str,
                    url=url
                )

                # 绑定 作者
                for author_di in authors:
                    author_name = author_di['name']
                    author_organization = author_di['organization']

                    # 查询数据库
                    db_scholar = Scholar.objects.filter(
                        name=author_name,
                        organization=author_organization
                    ).first()
                    if not db_scholar:  # 不存在，添加
                        db_scholar = Scholar.objects.create(
                            name=author_name,
                            organization=author_organization,
                            json_str=author_di['json_str'],
                        )
                    db_paper.li_authors.add(db_scholar)  # 关联到 paper

                # 绑定 关键词
                for key in keywords:
                    # 查看数据库
                    db_keyword = Keywords.objects.filter(value=key).first()
                    if not db_keyword:
                        db_keyword = Keywords.objects.create(
                            value=key
                        )
                    db_paper.li_keywords.add(db_keyword)  # 关联到 paper

            except Exception as e:
                logging.exception(e)
                traceback.print_exc()
                self.li_error_url.append(url)

            # 延迟
            sleep(random.random())

        if self.li_error_url:
            with open('error.txt', 'w') as f:
                for line in self.li_error_url:
                    f.write(line)


if __name__ == '__main__':
    s = Scanner()
    s.run()
