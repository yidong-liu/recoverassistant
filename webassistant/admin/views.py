from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.views import View
from django.views.decorators.http import require_http_methods

from user.models import UserInfo, FeedbackInfo, QueryLog


# Create your views here.
class UserManagement(View):
    """展示用户管理界面"""
    def get(self, request):
        # 判断当前用户的身份
        user_id = request.session.get('user_id')
        user = UserInfo.objects.get(id=user_id)
        user_list = []
        if user.authority == 1:  # 判断是否是超级管理员
            user_list = UserInfo.objects.all()
        # 分页显示
        paginator = Paginator(user_list, 5)
        page_number = request.GET.get('page')       # 获取当前页面序号
        page_obj = paginator.get_page(page_number)  # 获取页面对象

        context = {
            'user_list': user_list,
            'page_obj': page_obj,
            'user': user,
        }
        return render(request, 'admin/user-management.html', context=context)


@require_http_methods('GET')
def delete_user(request):
    """删除用户"""
    pk = request.GET.get('id')
    UserInfo.objects.filter(id=pk).delete()

    return redirect('admin:user_management')


class FeedbackManagement(View):
    """展示反馈信息管理界面"""

    def get(self, request):
        # 判断当前用户的身份
        user_id = request.session.get('user_id')
        user = UserInfo.objects.get(id=user_id)
        feedback_list = []
        if user.authority == 1:  # 判断是否是超级管理员
            feedback_list = FeedbackInfo.objects.all()  # 管理员获得所有反馈的列表
        # 分页显示
        paginator = Paginator(feedback_list, 5)
        page_number = request.GET.get('page')       # 获取当前页面序号
        page_obj = paginator.get_page(page_number)  # 获取页面对象

        context = {
            'feedback_list': feedback_list,
            'page_obj': page_obj,
            'user': user,
        }
        return render(request, 'admin/feedback-management.html', context=context)


@require_http_methods('GET')
def delete_feedback(request):
    """删除反馈"""
    pk = request.GET.get('id')
    FeedbackInfo.objects.filter(id=pk).delete()

    return redirect('admin:feedback_management')


@require_http_methods('GET')
def collect_feedback(request):
    """将反馈设置为已解决"""
    # 获得题目的id
    feedback_id = request.GET.get('id')
    # 设置为已解决
    feedback = FeedbackInfo.objects.get(id=feedback_id)   # 获得题目对象
    feedback.collection = True   # 将题目是否收藏的标志位设为真
    feedback.save()              # 保存
    return redirect('admin:feedback_management')


class LogManagement(View):
    """展示日志信息管理界面"""
    def get(self, request):
        # 判断当前用户的身份
        user_id = request.session.get('user_id')
        user = UserInfo.objects.get(id=user_id)
        log_list = QueryLog.objects.all()  # 管理员获得所有反馈的列表
        # 分页显示
        paginator = Paginator(log_list, 5)
        page_number = request.GET.get('page')       # 获取当前页面序号
        page_obj = paginator.get_page(page_number)  # 获取页面对象

        context = {
            'feedback_list': log_list,
            'page_obj': page_obj,
            'user': user,
        }
        return render(request, 'admin/log-management.html', context=context)


@require_http_methods('GET')
def delete_log(request):
    """删除日志"""
    pk = request.GET.get('id')
    QueryLog.objects.filter(id=pk).delete()

    return redirect('admin:log_management')


@require_http_methods('GET')
def log_detail(request):
    """展示题目详情"""
    pk = request.GET.get('id')
    query_log = QueryLog.objects.get(id=pk)

    return render(request, 'admin/log-detail.html', {'query_log': query_log})
