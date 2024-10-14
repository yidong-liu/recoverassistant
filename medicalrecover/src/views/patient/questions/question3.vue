<template>
  <div class="question3Box">
    <h2 class="title">记忆力</h2>
    <div class="content">
      <h3>根据语音提示建记住图片物品，并选择图片中物体名称</h3>
      <div class="questions">
        <div class="demo-image">
          <img src="@/assets/images/apple.png" alt="苹果" />
          <div>
            <audio controls>
              <source src="../../../../public/audio/ttsmaker-苹果.mp3" type="audio/mp3" />
              Your browser does not support the audio element.
            </audio>
          </div>

          <div class="buttonSelect">
            <button
              v-for="([option, value], index) in fruitsData"
              :key="index"
              @click="getFruits"
              :class="{ active: fruitsShow == `${option}` }"
            >
              <span>{{ option }}</span
              >{{ value }}
            </button>
          </div>
        </div>
        <div class="demo-image">
          <img src="@/assets/images/Paper.jpeg" alt="报纸" />
          <div>
            <audio controls>
              <source src="../../../../public/audio/ttsmaker-报纸.mp3" type="audio/mp3" />
              Your browser does not support the audio element.
            </audio>
          </div>

          <div class="buttonSelect">
            <button
              v-for="([option, value], index) in paperData"
              :key="index"
              @click="getPaper"
              :class="{ active: paperShow == `${option}` }"
            >
              <span>{{ option }}</span
              >{{ value }}
            </button>
          </div>
        </div>
        <div class="demo-image">
          <img src="@/assets/images/Train.jpeg" alt="火车" />
          <div>
            <audio controls>
              <source src="../../../../public/audio/ttsmaker-火车.mp3" type="audio/mp3" />
              Your browser does not support the audio element.
            </audio>
          </div>
          <div class="buttonSelect">
            <button
              v-for="([option, value], index) in trainData"
              :key="index"
              @click="getTrain"
              :class="{ active: trainShow == `${option}` }"
            >
              <span>{{ option }}</span
              >{{ value }}
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import useStore from '@/stores/index'
const { mmse } = useStore()
const fruitsShow = ref(sessionStorage.getItem('fruits') || '')
const fruitsData = reactive([
  ['A', '苹果'],
  ['B', '香蕉']
])
const getFruits = (e) => {
  let fruits = /\w/.exec(e.target.innerText)[0]
  fruitsShow.value = fruits
  mmse.setFruits(fruits)
}

const paperShow = ref(sessionStorage.getItem('paper') || '')
const paperData = reactive([
  ['A', '报纸'],
  ['B', '地图']
])
const getPaper = (e) => {
  let paper = /\w/.exec(e.target.innerText)[0]
  paperShow.value = paper
  mmse.setPaper(paper)
}

const trainShow = ref(sessionStorage.getItem('train') || '')
const trainData = reactive([
  ['A', '火车'],
  ['B', '高铁']
])
const getTrain = (e) => {
  let train = /\w/.exec(e.target.innerText)[0]
  trainShow.value = train
  mmse.setTrain(train)
}
</script>

<style lang="scss" scoped>
.question3Box {
  margin-left: 150px;

  height: 490px;
  .title {
    margin-bottom: 40px;
  }
  .content {
    h3 {
      margin-bottom: 30px;
    }
    .questions {
      display: flex;
      justify-content: space-between;
      .demo-image {
        img {
          box-shadow: 0 4px 8px rgba(22, 22, 22, 0.1);
          width: 200px;
          height: 200px;
        }
        audio {
          width: 200px;
          margin-bottom: 30px;
          margin-top: 10px;
        }

        .buttonSelect {
          padding-left: 16px;

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
  }
}
</style>
