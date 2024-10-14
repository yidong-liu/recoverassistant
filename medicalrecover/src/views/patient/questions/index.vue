<template>
  <div class="testBox">
    <div class="bar">
      <h1 class="title">MMSE测试</h1>
      <el-button type="info" @click="finishiCheck">交卷</el-button>
    </div>
    <div class="main">
      <leftDirect></leftDirect>
      <div class="rightAnswerBox">
        <RouterView></RouterView>
        <div class="direction">
          <el-button-group>
            <el-button type="primary" color="#626aef" @click="goPreviousPage">上一页</el-button>
            <el-button type="primary" color="#626aef" @click="goNextPage"> 下一页 </el-button>
          </el-button-group>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useRouter, useRoute } from 'vue-router'
import leftDirect from './leftDirect.vue'
import { ElMessageBox } from 'element-plus'
import open from '@/utils/message'
import useStore from '@/stores'
import { keepScore } from '@/api'
const { mmse } = useStore()
const router = useRouter()
const route = useRoute()
let goNextPage = () => {
  let path = route.path
  let number = /question(\d+)/.exec(path)[1] * 1

  number++
  if (number > 10) {
    number = 10
    open('当前为最后一题', 'warning')
  }
  router.replace({
    path: `/mmse/questions/question${number}`
  })
}
let goPreviousPage = () => {
  let path = route.path
  let number = /question(\d+)/.exec(path)[1] * 1
  number--
  if (number < 1) {
    number = 1
    open('当前为第一题', 'warning')
  }
  router.replace({
    path: `/mmse/questions/question${number}`
  })
}
let finishiCheck = () => {
  ElMessageBox.confirm('确定交卷 ？', 'Warning', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  })
    .then(async () => {
      let score = await mmse.getMyScore()
      //console.log(score)
      let result = await keepScore(score)

      //console.log(result)
      if (result.data.code == 200) {
        open(`本次测试分数${score}`, 'success')
        router.replace({
          path: '/patient/mmse'
        })
        sessionStorage.clear()
        mmse.reset()
      } else {
        open('欧欧，出现了一点错误，请重新尝试')
      }
    })
    .catch((error) => {
      open('取消交卷', 'info')
    })
}
</script>

<style lang="scss" scoped>
.testBox {
  width: 1200px;
  margin: auto;
  height: 100vh;
  overflow: hidden;
  .bar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    border-bottom: 3px solid gray;
    margin-bottom: 50px;
    padding: 20px 0;
    .title {
      font-size: 20px;
      font-family: 'Trebuchet MS', 'Lucida Sans Unicode', 'Lucida Grande', 'Lucida Sans', Arial,
        sans-serif;
      font-weight: bolder;
      color: black;

      background-color: #fff;
    }
  }
  .main {
    height: calc(100% - 97px);
    display: flex;
    width: 100%;
    overflow: hidden;
    .rightAnswerBox {
      height: 100%;
      width: 100%;
      overflow: auto;
      .direction {
        margin-top: 8px;
        float: right;
      }
    }
  }
}
</style>
