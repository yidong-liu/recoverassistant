<template>
  <div class="overlay">
    <div class="history">
      <div class="top">
        <span @click="hideHistory">❌</span>
        <el-button type="info" plain @click="exportData">导出数据</el-button>
      </div>
      <el-table
        :data="data"
        :default-sort="{ prop: 'score', order: 'descending' }"
        style="width: 100%; height: calc(100% - 48px)"
      >
        <el-table-column prop="time" label="日期" sortable width="300" />
        <el-table-column prop="score" label="分数" sortable width="200" />
        <el-table-column prop="type" label="考试类别" width="200" />
        <el-button type="primary" />
      </el-table>
    </div>
  </div>
</template>

<script setup>
import { defineProps, onMounted, ref } from 'vue'
const props = defineProps(['getHistoryShow'])
import { getHistory, getPatientTestScore } from '@/api'
import open from '@/utils/message'
import { useRoute } from 'vue-router'
let route = useRoute()
import * as XLSX from 'xlsx'
import { saveAs } from 'file-saver'
const hideHistory = () => {
  props.getHistoryShow(false)
}

let data = ref([])
const getHistoryScore = async () => {
  try {
    //console.log(route.query.id)
    let role = localStorage.getItem('role')
    //console.log(role)
    let result
    if (role == 'doctor') {
      result = await getPatientTestScore(route.query.id)
    } else if (role == 'user') {
      result = await getHistory()
    }
    //console.log(result.data)
    let code = result.data.code
    let getData = result.data.data
    if (getData.length == 0) {
      emptyData()
    }
    if (code == '200') {
      data.value = getData.map((item) => {
        item.type = 'MMSE测试'
        return item
      })

      //console.log(optionData.value)
    } else {
      open('获取数据失败，请刷新', 'success')
    }
  } catch (error) {
    console.log(error.message)
  }
}
const exportData = async () => {
  try {
    // 创建工作簿
    const workbook = XLSX.utils.book_new()
    const worksheet = XLSX.utils.json_to_sheet(data.value)

    // 设置每列宽度
    const colWidths = []
    data.value.forEach((row) => {
      Object.keys(row).forEach((key, index) => {
        const cellContent = row[key] + '' // 转换为字符串
        const cellWidth = cellContent.length * 2 // 这里的 1.5 是一个简单的估计，根据具体内容调整
        if (!colWidths[index] || colWidths[index] < cellWidth) {
          colWidths[index] = cellWidth
        }
      })
    })
    // 设置每列宽度
    worksheet['!cols'] = colWidths.map((width) => ({ width }))

    // 添加工作表到工作簿
    XLSX.utils.book_append_sheet(workbook, worksheet, 'Sheet1')

    // 添加边框
    const range = XLSX.utils.decode_range(worksheet['!ref'])
    for (let R = range.s.r; R <= range.e.r; ++R) {
      for (let C = range.s.c; C <= range.e.c; ++C) {
        const cellAddress = { c: C, r: R }
        const cellRef = XLSX.utils.encode_cell(cellAddress) // 获取单元格引用
        const cell = worksheet[cellRef]
        if (cell) {
          if (!cell.s) cell.s = {} // 如果单元格没有样式，创建一个空样式对象
          cell.s.border = {
            // 设置边框
            top: { style: 'thin' },
            bottom: { style: 'thin' },
            left: { style: 'thin' },
            right: { style: 'thin' }
          }
        }
      }
    }

    // 将工作簿转换为Excel文件的二进制对象
    const excelBuffer = XLSX.write(workbook, { bookType: 'xlsx', type: 'array' })

    // 将二进制对象转换为Blob
    const blob = new Blob([excelBuffer], { type: 'application/octet-stream' })

    // 使用 file-saver 库保存Blob为Excel文件
    saveAs(blob, 'data.xlsx')
  } catch (error) {
    console.log(error.message)
  }
}

onMounted(() => {
  getHistoryScore()
})
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

  .history {
    width: 50%;
    height: 70%;
    background-color: #fff;
    padding: 20px 8px 20px;
    .top {
      padding: 8px 40px 8px 10px;
      display: flex;
      justify-content: space-between;
    }
  }
}
</style>
