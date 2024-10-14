from django.shortcuts import redirect
from django.utils.deprecation import MiddlewareMixin


class ConfirmLoginMiddleware(MiddlewareMixin):

    def process_request(self, request):
        user_status = request.COOKIES.get('user_status')
        path = request.path
        allow_path = ['/user/login/', '/user/register/']
        print(f'path = {path}')

        # 当有人登录就想访问的时候，跳转登录界面
        if user_status != 'is_login' and path not in allow_path:
            return redirect('user:login')
        
        if user_status == 'is_login' and path in ['/']:
            return redirect('user:home')

    def process_response(self, request, response):
        return response
