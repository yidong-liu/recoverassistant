<template>
  <div class="login-container">
    <div class="logo">
      <div class="fontAnimation">
        <span>I</span>
        <span>n</span>
        <span>t</span>
        <span>e</span>
        <span>l</span>
        <span>l</span>
        <span>i</span>
        <span>g</span>
        <span>e</span>
        <span>t</span>
      </div>
      <div class="fontAnimation">
        <span>R</span><span>e</span><span>h</span><span>b</span><span>i</span><span>t</span
        ><span>a</span><span>t</span><span>i</span><span>o</span>
        <span>n</span>
      </div>
    </div>
    <div class="form" v-if="changeStatus === 'login'">
      <h1>登录</h1>
      <a class="goRegister" @click="change('register')">没有账号 免费注册</a>
      <el-card shadow="never" class="login-card">
        <!--登录表单-->
        <!-- el-form > el-form-item > el-input -->
        <el-form ref="form">
          <div class="checkRole">
            <el-radio-group v-model="role" class="ml-4">
              <el-radio label="0" size="large">医生</el-radio>
              <el-radio label="1" size="large">患者</el-radio>
            </el-radio-group>
          </div>
          <el-form-item>
            <el-input placeholder="请输入用户名" v-model="loginUserName" />
          </el-form-item>
          <el-form-item>
            <el-input
              placeholder="请输入密码"
              v-model="loginPassword"
              type="password"
              autocomplete="off"
            />
          </el-form-item>

          <el-form-item>
            <el-button style="width: 350px" type="primary" @click="login">登录</el-button>
          </el-form-item>
        </el-form>
      </el-card>
    </div>
    <div class="form" v-else>
      <h1>注册</h1>
      <a class="goRegister" @click="change('login')">已有账号 去登陆</a>
      <div class="checkRole">
        <el-radio-group v-model="role" class="ml-4">
          <el-radio label="0" size="large">医生</el-radio>
          <el-radio label="1" size="large">患者</el-radio>
        </el-radio-group>
      </div>
      <div class="passwordForm">
        <el-form ref="ruleFormRef" :model="ruleForm" status-icon :rules="rules" label-width="20px">
          <el-form-item prop="userName" required>
            <el-input
              v-model="ruleForm.userName"
              type="text"
              autocomplete="off"
              placeholder="请输入用户名"
            />
          </el-form-item>

          <el-form-item prop="userName" required>
            <el-input
              v-model="ruleForm.name"
              type="text"
              autocomplete="off"
              placeholder="请输入姓名"
            />
          </el-form-item>
          <el-form-item prop="newPass" required>
            <el-input
              v-model="ruleForm.newPass"
              type="password"
              autocomplete="off"
              placeholder="请输入密码"
            />
          </el-form-item>
          <el-form-item prop="checkPass" required>
            <el-input
              v-model="ruleForm.checkPass"
              type="password"
              autocomplete="off"
              placeholder="请输入重复密码"
            />
          </el-form-item>

          <el-form-item>
            <el-button type="primary" @click="register(ruleFormRef)">注册</el-button>
          </el-form-item>
        </el-form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import { goRegister, goLogin } from '@/api/index.js'
import useStore from '@/stores/index'
const { mainStore } = useStore()
import open from '@/utils/message'
const router = useRouter()
const role = ref('0')
const changeStatus = ref('login')
const change = (status) => {
  changeStatus.value = status
}
const loginPassword = ref('')
const loginUserName = ref('')
const login = async () => {
  if (loginPassword.value.trim() == '' || loginUserName.value.trim() == '') {
    open('请输入用户名和密码', 'error')
    return
  }
  let result
  if (role.value == '0') {
    result = await goLogin('doctor', loginUserName.value, loginPassword.value)
  } else {
    result = await goLogin('user', loginUserName.value, loginPassword.value)
  }
  let code = result.data.code
  let message = result.data.message
  //console.log(result)
  if (code == 200) {
    //console.log(result.data.data.role,result.data.data.token)
    loginPassword.value = ''
    loginUserName.value = ''
    open('登陆成功.', 'success')
    let myRole = result.data.data.role
    let token = result.data.data.token
    localStorage.setItem('role', myRole)
    mainStore.setToken(token)
    if (myRole == 'doctor') {
      router.replace({
        path: '/doctor'
      })
    } else {
      router.replace({
        path: '/patient'
      })
    }
  } else if (code == 500) {
    open(`${message}`, 'error')
  }
}

const ruleFormRef = ref()

