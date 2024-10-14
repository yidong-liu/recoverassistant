from django.views import View
from transformers import AutoTokenizer, AutoModel
import json
from django.shortcuts import render, redirect
import openai
import requests
# 从secret_key文件中导入生成的API密钥
from .secret_key import API_KEY
# 从secret_key文件中加载API密钥
openai.api_key = API_KEY
# 历史消息列表
history = []
# langchain模型
model = None
tokenizer = None


# 这是处理主页逻辑的主视图
def home(request):
    try:
        # 如果会话没有消息密钥，请创建消息密钥
        if 'messages' not in request.session:
            request.session['messages'] = [
                {"role": "system", "content": "你现在正在与用户聊天，为他们提供全面、简短、简洁的答案。"},
            ]
        if request.method == 'POST':
            # 从表单中获取提示
            prompt = request.POST.get('prompt')
            # 从表单中获取随机性参数
            temperature = float(request.POST.get('temperature', 0.1))
            # 将提示追加到消息列表
            request.session['messages'].append({"role": "user", "content": prompt})
            # 设置会话为修改会话
            request.session.modified = True
            # 调用openai API
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=request.session['messages'],
                temperature=temperature,
                max_tokens=1000,
            )
            # 格式化响应
            formatted_response = response['choices'][0]['message']['content']
            # 将响应追加到消息列表
            request.session['messages'].append({"role": "assistant", "content": formatted_response})
            request.session.modified = True
            # 重定向到主页
            context = {
                'messages': request.session['messages'],
                'prompt': '',
                'temperature': temperature,
            }
            return render(request, 'assistant/home.html', context)
        else:
            # 如果请求不是POST请求，则呈现主页
            context = {
                'messages': request.session['messages'],
                'prompt': '',
                'temperature': 0.1,
            }
            return render(request, 'assistant/home.html', context)
    except Exception as e:
        print(e)
        # 如果有错误，重定向到错误处理程序
        return redirect('error_handler')



def home2(request):
    try:
        # 如果会话没有消息密钥，请创建消息密钥
        if 'messages' not in request.session:
            request.session['messages'] = [
                {"role": "system", "content": "你现在正在与用户聊天，为他们提供全面、简短、简洁的答案。"},
            ]
        if request.method == 'POST':
            # 从表单中获取提示
            prompt = request.POST.get('prompt')
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
            print(type(formatted_response))
            # 将响应追加到消息列表
            request.session['messages'].append({"role": "assistant", "content": formatted_response})
            request.session.modified = True
            # 重定向到主页
            context = {
                'messages': request.session['messages'],
                'prompt': '',
                'temperature': temperature,
            }
            return render(request, 'assistant/home2.html', context)
        else:
            # 如果请求不是POST请求，则呈现主页
            context = {
                'messages': request.session['messages'],
                'prompt': '',
                'temperature': 0.1,
            }
            return render(request, 'assistant/home2.html', context)
    except Exception as e:
        print(e)
        # 如果有错误，重定向到错误处理程序
        return redirect('error_handler')


class ChatView(View):
    def get(self, request):
        try:
            global model
            global tokenizer
            # 如果会话没有消息密钥，请创建消息密钥
            if 'messages' not in request.session:
                request.session['messages'] = [
                    {"role": "system", "content": "你现在正在与用户聊天，为他们提供全面、简短、简洁的答案。"},
                ]
            tokenizer = AutoTokenizer.from_pretrained("THUDM/chatglm3-6b", trust_remote_code=True)
            model = AutoModel.from_pretrained("THUDM/chatglm3-6b", trust_remote_code=True).half().cuda()
            model = model.eval()

            context = {
                'messages': request.session['messages'],
                'prompt': '',
                'temperature': 0.1,
            }
            return render(request, 'assistant/home2.html', context)
        except Exception as e:
            print(e)
            # 如果有错误，重定向到错误处理程序
            return redirect('error_handler')



    def post(self, request):
        try:
            global history
            # 从表单中获取提示
            prompt = request.POST.get('prompt')
            # 从表单中获取随机性参数
            temperature = float(request.POST.get('temperature', 0.1))
            # 将提示追加到消息列表
            request.session['messages'].append({"role": "user", "content": prompt})
            # 设置会话为修改会话
            request.session.modified = True

            response, history = model.chat(tokenizer, f"{prompt}", history=history)

            # 格式化响应
            formatted_response = response
            # 将响应追加到消息列表
            request.session['messages'].append({"role": "assistant", "content": formatted_response})
            request.session.modified = True

            # 重定向到主页
            context = {
                'messages': request.session['messages'],
                'prompt': '',
                'temperature': temperature,
            }
            return render(request, 'assistant/home2.html', context)

        except Exception as e:
            print(e)
            # 如果有错误，重定向到错误处理程序
            return redirect('error_handler')


def home3(request):
    try:
        global history
        # 如果会话没有消息密钥，请创建消息密钥
        if 'messages' not in request.session:
            request.session['messages'] = [
                {"role": "system", "content": "你现在正在与用户聊天，为他们提供全面、简短、简洁的答案。"},
            ]
        if request.method == 'POST':
            # 从表单中获取提示
            prompt = request.POST.get('prompt')
            # 从表单中获取随机性参数
            temperature = float(request.POST.get('temperature', 0.1))
            # 将提示追加到消息列表
            request.session['messages'].append({"role": "user", "content": prompt})
            # 设置会话为修改会话
            request.session.modified = True
            # 调用langchain API
            tokenizer = AutoTokenizer.from_pretrained("THUDM/chatglm3-6b", trust_remote_code=True)
            model = AutoModel.from_pretrained("THUDM/chatglm3-6b", trust_remote_code=True).half().cuda()
            model = model.eval()

            response, history = model.chat(tokenizer, f"{prompt}", history=history)

            # 格式化响应
            formatted_response = response
            # 将响应追加到消息列表
            request.session['messages'].append({"role": "assistant", "content": formatted_response})
            request.session.modified = True
            # 重定向到主页
            context = {
                'messages': request.session['messages'],
                'prompt': '',
                'temperature': temperature,
            }
            return render(request, 'assistant/home2.html', context)
        else:
            # 如果请求不是POST请求，则呈现主页
            context = {
                'messages': request.session['messages'],
                'prompt': '',
                'temperature': 0.1,
            }
            return render(request, 'assistant/home2.html', context)
    except Exception as e:
        print(e)
        # 如果有错误，重定向到错误处理程序
        return redirect('error_handler')







# 生成新的聊天
def new_chat(request):
    # 清除消息列表
    request.session.pop('messages', None)
    return redirect('home')


# 这是处理错误的视图
def error_handler(request):
    return render(request, 'assistant/404.html')
