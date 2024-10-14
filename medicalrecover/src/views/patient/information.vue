<template>
  <div class="contentBox">
    <el-form :model="form" label-width="120px">
      <el-form-item label="姓名">
        <el-input v-model="form.name" />
      </el-form-item>
      <el-form-item label="联系方式">
        <el-input v-model="form.tel" />
      </el-form-item>

      <div class="region">
        <span class="regionTitle">地址</span>
        <el-cascader
          :options="pcaTextArr"
          @change="handleChange"
          class="full-width"
          size="large"
          v-model="form.address"
          placeholder="请选择您所在的城市"
        />
      </div>

      <el-form-item label="详细地址">
        <el-input v-model="form.addressDetail" />
      </el-form-item>
      <el-form-item label="出生日期">
        <el-col :span="11">
          <el-date-picker
            v-model="form.birth"
            type="date"
            placeholder="Pick a date"
            style="width: 100%"
          />
        </el-col>
        <el-col :span="2" class="text-center">
          <span class="text-gray-500">-</span>
        </el-col>
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
import { pcaTextArr } from 'element-china-area-data'
import open from '@/utils/message'
import { updateInformation } from '@/api/index'
import useStore from '@/stores'
const { mainStore } = useStore()
// do not use same name with ref
const form = reactive({
  tel: '',
  name: '',
  addressProvince: '',
  addressCity: '',
  addressCounty: '',
  address: '',
  addressDetail: '',
  birth: ''
})
const getInfo = async () => {
  try {
    let data = await mainStore.getInformation()
    //console.log(data)
    for (let key in form) {
      form[key] = data[key]
    }
    form.address = [data.addressProvince, data.addressCity, data.addressCounty]
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
    let result = await updateInformation(form, 'user')
    //console.log(result,result.data.code)
    if (result.data.code == 200) {
      open('更新成功', 'success')
    }
  } catch (error) {
    console.log(error.message)
  }
}

const handleChange = (value) => {
  //console.log(form.address)
  form.addressProvince = value[0]
  form.addressCity = value[1]
  form.addressCounty = value[2]
}
</script>
<style lang="scss" scoped>
.contentBox {
  padding: 45px 60px 20px 0;
  .region {
    padding-left: 80px;
    margin-bottom: 35px;
    .regionTitle {
      padding-right: 12px;
    }
  }
  .el-form-item {
    font-size: 16px;
    margin-bottom: 30px;
    ::v-deep .el-select__wrapper {
      margin-bottom: 35px;
    }
  }
}
</style>
