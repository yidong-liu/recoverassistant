<template>
  <div class="evaluationBox">
    <div class="leftEchart">
      <div class="top">
        <span>测试数据折线图</span>
      </div>
      <div id="lert" class="echartInstance"></div>
    </div>
    <div class="rightEchart">
      <div class="top">
        <span> 测试数据分数统计图 </span>
        <el-button key="primary" type="primary" text @click="showHistory">历史测试</el-button>
      </div>
      <div id="rert" class="echartInstance"></div>
    </div>
  </div>

  <historyStastics v-if="isShowHistory" :getHistoryShow="getHistoryShow"></historyStastics>
</template>

<script setup>
import initEchart from '@/utils/initEchart'
import historyStastics from '@/components/historyStastics.vue'
import { onMounted, reactive, onBeforeUnmount, ref, watch } from 'vue'
import { getHistory, getPatientTestScore } from '@/api'
import open from '@/utils/message'
import { ElMessageBox } from 'element-plus'
import { useRouter, useRoute } from 'vue-router'
let myChart1, myChart2
let isShowHistory = ref(false)
let optionData = ref([])
let router = useRouter()
let route = useRoute()
let option1 = reactive({
  xAxis: {
    type: 'category',
    data: []
  },
  yAxis: {
    type: 'value'
  },
  tooltip: {
    trigger: 'axis'
  },
  series: [
    {
      data: [],
      type: 'line'
    }
  ]
})
// 监听data的变化，更新option1中的xAxis和series的data
watch(
  () => optionData.value,
  (newData) => {
    let data = newData.slice(-7)
    myChart1.setOption({
      series: [
        {
          data: data.map((item) => item.score),
          type: 'line'
        }
      ],
      xAxis: {
        data: data.map((item) => item.time)
      }
    })
    let option2Data = [
      {
        value: 0,
        name: '60以下'
      },
      {
        value: 0,
        name: '60-70'
      },
      {
        value: 0,
        name: '70-80'
      },
      {
        value: 0,
        name: '80-90'
      },
      {
        value: 0,
        name: '90-100'
      }
    ]
    newData.forEach((item) => {
      if (item.score >= 0 && item.score < 60) {
        option2Data[0].value++
      } else if (item.score >= 60 && item.score < 70) {
        option2Data[1].value++
      } else if (item.score >= 70 && item.score < 80) {
        option2Data[2].value++
      } else if (item.score >= 80 && item.score < 90) {
        option2Data[3].value++
      } else if (item.score >= 90 && item.score <= 100) {
        option2Data[4].value++
      }
    })
    myChart2.setOption({
      series: [
        {
          data: option2Data
        }
      ]
    })
  }
)
let option2 = reactive({
  tooltip: {
    trigger: 'item', // 鼠标悬浮时触发
    formatter: '{b}分: {c}次 占比{d}%' // 提示信息格式
  },
  series: [
    {
      type: 'pie',
      roseType: 'area'
    }
  ]
})
const emptyData = (msg,route) => {
  ElMessageBox.alert(`${msg}`, {
    confirmButtonText: '好的',
    callback: () => {
      router.replace({
        path: `${route}`
      })
    }
  })
}
const getHistoryScore = async () => {
  try {
    let role = localStorage.getItem('role')

    let result
    if (role == 'doctor') {
      result = await getPatientTestScore(route.query.id)
    } else if (role == 'user') {
      result = await getHistory()
    }

    let code = result.data.code
    let getData = result.data.data

    if (getData.length == 0) {
      if (role == 'doctor') {
        emptyData('此患者并未有测试数据','/doctor/myPatient')
      } else if (role == 'user') {
        emptyData('你并未有测试数据，请先前往测试','/patient/mmse')
      }
    }

    if (code == '200') {
      optionData.value = getData
    } else {
      open('获取数据失败，请刷新', 'success')
    }
  } catch (error) {
    console.log(error.message)
  }
}

onMounted(() => {
  getHistoryScore()
  myChart1 = initEchart('lert', option1)
  myChart2 = initEchart('rert', option2)
})

const showHistory = () => {
  isShowHistory.value = true
}
const getHistoryShow = (hide) => {
  isShowHistory.value = hide
}
</script>

<style lang="scss" scoped>
.evaluationBox {
  overflow: hidden;
  width: 100%;
  height: calc(100% - 50px);
  background-color: rgb(250, 254, 255);
  .leftEchart,
  .rightEchart {
    display: inline-block;
    width: 50%;

    padding: 25px 50px;
    height: 100%;
    .top {
      padding: 10px 8px 20px 16px;
      border-bottom: 5px solid rgb(199, 197, 197);
      display: flex;
      justify-content: space-between;
      align-items: center;
      span {
        font-size: 20px;
      }
      .el-button {
        font-size: 20px;
      }
    }
    #rert,
    #lert {
      width: 100%;
      height: 100%;
      padding: 16px 8px;
    }
  }
}
</style>
