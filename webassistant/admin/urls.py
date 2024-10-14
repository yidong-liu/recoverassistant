"""nurse URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, re_path
from admin import views

app_name = 'admin'
urlpatterns = [
    # 用户管理
    re_path(r'^user_management/$', views.UserManagement.as_view(), name='user_management'),
    # 删除用户
    re_path(r'^delete/$', views.delete_user, name='delete'),
    # # 知识库管理
    # re_path(r'^knowledge_base_management/$', views.RegisterView.as_view(), name='knowledge_base_management'),
    # 反馈管理
    re_path(r'^feedback_management/$', views.FeedbackManagement.as_view(), name='feedback_management'),
    # 删除反馈
    re_path(r'^delete_feedback/$', views.delete_feedback, name='delete_feedback'),
    # 将反馈标记为已解决
    re_path(r'^collect/$', views.collect_feedback, name='collect'),
    # 日志管理
    re_path(r'^log_management/$', views.LogManagement.as_view(), name='log_management'),
    # 日志详情
    re_path(r'^log_detail/$', views.log_detail, name='log_detail'),
    # 删除日志
    re_path(r'^delete_log/$', views.delete_log, name='delete_log'),
]
