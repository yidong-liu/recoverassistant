<template>
  <div class="direct">
  
    <div class="progress">
      <div class="progressTop">
        <span>答题进度</span>
        <span
          ><span style="color: rgb(44, 44, 149)">{{ questionNumber }}</span
          >/10</span
        >
      </div>
      <el-progress
        :percentage="percentage"
        :stroke-width="15"
        status="success"
        striped
        striped-flow
        :duration="10"
      />
      <p>
        共<span style="color: rgb(44, 44, 182)">10</span>题；满分<span style="color: orange">100</span
        >分
      </p>
    </div>
    <div class="table">
      <table @click="changeQuestionNumber">
        <tr>
          <td>1</td>
          <td>2</td>
          <td>3</td>
        </tr>
        <tr>
          <td>4</td>
          <td>5</td>
          <td>6</td>
        </tr>
        <tr>
          <td>7</td>
          <td>8</td>
          <td>9</td>
        </tr>
        <tr>
          <td>10</td>
        
        </tr>
      </table>
    </div>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'
import { useRouter, useRoute } from 'vue-router'
let questionNumber = ref(sessionStorage.getItem('currentQuestion')||1)
let router = useRouter()
let route = useRoute()
const percentage = ref(sessionStorage.getItem('currentPercentage')*1||10)
const changeQuestionNumber = (e) => {
  //console.log(e.target.innerText)
  questionNumber.value = e.target.innerText * 1

  if (!isNaN(questionNumber.value)) {
    router.replace({
      path: `/mmse/questions/question${questionNumber.value}`
    })
    
  }
}
// 使用 watch 监听路由变化
watch(
  () => route.path,
  (newPath) => {
    let number = /question(\d+)/.exec(newPath)[1]*1
    sessionStorage.setItem('currentQuestion',number)
    questionNumber.value = number
    percentage.value = questionNumber.value * 10
    sessionStorage.setItem('currentPercentage',percentage.value)

  }
)
</script>

<style lang="scss" >
.direct {
  width: 250px;
  height: 100%;
  
 
  .progress {
    padding: 0px 20px 0 8px;
    border-bottom: 1px solid darkgray;
    .progressTop {
      display: flex;
      justify-content: space-between;
      margin-bottom: 5px;
    }
    .el-progress {
      padding: 5px 0;
      width: 100%;
      
    }
    ::deep .el-progress__text {
        min-width: 0;
    }
    p {
      letter-spacing: 1px;
      margin-bottom: 40px;
    }
  }
  .table {
    padding-left: 8px;
    padding-top: 5px;
    margin-left: -25px;
    cursor: pointer;
    table {
      border-collapse: collapse;
      width: 100%;

    }

    td {
      width: 70px;
      padding: 8px 0;
      text-align: center;
      color: green;
    }
    td:hover {
      background: linear-gradient(to right, #3498db, #ffffff);
    }
  }
}
</style>
