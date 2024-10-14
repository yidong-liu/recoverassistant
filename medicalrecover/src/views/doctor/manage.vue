<template>
  <div class="manage">
    <el-table :data="filterTableData" setScrollTop="top" style="width: 100%; height: 90%">
      <el-table-column label="序号" prop="number" />
      <el-table-column label="名字" prop="name" />
      <el-table-column label="年龄" prop="birth" />
      <el-table-column label="地址" prop="address" />
      <el-table-column label="主治医师" prop="major_doctor" />
      <el-table-column align="right">
        <template #header>
          <el-input v-model="search" size="small" placeholder="Type to search" />
        </template>
        <template #default="scope">
          <el-button size="small" type="danger" @click="addPatient(scope.row)">添加</el-button>
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script setup>
import { computed, ref, onMounted } from 'vue'
import { getAllUsers, addMyPatient } from '@/api'
import open from '@/utils/message'
import { ElMessageBox } from 'element-plus'
const search = ref('')
let tableData = ref([])
const filterTableData = computed(() =>
  tableData.value.filter(
    (data) => !search.value || data.name.toLowerCase().includes(search.value.toLowerCase())
  )
)

const getMyAllUsers = async () => {
  let result = await getAllUsers()
  console.log(result)
  if (result.data.code == '200') {
    let data = result.data.data
    tableData.value = data.map((element, index) => {
      if (element.birth) {
        let date = new Date()
        let year = date.getFullYear()
        element.birth = year * 1 - element.birth.slice(0, 4) * 1
      }
      if (
        element.address_province &&
        element.address_city &&
        element.address_county &&
        element.address_detail
      ) {
        element.address =
          element.address_province +
          element.address_city +
          element.address_county +
          element.address_detail
      }
      element.number = index

      return element
    })

    tableData.value = data
  }
}
const openBox = (rowData) => {
  ElMessageBox.confirm('他已有主治医师，是否继续添加该病人？', 'Warning', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  })
    .then(async () => {
      let result = await addMyPatient(rowData.id * 1)
      if (result.data.code == '200') {
        open('添加成功', 'success')
      } else {
        open('出现错误，请重试')
      }
    })
    .catch(() => {
      open('取消添加', 'info')
    })
}
const addPatient = async (rowData) => {
  try {
    /* console.log(rowData.major_doctor)
    if (rowData?.major_doctor) {
      openBox(rowData)
    } else {
      let result = await addMyPatient(rowData.id * 1)
      if (result.data.code == '200') {
        open('添加成功', 'success')
      } else {
        open('出现错误，请重试')
      }
    } */
    let result = await addMyPatient(rowData.id * 1)
      if (result.data.code == '200') {
        open('添加成功', 'success')
      } else {
        open('出现错误，请重试')
      }
  } catch (error) {
    console.log(error.message)
    open('出现错误，请重试')
  }
}
onMounted(() => {
  getMyAllUsers()
})
</script>
<style scoped>
.manage {
  width: 100%;
  height: 100%;
  padding: 0 40px;
}
</style>
