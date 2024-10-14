<template>
  <div class="overlay" >
    <div class="passwordUpdateBOx">
      <div class="passwordTop">
        <span>修改密码</span>
        <span @click="hideButton">❌</span>
      </div>
      <div class="passwordForm">
        <el-form
          ref="ruleFormRef"
          :model="ruleForm"
          status-icon
          :rules="rules"
          label-width="120px"
          
        >
         <el-form-item label="旧密码" prop="oldPass" required>
            <el-input v-model="ruleForm.oldPass" type="password" autocomplete="off"/>
          </el-form-item>
          <el-form-item label="新密码" prop="newPass" required>
            <el-input v-model="ruleForm.newPass" type="password" autocomplete="off" />
          </el-form-item>
          <el-form-item label="重复密码" prop="checkPass" required>
            <el-input v-model="ruleForm.checkPass" type="password" autocomplete="off" />
          </el-form-item>
          
          <el-form-item>
            <el-button type="primary" @click="submitForm(ruleFormRef)">Submit</el-button>
            <el-button @click="resetForm(ruleFormRef)">Reset</el-button>
          </el-form-item>
        </el-form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { reactive, ref ,defineProps} from 'vue'
import { updatePassword } from '@/api/index.js';
import open from '@/utils/message';
const ruleFormRef = ref()
const props = defineProps(['getHideInformation','userName'])
const hideButton=()=>{
  //console.log(props)
  props.getHideInformation(false)

}

const checkOldPass = (rule , value, callback) => {
  if (!value) {
    return callback(new Error('请输入旧密码'))
  }else{
    callback()
  }
 
}

const validatePass = (rule , value , callback ) => {
  if (value === '') {
    callback(new Error('请输入新密码'))
  } 
  setTimeout(() => {
    
    if (!/^(?![\d]+$)(?![a-zA-Z]+$)(?![^\da-zA-Z]+$)([^\u4e00-\u9fa5\s]){6,20}$/.test(value)) {
    callback(new Error('请输入6-20位英文字母、数字或者符号（除空格），且字母、数字和标点符号至少包含两种'))
  } else {
    callback()
  }

  }, 1000)
}
const validatePass2 = (rule, value, callback) => {
  if (value === '') {
    callback(new Error('请重复新密码！'))
  } else if (value !== ruleForm.newPass) {
    callback(new Error("两个输入不匹配!"))
  } else {
    callback()
  }
}

const ruleForm = reactive({
  oldPass: '',
  newPass: '',
  checkPass: '',
})

const rules = reactive({
  oldPass: [{ validator: checkOldPass, trigger: 'blur' }],
  newPass: [{ validator: validatePass, trigger: 'blur' }],
  checkPass: [{ validator: validatePass2, trigger: 'blur' }],
})

const submitForm = (formEl) => {
  if (!formEl) return
  formEl.validate(async(valid) => {
    if (valid) {
      let role=localStorage.getItem('role')
      let result=await updatePassword(role,props.userName,ruleForm.oldPass,ruleForm.newPass)
      let code=result.data.code
      let message=result.data.message
      //console.log(code,message)
      if(code==200){
        open(message,'success')
      }else{
        open(message,'error')
      }

    } else {
      console.log('error submit!')
      return false
    }
  })
}


const resetForm = (formEl) => {
  if (!formEl) return
  formEl.resetFields()
}
</script>

<style lang="scss" scoped>
.overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5); /* 半透明黑色背景 */
  z-index: 1002; /* 确保在最上层 */
  display: flex;
  align-items: center;
  justify-content: center;
  .passwordUpdateBOx {
    width: 500px;
    height: 350px;
    background-color: #fff;
    .passwordTop {
      padding: 20px 20px 10px 20px;
      display: flex;
      justify-content: space-between;
      span:first-child {
        font-size: 20px;
      }
    }
    .passwordForm {
      padding: 30px 20px;
    }
    .el-form-item {
      margin-bottom: 35px;
    }
  }
}
</style>
