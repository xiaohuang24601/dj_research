from django.contrib import admin

# Register your models here.
from science.models import Paper, Scholar, Keywords


@admin.register(Paper)  # 基于 model 创建一个 admin视图
class PaperAdmin(admin.ModelAdmin):
    # 搜索关键词
    search_fields = ('title', 'title_en', 'project', 'periodical')
    # 列表里显示想要显示的字段
    list_display = ('id', 'title', 'title_en', 'project', 'periodical', 'sno',)
    # list_filter = ('name',)  # 筛选字段
    list_per_page = 20  # 满10条数据就自动分页
    ordering = ('-id',)  # 后台数据列表排序方式
    list_display_links = ('title',)  # 设置哪些字段可以点击进入编辑界面


@admin.register(Scholar)  # 基于 model 创建一个 admin视图
class ScholarAdmin(admin.ModelAdmin):
    # 搜索关键词
    search_fields = ('name', 'organization',)
    # 列表里显示想要显示的字段
    list_display = ('id', 'name', 'organization', 'h_index', 'referenced_count')
    # list_filter = ('name',)  # 筛选字段
    list_per_page = 20  # 满10条数据就自动分页
    ordering = ('-id',)  # 后台数据列表排序方式
    list_display_links = ('name',)  # 设置哪些字段可以点击进入编辑界面


@admin.register(Keywords)  # 基于 model 创建一个 admin视图
class KeywordsAdmin(admin.ModelAdmin):
    # 搜索关键词
    search_fields = ('value',)
    # 列表里显示想要显示的字段
    list_display = ('id', 'value',)
    # list_filter = ('name',)  # 筛选字段
    list_per_page = 20  # 满10条数据就自动分页
    ordering = ('-id',)  # 后台数据列表排序方式
    list_display_links = ('value',)  # 设置哪些字段可以点击进入编辑界面
