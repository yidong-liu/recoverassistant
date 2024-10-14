<template>
  <div class="question3Box">
    <h2 class="title">命名</h2>
    <div class="content">
      <h3>下面的三张图片分别是什么东西?请在输入框中打出它的名字</h3>
      <div class="questions">
        <div class="demo-image">
          <img src="@/assets/images/satellite.webp" alt="苹果" />
          <el-input v-model="answer7.input1" placeholder="请输入它的名称" @input="getAnswer7" />
        </div>
        <div class="demo-image">
          <img src="@/assets/images/plane.png" alt="报纸" />
          <el-input v-model="answer7.input2" placeholder="请输入它的名称" @input="getAnswer7" />
        </div>
        <div class="demo-image">
          <img src="@/assets/images/rocket.png" alt="火车" />
          <el-input v-model="answer7.input3" placeholder="请输入它的名称" @input="getAnswer7" />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import useStore from '@/stores/index'
const { mmse } = useStore()
const answer7 = ref(JSON.parse(sessionStorage.getItem('answer7'))||{
  input1: '',
  input2: '',
  input3: ''
})
const getAnswer7 = () => {
  mmse.setQuestion7(answer7.value)
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
        padding: 0 8px;
        img {
          box-shadow: 0 4px 8px rgba(22, 22, 22, 0.1);
          width: 200px;
          height: 200px;
          margin-bottom: 15px;
        }
        .el-input{
          width: 200px;
        }
      }
    }
  }
}
</style>