const checkUserName = (rule, value, callback) => {
  if (!value) {
    return callback(new Error('请输入用户名'))
  } else if (value.trim() == '') {
    return callback(new Error('名字不能为空字符'))
  } else {
    callback()
  }
}
const checkName = (rule, value, callback) => {
  if (!value) {
    return callback(new Error('请输入姓名'))
  } else if (value.trim() == '') {
    return callback(new Error('名字不能为空字符'))
  } else {
    callback()
  }
}
const validatePass = (rule, value, callback) => {
  if (value === '') {
    callback(new Error('请输入密码'))
  }
  setTimeout(() => {
    if (!/^(?![\d]+$)(?![a-zA-Z]+$)(?![^\da-zA-Z]+$)([^\u4e00-\u9fa5\s]){6,20}$/.test(value)) {
      callback(
        new Error(
          '请输入6-20位英文字母、数字或者符号（除空格），且字母、数字和标点符号至少包含两种'
        )
      )
    } else {
      callback()
    }
  }, 1000)
}
const validatePass2 = (rule, value, callback) => {
  if (value === '') {
    callback(new Error('请重复新密码！'))
  } else if (value !== ruleForm.newPass) {
    callback(new Error('两个输入不匹配!'))
  } else {
    callback()
  }
}
const ruleForm = reactive({
  userName: '',
  name: '',
  newPass: '',
  checkPass: ''
})
const rules = reactive({
  userName: [{ validator: checkUserName, trigger: 'blur' }],
  name: [{ validator: checkName, trigger: 'blur' }],
  newPass: [{ validator: validatePass, trigger: 'blur' }],
  checkPass: [{ validator: validatePass2, trigger: 'blur' }]
})
const register = (formEl) => {
  if (!formEl) return
  formEl.validate(async (valid) => {
    if (valid) {
      let result
      if (role.value == '0') {
        result = await goRegister('doctor', ruleForm.userName, ruleForm.newPass, ruleForm.name)
      } else {
        result = await goRegister('user', ruleForm.userName, ruleForm.newPass, ruleForm.name)
      }
      //console.log(result.data)
      let code = result.data.code
      if (code == 200) {
        ruleForm.userName = ''
        ruleForm.name = ''
        ruleForm.newPass = ''
        ruleForm.checkPass = ''
        //console.log(result.data)
        open('注册成功，去登陆吧.', 'success')
        changeStatus.value = 'login'
      } else if (code == 500) {
        open('用户已存在，请使用其他用户名 !', 'error')
      } else {
        console.log('error submit!')
        return false
      }
    }
  })
}
</script>

<style lang="scss">
.login-container {
  display: flex;
  align-items: stretch;
  height: 100vh;

  .logo {
    flex: 3;
    background: rgba(38, 72, 176) no-repeat center / cover;
    border-top-right-radius: 60px;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 0 100px;
    color: white;
    .fontAnimation span {
      top: 20px; /*字符上下浮动*/
      position: relative;
      animation: loading 0.5s ease 0s infinite alternate; /*引用动画*/
      /* animation: 动画名称 动画时间 动画曲线 何时开始 播放次数 是否反方向; 
            alternate:表示动画先正常运行再反方向运行，并持续交替
            infinite:表示无限循环*/
      font-size: 100px;
      color: white;
      text-shadow:
        0 1px 0 #ccc,
        0 2px 0 #ccc,
        0 3px 0 #ccc,
        0 4px 0 #ccc,
        0 5px 0 #ccc,
        0 6px 0 #ccc,
        0 7px 0 #ccc,
        0 8px 0 #ccc,
        0 9px 0 #ccc,
        0 10px 10px rgba(0, 0, 0, 0.5);
      /*text-shadow: 水平阴影位置(必须) 垂直阴影位置(必须) 模糊距离(可选) 阴影颜色(可选);
       text-shadow: h-shadow v-shadow blur color; */
    }
    .fontAnimation span:nth-child(2) {
      animation-delay: 0.1s;
    }
    .fontAnimation span:nth-child(3) {
      animation-delay: 0.2s;
    }
    .fontAnimation span:nth-child(4) {
      animation-delay: 0.3s;
    }
    .fontAnimation span:nth-child(5) {
      animation-delay: 0.4s;
    }
    .fontAnimation span:nth-child(6) {
      animation-delay: 0.5s;
    }
    @keyframes loading {
      /* 定义动画*/
      100% {
        top: -20px; /*字符上下浮动*/
        text-shadow:
          0 1px 0 #ccc,
          0 2px 0 #ccc,
          0 3px 0 #ccc,
          0 4px 0 #ccc,
          0 5px 0 #ccc,
          0 6px 0 #ccc,
          0 7px 0 #ccc,
          0 8px 0 #ccc,
          0 9px 0 #ccc,
          0 50px 25px rgba(0, 0, 0, 0.3);
      }
    }

    .icon {
      width: 300px;
      height: 50px;
      margin-bottom: 50px;
    }
    p {
      color: #fff;
      font-size: 18px;
      margin-top: 20px;
      width: 300px;
      text-align: center;
    }
  }
  .form {
    flex: 2;

    display: flex;
    flex-direction: column;
    justify-content: center;
    padding-left: 176px;
    .goRegister {
      padding: 5px 0;
      color: white;
      text-shadow: 2px 2px 4px #000000;
      padding-left: 20px;
    }
    .checkRole {
      padding: 5px 0px 10px 20px;
    }

    .el-card {
      border: none;
      padding: 0;
    }
    h1 {
      padding-left: 20px;
      font-size: 24px;
    }
    .el-input {
      width: 350px;
      height: 44px;

      .el-input__inner {
        background-color: #fff;
      }
    }
    .el-checkbox {
      color: #606266;
    }
    .el-form-item {
      margin-bottom: 25px;
    }
    .el-button {
      width: 350px;
      height: 40px;
      margin-top: 20px;
    }
  }
}
</style>
@/stores/main
