from django.contrib.auth.hashers import make_password, check_password
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views import View
from django.views.decorators.http import require_http_methods
from django.utils.timezone import now
import requests
import json
import re
from transformers import AutoTokenizer, AutoModel
from user.models import UserInfo, FeedbackInfo, QueryLog
# 历史消息列表
history = []
# langchain模型
model = None
tokenizer = None

# Create user views here.


class LoginView(View):

    def get(self, request):
        """用户get请求渲染登陆页面"""
        return render(request, 'user/login.html')

    def post(self, request):
        """用户post请求验证用户身份"""
        try:
            name = request.POST.get('name')
            password = request.POST.get('password')
            maintain_entry = request.POST.get('maintain_entry')
            user = UserInfo.objects.filter(name=name)[0]
            if user:
                encrypt_pwd = user.password
                if check_password(password, encrypt_pwd):
                    response = JsonResponse({'code': 1})  # 成功
                    if maintain_entry:
                        response.set_cookie("user_status", "is_login", max_age=10*24*60*60)
                    else:
                        response.set_cookie("user_status", "is_login")

                    # 将登陆用户的ID和姓名存入session
                    request.session['user_id'] = user.id
                    request.session['user_name'] = user.name

                    return response
                else:
                    return JsonResponse({'code': 0})  # 密码错误
            else:
                return JsonResponse({'code': 0})     # 用户不存在
        except Exception as e:
            print(e)
            return JsonResponse({'code': 0})


class RegisterView(View):

    def get(self, request):
        """用户get请求渲染注册页面"""
        return render(request, 'user/register.html')

    def post(self, request):
        """用户post请求创建账号"""
        try:
            # 获取来自register.html模板的表单数据
            name = request.POST.get('name')
            phone = request.POST.get('phone')
            password = request.POST.get('password')
            print('新用户 = ', name, phone, password)
            encrypt_pwd = make_password(password)
            # 创建一个新用户
            UserInfo.objects.create(name=name, phone=phone, password=encrypt_pwd)
            return JsonResponse({'code': 1})  # 注册成功
        except Exception as e:
            print(e)
            return JsonResponse({'code': 0})  # 注册失败


@require_http_methods('POST')
def check_user(request):
    """验证是否存在同名用户"""
    name = request.POST.get('name')
    user = UserInfo.objects.filter(name=name)
    print('user', user)
    if user:
        return JsonResponse({'code': 0})
    else:
        return JsonResponse({'code': 1})


def home(request):
    """用户的主页面"""

    # 等到当前登陆的用户信息
    user_name = request.session.get('user_name', '游客')
    user = UserInfo.objects.get(name=user_name)

    if user.authority == 0:
        # 如果会话没有消息密钥，请创建消息密钥
        if 'messages' not in request.session:
            request.session['messages'] = [
                {"role": "system", "content": "你现在正在与用户聊天，为他们提供全面、简短、简洁的答案。"},
            ]
        if request.method == 'POST':
            # 从表单中获取提示
            prompt = request.POST.get('prompt')
            # 记录日志信息，提问的问题和时间
            query_log = QueryLog(query_text=prompt, query_timestamp=now())

            # 从表单中获取随机性参数
            temperature = float(request.POST.get('temperature', 0.1))
            # 将提示追加到消息列表
            request.session['messages'].append({"role": "user", "content": prompt})
            # 设置会话为修改会话
            request.session.modified = True
            # 调用openai API
            url = "https://api.openai-hk.com/v1/chat/completions"

            headers = {
                "Content-Type": "application/json",
                "Authorization": "hk-genxxb100000605003026d2fe19e4c95f79ed34e09b04b5d"
            }

            data = {
                "max_tokens": 1200,
                "model": "gpt-3.5-turbo",
                "temperature": 0.8,
                "top_p": 1,
                "presence_penalty": 1,
                "messages": [
                    {
                        "role": "system",
                        "content": "You are ChatGPT, a large language model trained by OpenAI. Answer as concisely as possible."
                    },
                    {
                        "role": "user",
                        "content": f"{prompt}"
                    }
                ]
            }

            response = requests.post(url, headers=headers, data=json.dumps(data).encode('utf-8'))
            result = response.json()

            # 格式化响应
            formatted_response = result['choices'][0]['message']['content']
            # 记录日志的回答信息
            query_log.response_text = formatted_response
            query_log.response_timestamp = now()
            query_log.save()  # 保存日志
            # 将响应追加到消息列表
            request.session['messages'].append({"role": "assistant", "content": formatted_response})
            request.session.modified = True
            # 重定向到主页
            context = {
                'messages': request.session['messages'],
                'prompt': '',
                'temperature': temperature,
                'user_name': user_name,
                'user': user,
            }
            print(user_name)
            return render(request, 'index.html', context)
        else:
            # 如果请求不是POST请求，则呈现主页
            context = {
                'messages': request.session['messages'],
                'prompt': '',
                'temperature': 0.1,
                'user_name': user_name,
                'user': user,
            }
            return render(request, 'index.html', context)

    else:
        return redirect('admin:user_management')


def chat(request):
    """加载LLM模型"""
    global model
    global tokenizer
    # 调用langchain API
    tokenizer = AutoTokenizer.from_pretrained("THUDM/chatglm3-6b", trust_remote_code=True)
    model = AutoModel.from_pretrained("THUDM/chatglm3-6b", trust_remote_code=True).half().cuda()
    model = model.eval()
    return redirect('user:home')


