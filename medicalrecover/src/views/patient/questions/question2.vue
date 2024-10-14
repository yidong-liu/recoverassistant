<template>
  <div class="question2Box">
    <h2 class="title">地点判断</h2>
    <div class="questions">
      <div class="region">
        <h3>请选择你当前所在地址</h3>
        <span style="padding-right: 8px;">地址</span>
        <el-cascader
          :options="pcaTextArr"
          @change="handleChange"
          class="full-width"
          size="large"
          v-model="region"
          placeholder="请选择您所在的城市"
        />
      </div>
      <div>
        <h3>当前所在医院 ？</h3>
        <div class="buttonSelect">
            <div class="buttonSelect">
              <button
                v-for="([option, value], index) in hospitalData"
                :key="index"
                @click="getHospital"
                :class="{ active: hospitalShow == `${option}` }"
              >
                <span>{{ option }}</span
                >{{ value }}
              </button>
            </div>
    
        </div>
      </div>
      <div>
        <h3>请选择当前所在楼层</h3>
        <el-select
          v-model="floor"
          class="m-2"
          placeholder="选择楼层"
          size="large"
          style="width: 240px"
          @change="getFloor"
        >
          <el-option
            v-for="item in floors"
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
import { ref, onBeforeMount, reactive } from 'vue'
import {  pcaTextArr } from 'element-china-area-data'
import useStore from '@/stores/index'
const { mmse } = useStore()

const floors = []
onBeforeMount(() => {
  for (let i = 1; i <= 25; i++) {
    floors.push({
      value: `第${i}楼`,
      label: `第${i}楼`
    })
  }
})

let region = ref(JSON.parse(sessionStorage.getItem('region'))||[])
const handleChange = (value) => {
  //console.log(value)
  mmse.setRegion(value)

}

const hospitalShow = ref(sessionStorage.getItem('hospital') || '')
const hospitalData = reactive([
  ['A', '湘雅附属第一医院'],
  ['B', '长沙市第一医院'],
  ['C', '南华医院'],
  ['D', '湘雅附属第二医院']
])
const getHospital = (e) => {
  let hospital = /\w/.exec(e.target.innerText)[0]
  hospitalShow.value=hospital
  mmse.setHospital(hospital)
}
const floor = ref(sessionStorage.getItem('floor')||'')
const getFloor = () => {
  mmse.setFloor(floor.value)
}

</script>

<style lang="scss" scoped>
.question2Box {
  height: 490px;
  margin-left: 150px;
  width: 100%;

  .title {
    margin-bottom: 40px;
  }
  .questions {
    > div {
      margin-bottom: 60px;

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
