<template>
  <table class="situation">
    <tr>
      <td><span class="label">姓名:</span> {{ data.name }}</td>
      <td><span class="label">年龄:</span> {{ age }}</td>
    </tr>

    <tr>
      <td colspan="5" class="label" style="vertical-align: top">
        疾病诊治情况:
        <ol class="details">
          {{
            treat
          }}
        </ol>
      </td>
    </tr>
    <tr>
      <td colspan="5" class="label" style="vertical-align: top">
        建议意见:
        <ol class="details">
          {{
            suggestion
          }}
        </ol>
      </td>
    </tr>
    <tr>
      <td style="border: none; text-align: right; padding-right: 50px" colspan="5" class="label">
        <span class="label">主治医师:{{ doctor }}</span>
      </td>
    </tr>
  </table>
</template>

<script setup>
import useStore from '@/stores'
const { mainStore } = useStore()
import { getSituations, getSuggestion } from '@/api'
import { onMounted, ref, computed } from 'vue'
let data = ref({})
let suggestion = ref('')
let treat = ref('')
let doctor = ref('')
const getInfo = async () => {
  data.value = await mainStore.getInformation()
 
}
const getMySituations = async () => {
  try {
    let result = await getSituations()
    console.log(result)
    if (result.data.code == '200') {
      treat.value = result.data.data[0].situation
      doctor.value = result.data.data[0].doctor
    } else if (result.data.code == '500') {
      treat.value = '您当前没有诊断情况！'
      doctor.value = '空'
    }
  } catch (error) {
    console.log(error.message)
  }
}
const getMySuggestion = async () => {
  try {
    let result = await getSuggestion()
    //console.log(result)
    if (result.data.code == '200') {
      suggestion.value = result.data.data[0].suggestion
    } else if (result.data.code == '500') {
      suggestion.value = '医生当前没有给与建议！'
    }
  } catch (error) {
    console.log(error.message)
  }
}
let age = computed(() => {
  let date = new Date()
  let year = date.getFullYear()
  return year - data.value.birth?.substr(0, 4)
})
onMounted(() => {
  getInfo()
  getMySituations()
  getMySuggestion()
})
</script>
<style lang="scss" scoped>
/* 设置中间两个<tr>占据剩余空间 */
table.situation tr:nth-child(2),
table.situation tr:nth-child(3) {
  height: calc((100% - 100px) / 2); /* 计算剩余空间并分配给两个<tr> */
}

.situation {
  border-collapse: collapse;
  width: 100%;
  height: calc(100vh - 50px);
  tr:first-child,
  tr:last-child {
    height: 50px; /* 设置高度 */
  }
  tr:nth-child(2),
  tr:nth-child(3) {
    height: calc((100% - 100px) / 2); /* 计算剩余空间并分配给两个<tr> */
  }
  td,
  th {
    border: 1px solid #ddd;
    padding: 12px; // 增加内边距
    text-align: left;
  }

  tr:nth-child(even) {
    background-color: #f2f2f2;
  }

  tr:hover {
    background-color: #ddd;
  }

  .label {
    font-weight: bold;
  }

  .details {
    margin-top: 16px; // 上方边距
    padding-left: 20px;

    li {
      list-style-type: decimal;
      margin-bottom: 30px;

      &:last-child {
        margin-bottom: 0;
      }
    }
  }
}
</style>
