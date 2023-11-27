import jieba
from django.contrib import messages
from django.db.models import Avg, Q
from django.shortcuts import render, redirect

# Create your views here.
from science.models import Paper, Scholar, Keywords


def index(request):
    """首页"""

    # 获取 文献列表
    keyword = request.GET.get('keyword', '')
    page = int(request.GET.get('page', 1))
    limit = 10

    start = (page - 1) * limit

    tmp_paper = Paper.objects.filter(
        title__icontains=keyword
    )

    count_paper = tmp_paper.count()  # 数据量

    return render(
        request,
        'index.html',
        context={
            'li_paper': tmp_paper.order_by('-id')[start:start + limit],
            'count_paper': count_paper,
        }
    )


def scholar_list(request):
    """学者列表"""

    # 获取 关键词
    keyword = request.GET.get('keyword', '')
    page = int(request.GET.get('page', 1))
    limit = 10

    start = (page - 1) * limit

    tmp_scholar = Scholar.objects

    if keyword:
        tmp_scholar = tmp_scholar.filter(
            Q(name__icontains=keyword)
            |
            Q(paper__li_keywords__value__icontains=keyword)
        ).distinct()

    return render(
        request,
        'scholar_list.html',
        context={
            'li_scholar': [
                item.get_scholar_info()
                for item in tmp_scholar.order_by('-id')[start:start + limit]
            ],
            'count_scholar': tmp_scholar.count(),
            'di_author_group': get_scholar_group(1)
        }
    )


def scholar_detail(request, sid):
    """学者详情"""

    db_scholar = Scholar.objects.get(id=sid)

    if not db_scholar:  # 不存在，去首页
        messages.error(request, '学者id 不存在')
        return redirect('/')

    # ———— 找出当前学者的合作关系（一起发过论文的人）————
    di_author_group = get_scholar_group(sid)  # 找出所有的合作伙伴

    # 提取 所有论文的所有领域

    return render(
        request,
        'scholar_detail.html',
        context={
            'scholar': db_scholar.get_scholar_info(),
            # 合作伙伴-柱状图
            'li_author_group': {
                'li_x': list(di_author_group.keys()),
                'li_y': list(di_author_group.values())
            },
            # 获取 研究领域
        }
    )


def get_scholar_group(sid):
    """找出某个学者的合作关系"""
    # 找出所有的论文
    li_paper_this_author = Paper.objects.filter(li_authors=sid)

    # 提取 所有合作作者
    di_author_group = {}
    for paper_item in li_paper_this_author:
        li_author = paper_item.li_authors.exclude(id=sid)
        print(li_author)

        for author_other in li_author:
            author_name = author_other.name

            if author_name in di_author_group:  # 记录过，+1
                di_author_group[author_name] += 1
            else:  # 未记录，初始化
                di_author_group[author_name] = 1

    return di_author_group


def keyword_list(request):
    """关键词列表"""

    # 获取 搜索key
    key = request.GET.get('keyword', '')

    page = int(request.GET.get('page', 1))
    limit = 10

    start = (page - 1) * limit

    tmp_keywords = Keywords.objects.filter(
        value__icontains=key
    )

    return render(
        request,
        'keyword_list.html',
        context={
            'li_keywords': [
                k.get_keyword_detail()
                for k in tmp_keywords.order_by('-id')[start:start + limit]
            ],
            'count_keywords': tmp_keywords.count()
        }
    )
    pass


def keyword_detail(request, value):
    """领域详情"""

    db_keyword = Keywords.objects.get(value=value)

    if not db_keyword:
        messages.error(request, '领域id 不存在')
        return redirect('/')

    return render(
        request,
        'keyword_detail.html',
        context={
            'keyword_detail': db_keyword.get_keyword_detail()
        }
    )


def _get_word_cloud_for_group(sid):
    """根据 某个学者，制作 团队词云图"""

    di_count = {}

    # 获取 学者的所有团队的 领域，标题
    content = ''
    for paper_item in Paper.objects.filter(li_authors__id=sid).all():
        title = paper_item.title  # 标题
        str_keywords = ';'.join(
            [
                k.value
                for k in paper_item.li_keywords.all()
            ]
        )
        content += title + ';'
        content += str_keywords

    # 分词
    words = jieba.lcut(content)

    # 遍历单词
    for word in words:
        if word in (',', '，', ';', '；', '.', '。', '(', ')'):  # 过滤词
            continue

        # 统计
        di_count[word] = di_count.get(word, 0) + 1

    # 输出为 二位数组，用于词云图使用
    return [
        {'name': k, 'value': v}
        for k, v in di_count.items()
        # if v > 2
    ]


def group_list(request, sid):
    """团队列表"""

    di_all_author = {}  # 作者统计字典

    di_all_research = {}  # 所有的 领域

    # 当前作者
    now_author = Scholar.objects.get(id=sid)

    # 遍历 当前作者的 所有论文
    for paper_item in Paper.objects.filter(li_authors=sid):
        # ———— 获取 当前论文的 所有作者（除了当前作者）————
        for author_other in paper_item.li_authors.exclude(id=sid):
            author_id = author_other.id  # 作者id

            # 统计次数
            if author_id not in di_all_author:  # 不存在，初始化
                di_all_author[author_id] = 1
            else:  # 存在，+1
                di_all_author[author_id] += 1

        # ———— 获取 所有领域 ————
        for keyword_item in paper_item.li_keywords.all():
            keyword_val = keyword_item.value  # 领域关键词

            # 统计
            if keyword_val not in di_all_research:  # 不存在，初始化
                di_all_research[keyword_val] = 1
            else:
                di_all_research[keyword_val] += 1

    # 查询 学者信息
    tmp_scholar = Scholar.objects.filter(
        id__in=list(di_all_author.keys())  # 筛选所有的 作者
    )

    # 团队的 作者id 列表
    li_group_author_id = [
        *list(di_all_author.keys()),
        sid
    ]

    total_count_post = _get_total_post_for_group(li_group_author_id)

    avg_h_index = Scholar.objects.filter(id__in=li_group_author_id).aggregate(
        Avg('h_index')
    )['h_index__avg']

    avg_referenced_count = Scholar.objects.filter(id__in=li_group_author_id).aggregate(
        Avg('referenced_count')
    )['referenced_count__avg']

    return render(
        request,
        'group_list.html',
        context={
            'now_author': now_author,  # 当前作者
            'list': [
                {
                    **item.get_scholar_info(),
                    'coop_count': di_all_author[item.id],  # 获取作者的合作次数
                }
                for item in tmp_scholar.order_by('-id')[:20]
            ],
            'count': tmp_scholar.count(),
            # 团队所有成员的 研究领域
            'all_research_pie': [
                {'name': k, 'value': v}
                for k, v in di_all_research.items()
            ],
            # 词云图
            'word_cloud': _get_word_cloud_for_group(sid),
            # 团队总发文量
            'total_count_post': total_count_post,
            # 平均发文量
            'avg_count_post': total_count_post / len(li_group_author_id),
            # 平均 h指数
            'avg_count_h_index': avg_h_index,
            # 平均 被引量
            'avg_count_referenced': avg_referenced_count,
        }
    )


def _get_total_post_for_group(li_group_author_id):
    """团队 总发文量"""

    # 找出 所有作者的所有论文数量
    return Paper.objects.filter(li_authors__in=li_group_author_id).count()
