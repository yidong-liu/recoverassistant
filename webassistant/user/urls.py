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
from user import views

app_name = 'user'
urlpatterns = [
    # 用户的登陆
    re_path(r'^login/$', views.LoginView.as_view(), name='login'),
    # 用户的注册
    re_path(r'^register/$', views.RegisterView.as_view(), name='register'),
    # 用户存在性验证
    re_path(r'^check/$', views.check_user, name='check'),
    # 用户的家
    re_path(r'^home/$', views.home2, name='home'),
    # 个人主页
    re_path(r'^profile/$', views.profile, name='profile'),
    # 用户登出
    re_path(r'^logout/$', views.user_logout, name='logout'),
    # 反馈信息
    re_path(r'^add_feedback/$', views.AddFeedback.as_view(), name='add_feedback'),
    # 创建新对话
    re_path(r'^create_dialog/$', views.new_chat, name='create_dialog'),
    # 智能问答
    re_path(r'^chat/$', views.chat, name='chat'),
    # 反复对话
    re_path(r'^repeat_chat/$', views.questions_and_answers, name='repeat_chat'),
]
