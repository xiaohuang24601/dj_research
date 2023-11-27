import json
import re

import pandas as pd

SEP = 'aaa'  # 分隔符


class Scanner:

    def base_pick(self, patt_str, raw_content):
        patt = re.compile(patt_str, flags=re.I)
        tmp = patt.search(raw_content)

        try:
            res_value = tmp.groups()[0].strip()

            res_value = res_value.strip().strip(';').strip().strip(SEP).strip()
        except:
            res_value = ''

        return res_value

    def base_pick_array(self, patt_str, raw_content):
        return [
            item.strip().strip(';')
            for item in self.base_pick(patt_str, raw_content).split(SEP)
            if item.strip().strip(';')
        ]

    def run(self):
        df = pd.read_csv('最原始数据.csv', encoding='gbk')
        # print(df)

        for index, line in df[:5].iterrows():
            url = line['url']

            lyqk = line['lyqk']

            keywords = line['key words']

            content = line['contents']

            catation = line['catation']

            authors = self.base_pick_array(patt_str='authors:(.*?), authors_jg', raw_content=content)

            title = self.base_pick(patt_str='lypm:(.*?), lypmp', raw_content=content, )
            title_en = self.base_pick(patt_str='blpm:(.*?), authors', raw_content=content, )

            sno = self.base_pick(patt_str='sno: (.*?), lypm', raw_content=content)

            authors_jg = self.base_pick_array(patt_str='authors_jg: (.*?), authors_address', raw_content=content)

            authors_address = self.base_pick_array(patt_str='authors_address: (.*?), wzlx', raw_content=content)

            # 基金项目
            jjxm = self.base_pick(patt_str='xmlb: (.*?), jjlb', raw_content=content)

            print(index)
            # print('     catation:', catation)
            print('     url:', url)
            print('     sno:', sno)
            print('     title:', title)
            print('     title_en:', title_en)
            print('     authors:', authors)  # 作者
            print('     authors_jg:', authors_jg)  # 机构
            print('     authors_address:', authors_address)  # 地址
            print('     jjxm:', jjxm)  # 机构
            print('     lyqk:', lyqk)  # 分类
            print('     keywords:', keywords)  # 关键词


if __name__ == '__main__':
    s = Scanner()
    s.run()
