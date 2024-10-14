<template>
  <div class="question1Box">
    <h2 class="title">计算力</h2>
    <div class="questions">
      <div>
        <h3>20 + 5= ?</h3>
        <div class="buttonSelect">
          <button
            v-for="([option, value], index) in calculation1Data"
            :key="index"
            @click="getCalculation1"
            :class="{ active: calculation1Show == `${option}` }"
          >
            <span>{{ option }}</span
            >{{ value }}
          </button>
        </div>
      </div>
      <div>
        <h3>100 - 7 ?</h3>
        <div class="buttonSelect">
          <button
            v-for="([option, value], index) in calculation2Data"
            :key="index"
            @click="getCalculation2"
            :class="{ active: calculation2Show == `${option}` }"
          >
            <span>{{ option }}</span
            >{{ value }}
          </button>
        </div>
      </div>
      <div>
        <h3>3 * 4 ?</h3>
        <div class="buttonSelect">
          <button
            v-for="([option, value], index) in calculation3Data"
            :key="index"
            @click="getCalculation3"
            :class="{ active: calculation3Show == `${option}` }"
          >
            <span>{{ option }}</span
            >{{ value }}
          </button>
        </div>
      </div>
      <div>
        <h3>20 / 5 ?</h3>
        <div class="buttonSelect">
          <button
            v-for="([option, value], index) in calculation4Data"
            :key="index"
            @click="getCalculation4"
            :class="{ active: calculation4Show == `${option}` }"
          >
            <span>{{ option }}</span
            >{{ value }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import useStore from '@/stores/index'
const { mmse } = useStore()
const calculation1Show = ref(sessionStorage.getItem('calculation1') || '')
const calculation1Data = reactive([
  ['A', '21'],
  ['B', '25'],
  ['C', '22'],
  ['D', '23']
])
const getCalculation1 = (e) => {
  let calculation1 = /\w/.exec(e.target.innerText)[0]
  calculation1Show.value = calculation1
  mmse.setCalculation1(calculation1)
}


const calculation2Show = ref(sessionStorage.getItem('calculation2') || '')
const calculation2Data = reactive([
  ['A', '93'],
  ['B', '100'],
  ['C', '86'],
  ['D', '95']
])
const getCalculation2 = (e) => {
  let calculation2 = /\w/.exec(e.target.innerText)[0]
  calculation2Show.value = calculation2
  mmse.setCalculation2(calculation2)
}


const calculation3Show = ref(sessionStorage.getItem('calculation3') || '')
const calculation3Data = reactive([
  ['A', '12'],
  ['B', '15'],
  ['C', '24'],
  ['D', '10']
])

const getCalculation3 = (e) => {
  let calculation3 = /\w/.exec(e.target.innerText)[0]
  calculation3Show.value = calculation3
  mmse.setCalculation3(calculation3)
}
const calculation4Show = ref(sessionStorage.getItem('calculation4') || '')
const calculation4Data = reactive([
  ['A', '6'],
  ['B', '3'],
  ['C', '2'],
  ['D', '4']
])

const getCalculation4 = (e) => {
  let calculation4 = /\w/.exec(e.target.innerText)[0]
  calculation4Show.value = calculation4
  mmse.setCalculation4(calculation4)
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
      margin-bottom: 100px;

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
      width: 327px;

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
