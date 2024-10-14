<template>
  <div style="padding: 10px 25px 40px 25px;width: 100%;height: 90%;">
    <el-table :data="filterTableData" :border="parentBorder" style="width: 100%;height: 100%;" >
      <el-table-column type="expand">
        <template #default="props">
          <div class="record">
            <div class="item">
              <h3>诊断</h3>
              <p>
                {{ props.row.treat_situation||'没有诊断情况' }}
              </p>
            </div>
            <div class="item">
              <h3>建议</h3>
              <p>
                {{ props.row.suggestion||'没有给与建议' }}
              </p>
            </div>
          </div>
        </template>
      </el-table-column>
      <el-table-column label="序号" prop="number" />
      <el-table-column label="名字" prop="name" />
      <el-table-column label="电话号码" prop="tel" />
      <el-table-column label="年龄" prop="birth" />
      <el-table-column label="地址" prop="address" />
      <el-table-column align="right">
        <template #header>
          <el-input v-model="search" size="small" placeholder="Type to search" />
        </template>
        <template #default="scope">
          <el-button size="small" type="danger" @click="treatPatient(scope.row)">诊断</el-button>
          <el-button size="small" type="danger" @click="goPatientTest(scope.row)"
            >测试情况</el-button
          >
        </template>
      </el-table-column>
    </el-table>
    <treat v-show="isShow" :getHide="getHide" :id="id"></treat>
  </div>
</template>

<script lang="ts" setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import treat from '@/components/treat.vue'
import { getMyPatient } from '@/api'
let router = useRouter()
const isShow = ref(false)
let id = ref('')
const parentBorder = ref(false)
const tableData = ref([])
const search = ref('')
const filterTableData = computed(() =>
  tableData.value.filter(
    (data) => !search.value || data.name.toLowerCase().includes(search.value.toLowerCase())
  )
)
const treatPatient = (data) => {
  isShow.value = true
  id.value = data.id
}
const getHide = (value) => {
  isShow.value = value
}
const getPatient = async () => {
  try {
    let result = await getMyPatient()
   // console.log(result)
    if (result.data.code == '200') {
      let data = result.data.data
      console.log(data)
      tableData.value = data.map((element, index) => {
        //console.log(element.birth)
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
  } catch (error) {
    console.log(error.message)
  }
}
const goPatientTest = (data) => {
  router.push({
    path: '/doctor/myPatient/evaluation',
    query: { id: data.id }
  })
}

onMounted(() => {
  getPatient()
})
</script>
<style lang="scss" scoped>
.record {
  width: 100%;
 height: auto;
 
  .item {
    padding: 10px 8px;
    h3 {
      height: 40px;
      line-height: 40px;
    }
    p {
      font-size: 14px;
      text-indent: 2em;
    }
  }
}
</style>
