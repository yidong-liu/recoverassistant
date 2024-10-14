<template>
  <div class="question8Box">
    <h2>仿写</h2>
    <div class="textBox">
      <h3>
        请仿照下方的句子 在右边方框内 输入一句完整的句子 注意以句号或问号结束
        <span style="color: red; font-size: 20px">例如：我想吃西瓜。</span>
      </h3>
      <textarea cols="80" rows="17" v-model="answer8"  placeholder="请输入" @input="getAnswer8">

      </textarea>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import useStore from '@/stores/index'
const { mmse } = useStore()
const textarea = ref('')
const answer8 = ref(sessionStorage.getItem('answer8')||'')
const getAnswer8 = () => {
  mmse.setQuestion8(answer8.value)
}
</script>

<style lang="scss" scoped>

.question8Box {
  

  margin-left: 150px;
 
  height: 490px;
  
  h2 {
    margin-bottom: 40px;
    
  }
  .textBox{
    

      h3 {
        margin-bottom: 25px;
      }
      textarea{
        padding: 5px 10px;
        border-color: greenyellow;
        font-size: 16px;
      }
     
      
      
    
       
    
    
  }
}
</style>
