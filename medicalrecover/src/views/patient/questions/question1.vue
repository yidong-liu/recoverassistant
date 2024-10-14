<template>
  <div class="question1Box">
    <h2 class="title">时间判断</h2>
    <div class="questions">
      <div>
        <h3>今年是哪一年 ？</h3>
        <div class="buttonSelect">
          <button
            v-for="([option, value], index) in yearData"
            :key="index"
            @click="getYear"
            :class="{ active: yearShow==`${option}` }"
          >
            <span>{{ option }}</span
            >{{ value }}
          </button>
        </div>
      </div>
      <div>
        <h3>当前季节 ?</h3>
        <div class="buttonSelect">
          <button
            v-for="([option, value], index) in seasonData"
            :key="index"
            @click="getSeason"
            :class="{ active: seasonShow==`${option}` }"
          >
            <span>{{ option }}</span
            >{{ value }}
          </button>
        </div>
      </div>

      <div>
        <h3>当前月份 ？</h3>
        <el-select
          v-model="month"
          class="m-2"
          placeholder="选择月份"
          size="large"
          style="width: 240px"
          @change="getMonth"
        >
          <el-option
            v-for="item in monthes"
            :key="item.value"
            :label="item.label"
            :value="item.value"
          />
        </el-select>
      </div>
      <div>
        <h3>今天几号 ？</h3>
        <el-select
          v-model="day"
          class="m-2"
          placeholder="选择日期"
          size="large"
          style="width: 240px"
          @change="getDay"
        >
          <el-option
            v-for="item in days"
            :key="item.value"
            :label="item.label"
            :value="item.value"
          />
        </el-select>
      </div>
      <div>
        <h3>今天星期几 ？</h3>
        <el-select
          v-model="week"
          class="m-2"
          placeholder="选择星期几"
          size="large"
          style="width: 240px"
          @change="getWeek"
        >
          <el-option
            v-for="item in weeks"
            :key="item.value"
            :label="item.label"
            :value="item.value"
          />
        </el-select>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onBeforeMount, computed, reactive } from 'vue'
import useStore from '@/stores/index'
const { mmse } = useStore()
const month = ref(sessionStorage.getItem('month') || '')
const monthes = []
const day = ref(sessionStorage.getItem('day') || '')
const days = []
const week = ref(sessionStorage.getItem('week') || '')
const weeks = []

const currentYear = computed(() => {
  const currentDate = new Date()
  const currentYear = currentDate.getFullYear()
  return currentYear
})

const yearShow = ref(sessionStorage.getItem('year') || '')
const yearData = reactive([
  ['A', currentYear.value - 1],
  ['B', currentYear.value + 1],
  ['C', currentYear.value],
  ['D', 2021]
])

onBeforeMount(() => {
  for (let i = 1; i <= 12; i++) {
    monthes.push({
      value: `${i}月`,
      label: `${i}月`
    })
  }
  for (let i = 1; i <= 31; i++) {
    days.push({
      value: `${i}号`,
      label: `${i}号`
    })
  }
  for (let i = 1; i <= 7; i++) {
    weeks.push({
      value: `星期${i}`,
      label: `星期${i}`
    })
  }
})

const getYear = (e) => {
  let year = /\w/.exec(e.target.innerText)[0]
  //console.log(e.target.innerText,year)
  //e.target.style='background-color:rgb(103, 194, 58)'
  yearShow.value=year
  mmse.setYear(year)
}

const seasonShow = ref(sessionStorage.getItem('season') || '')
const seasonData = reactive([
  ['A', '春天'],
  ['B', '夏天'],
  ['C', '秋天'],
  ['D', '冬天']
])

const getSeason = (e) => {
  let season = /\w/.exec(e.target.innerText)[0]
  //console.log(season)
  seasonShow.value=season
  mmse.setSeason(season)
}
const getMonth = () => {
  mmse.setMonth(month.value)
}
const getDay = () => {
  mmse.setDay(day.value)
}
const getWeek = () => {
  mmse.setWeek(week.value)
}
</script>

<style lang="scss" scoped>
.question1Box {
  margin-left: 150px;
  height: 490px;

  .title {
    margin-bottom: 40px;
  }
  .questions {
    > div {
      margin-bottom: 60px;

      display: inline-block;
      width: 50%;

      h3 {
        margin-bottom: 15px;
      }
      :last-child {
        margin: 0;
      }
    }
    .buttonSelect {
      border: 1px sold rgb(203, 248, 182);
      border-radius: 5px;
      

      button {
        background-color: rgb(170, 235, 136);
        padding: 6px 15px;
        font-size: 14px;
        color: #fff;
        span {
          margin-right: 10px;
        }
      }
      button.active {
        background-color: rgb(103, 194, 58);
      }
    }
  }
}
</style>
