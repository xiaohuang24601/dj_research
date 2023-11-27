import random

from django.db import models

# Create your models here.
from django.db.models import Avg
from django.utils import timezone


def gen_referenced_count():
    return random.randint(0, 10)


def gen_h_index():
    return random.randint(0, 30)


class Scholar(models.Model):
    """学者"""
    name = models.CharField('名字', max_length=255)
    organization = models.CharField('机构', max_length=255, null=True, blank=True)
    json_str = models.TextField('原始json', null=True, blank=True)
    h_index = models.IntegerField('h指数', null=True, blank=True, default=gen_h_index)
    referenced_count = models.IntegerField('被引用', null=True, blank=True, default=gen_referenced_count)
    created_at = models.DateTimeField('时间', default=timezone.now)

    class Meta:
        verbose_name = '学者'
        verbose_name_plural = '学者'
        db_table = 'scholar'  # 指定 数据库表名，不设置则会从 class name 读取

    def __str__(self):
        return self.name

    def _get_scholar_research_dict(self):
        """获取 某个学者的 研究领域"""

        # 找出所有的论文
        li_paper_this_author = Paper.objects.filter(li_authors=self.id)

        di_keyword = {}
        for paper_item in li_paper_this_author:
            # 获取所有的关键词
            li_keywords = paper_item.li_keywords.all()

            # 遍历 当前论文的 所有关键词
            for keyword in li_keywords:
                key_val = keyword.value

                if key_val in di_keyword:  # 记录过，+1
                    di_keyword[key_val] += 1
                else:  # 未记录，初始化
                    di_keyword[key_val] = 1

        return di_keyword

    def _get_scholar_research_list(self):
        return sorted(
            [
                {'name': k, 'value': v}
                for k, v in self._get_scholar_research_dict().items()
            ],
            reverse=True,
            key=lambda x: x['value']
        )

    def get_scholar_info(self):
        return {
            'id': self.id,
            'name': self.name,
            'organization': self.organization,
            'h_index': self.h_index,
            'referenced_count': self.referenced_count,
            'count_paper': self.paper_set.count(),  # 发文量
            # 研究领域 列表，倒序排列
            'li_research': self._get_scholar_research_list()
        }


class Keywords(models.Model):
    """关键词（领域）"""
    value = models.CharField('关键词', max_length=255)
    created_at = models.DateTimeField('时间', default=timezone.now)

    class Meta:
        verbose_name = '关键词'
        verbose_name_plural = '关键词'
        db_table = 'keywords'  # 指定 数据库表名，不设置则会从 class name 读取

    def __str__(self):
        return self.value

    def get_keyword_detail(self):
        # 找出 当前 领域的所有文献
        tmp_paper = Paper.objects.filter(li_keywords__id=self.id)

        li_all_paper_id = [item.id for item in tmp_paper.all()]

        # 相关作者
        print(tmp_paper)
        # 通过 所有文献id，找出所有的作者
        tmp_all_author = Scholar.objects.filter(
            paper__in=li_all_paper_id  # 筛选 文献id
        )

        # 总发文量
        total_post = Paper.objects.filter(id__in=li_all_paper_id).count()

        # 人均 发文量
        avg_post = total_post / tmp_all_author.count()

        # 领域学者 人均 h指数
        avg_h_index = tmp_all_author.aggregate(
            Avg('h_index')
        )['h_index__avg']

        # 领域学者 人均 被引量
        avg_referenced_count = tmp_all_author.aggregate(
            Avg('referenced_count')
        )['referenced_count__avg']

        return {
            'id': self.id,
            'value': self.value,
            'li_paper': tmp_paper.all(),
            'count_paper': tmp_paper.count(),
            'li_author': [
                item.get_scholar_info()
                for item in tmp_all_author
            ],
            'count_author': tmp_all_author.count(),
            'total_post': total_post,
            'avg_post': avg_post,
            'avg_h_index': avg_h_index,
            'avg_referenced_count': avg_referenced_count
        }


class Paper(models.Model):
    """论文"""
    title = models.CharField('标题', max_length=255)
    title_en = models.CharField('英文标题', max_length=255)
    project = models.CharField('项目', max_length=255, null=True, blank=True)
    periodical = models.CharField('期刊名称', max_length=255, null=True, blank=True)
    sno = models.CharField('sno', max_length=255, null=True, blank=True)
    json_str = models.TextField('原始json', null=True, blank=True)
    url = models.CharField('链接', max_length=255, null=True, blank=True)
    created_at = models.DateTimeField('时间', default=timezone.now)

    # 作者（领域）（多对多）
    li_authors = models.ManyToManyField(Scholar, verbose_name='作者')

    # 关键词（领域）（多对多）
    li_keywords = models.ManyToManyField(Keywords, verbose_name='关键词(领域)')

    class Meta:
        verbose_name = '论文'
        verbose_name_plural = '论文'
        db_table = 'paper'  # 指定 数据库表名，不设置则会从 class name 读取

    def __str__(self):
        return self.title
