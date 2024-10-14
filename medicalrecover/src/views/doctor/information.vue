<template>
  <div class="contentBox">
    <el-form :model="form" label-width="120px">
      <el-form-item label="姓名">
        <el-input v-model="form.name" />
      </el-form-item>
      <el-form-item label="联系方式">
        <el-input v-model="form.tel" />
      </el-form-item>
      <el-form-item label="医院">
        <el-input v-model="form.hospital" />
      </el-form-item>
      <el-form-item label="科室">
        <el-input v-model="form.department" />
      </el-form-item>
      <el-form-item label="职称">
        <el-input v-model="form.title" :disabled="true"/>
      </el-form-item>

      <el-form-item>
        <el-button type="primary" @click="onSubmit">创建</el-button>
        <el-button @click="cancelAll">取消</el-button>
      </el-form-item>
    </el-form>
  </div>
</template>

<script setup>
import { reactive, onMounted } from 'vue'

import open from '@/utils/message'
import { updateInformation } from '@/api/index'
import useStore from '@/stores'
const { mainStore } = useStore()
// do not use same name with ref
const form = reactive({
  tel: '',
  name: '',
  hospital: '',
  department: '',
  jobTitle: ''
})
const getInfo = async () => {
  try {
    let data = await mainStore.getInformation()
    //console.log(data)
    for (let key in form) {
      form[key] = data[key]
    }
  } catch (error) {
    console.log(error.message)
  }
}
onMounted(() => {
  getInfo()
})
const cancelAll = () => {
  //console.log(form)
  for (let item in form) {
    //console.log(item)
    form[item] = ''
  }
}
const onSubmit = async () => {
  try {
    let result = await updateInformation(form,'doctor')
    //console.log(result, result.data.code)
    if (result.data.code == 200) {
      open('更新成功', 'success')
    }
  } catch (error) {
    console.log(error.message)
  }
}
</script>
<style lang="scss" scoped>
.contentBox {
  padding: 45px 60px 20px 0;

  .el-form-item {
    font-size: 16px;
    margin-bottom: 45px;
    ::v-deep .el-select__wrapper {
      margin-bottom: 35px;
    }
  }
}
</style>