def questions_and_answers(request):
    """用户的主页面"""
    global history
    global model
    global tokenizer
    # 等到当前登陆的用户信息
    user_name = request.session.get('user_name', '游客')
    user = UserInfo.objects.get(name=user_name)

    if user.authority == 0:
        if request.method == 'GET':
            # 如果会话没有消息密钥，请创建消息密钥
            if 'messages' not in request.session:
                request.session['messages'] = [
                    {"role": "system", "content": "你现在正在与用户聊天，为他们提供全面、简短、简洁的答案。"},
                ]

            context = {
                'messages': request.session['messages'],
                'prompt': '',
                'temperature': 0.1,
            }
            return render(request, 'user/FAQs.html', context)
        if request.method == 'POST':
            # 从表单中获取提示
            prompt = request.POST.get('prompt')
            # 记录日志信息，提问的问题和时间
            query_log = QueryLog(query_text=prompt, query_timestamp=now())

            # 从表单中获取随机性参数
            temperature = float(request.POST.get('temperature', 0.1))
            # 将提示追加到消息列表
            request.session['messages'].append({"role": "user", "content": prompt})
            # 设置会话为修改会话
            request.session.modified = True
            response, history = model.chat(tokenizer, f"{prompt}", history=history)

            # 格式化响应
            formatted_response = response
            # 记录日志的回答信息
            query_log.response_text = formatted_response
            query_log.response_timestamp = now()
            query_log.save()  # 保存日志
            # 将响应追加到消息列表
            request.session['messages'].append({"role": "assistant", "content": formatted_response})
            request.session.modified = True
            # 重定向到主页
            context = {
                'messages': request.session['messages'],
                'prompt': '',
                'temperature': temperature,
                'user_name': user_name,
                'user': user,
            }
            print(user_name)
            return render(request, 'user/FAQs.html', context)
        else:
            # 如果请求不是POST请求，则呈现主页
            context = {
                'messages': request.session['messages'],
                'prompt': '',
                'temperature': 0.1,
                'user_name': user_name,
                'user': user,
            }
            return render(request, 'user/FAQs.html', context)

    else:
        return redirect('admin:user_management')


def home2(request):
    flag = True
    context = {}
    # 等到当前登陆的用户信息
    user_name = request.session.get('user_name', '游客')
    user = UserInfo.objects.get(name=user_name)
    while flag:
        try:
            url = 'https://jiankang.baidu.com/widescreen/home'
            spider = HealthCrawler(url)
            article_list = spider.run()
            context = {
                'article_list': article_list,
                'user_name': user_name,
                'user': user,
            }
            flag = False
        except Exception as e:
            print(e)

    return render(request, 'index.html', context=context)


# 生成新的聊天
def new_chat(request):
    # 清除消息列表
    global history
    history = []
    request.session.pop('messages', None)
    return redirect('user:repeat_chat')


def profile(request):
    """用户个人中心"""
    pk = request.session.get('user_id')
    user = UserInfo.objects.get(id=pk)

    return render(request, 'user/profile.html', {'user': user})


@require_http_methods('GET')
def user_logout(request):
    """用户退出登陆"""
    response = redirect('user:login')
    response.delete_cookie('user_status')

    return response


class AddFeedback(View):
    """添加反馈"""
    def get(self, request):
        return render(request, 'user/add-feedback.html')

    def post(self, request):
        try:
            # 上传人
            user_id = request.session.get('user_id')
            current_user = UserInfo.objects.get(id=user_id)
            # 反馈内容
            description = request.POST.get('description')
            FeedbackInfo.objects.create(
                description=description,
                uploader=current_user
            )
            return JsonResponse({'code': 1})
        except Exception as e:
            print(e)
            return JsonResponse({'code': 0})


class HealthCrawler:
    def __init__(self, url):
        self.url = url
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.0.0'
        }
        self.text = ''
        self.detail_list = []
        self.session = requests.session()

    def get_html(self):
        response = self.session.get(self.url, headers=self.headers)
        response.encoding = 'utf-8'
        self.text = response.text

    def parse_data(self):
        result = re.findall(r'<script id="__NEXT_DATA__" type="application/json">(.*?)</script>', self.text, re.S)
        json_dict = json.loads(result[0])
        for item in json_dict['props']['pageProps']['authorityData']['tabs'][0]['items'][:3]:
            # 封面图片
            image = item['image']
            # 细节URL
            detail_url = item['url']
            # 标题
            title = item['title']
            # 发稿人
            author_hospital = item['doctorInfo']['hospital']
            author_title = item['doctorInfo']['title']
            author_name = item['doctorInfo']['name']
            author = author_hospital + ' ' + author_title + ' ' + author_name
            self.detail_list.append({
                'image': image,
                'detail_url': detail_url,
                'title': title,
                'author': author
            })

    def get_detail_html(self):
        for item in self.detail_list:
            detail_url = item['detail_url']
            response = self.session.get(detail_url, headers=self.headers)
            response.encoding = 'utf-8'

            result = re.findall(r'<script id="__NEXT_DATA__" type="application/json">(.*?)</script>', response.text, re.S)
            json_dict = json.loads(result[0])
            item['content'] = json_dict['props']['pageProps']['contentData']['content'][0]
            # item['date'] = json_dict['props']['pageProps']['contentData']['date']


    def run(self):
        self.get_html()
        self.parse_data()
        self.get_detail_html()
        return self.detail_list
