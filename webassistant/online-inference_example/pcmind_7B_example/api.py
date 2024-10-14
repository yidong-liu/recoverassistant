#通过api方式访问
#注意访问路由需要在启动在线推理任务后获取，如本示例中的访问get请求的api路由是https://mlunotebook.openi.org.cn/notebook_ja19ce9608174f8aa12525bc3b84806c_task0/api
#其中，https://mlunotebook.openi.org.cn/notebook_ja19ce9608174f8aa12525bc3b84806c_task0由os.getenv('OPENI_SELF_URL')获取
import os 
from fastapi import FastAPI
import uvicorn
app = FastAPI()
from c2net.context import prepare

#初始化导入数据集和预训练模型到容器内
c2net_context = prepare()
#获取预训练模型路径
pretrain_model_path = c2net_context.pretrain_model_path
base_url = os.getenv('OPENI_SELF_URL')

# 定义GET请求的路由
@app.get(os.path.join(base_url, "api"))
async def api_get():
    return "This is a GET request."

# 定义POST请求的路由
@app.post(os.path.join(base_url, "apipost"))
async def api_post():
    # 在这里执行模型推理等操作
    # 省略代码

    # 返回结果
    return {'output': "output_text"}


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=int(os.getenv('OPENI_SELF_PORT')))

