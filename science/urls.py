from django.urls import path

from . import views

urlpatterns = [
    # 主页
    path('', views.index),

    # 学者
    path('scholar_list/', views.scholar_list),  # 列表
    path('scholar_detail/<int:sid>', views.scholar_detail),  # 详情

    # 关键词
    path('keyword_list/', views.keyword_list),  # 列表
    path('keyword_detail/<str:value>', views.keyword_detail),  # 详情

    # 团队信息
    path('group_list/<int:sid>', views.group_list),  # 列表

    # 用户模块
    # path('user/register/', views.register),  # 注册
    # path('user/login/', views.login),  # 登录
    # path('user/logout/', views.logout),  # 注销
    # path('user/pwd/', views.user_pwd),  # 修改密码
    # path('user/user_info/', views.user_info),  # 个人中心

]
