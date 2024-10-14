<template>
  <div class="question6Box">
    <h2>回忆力</h2>
    <div class="questions">
      <h3>刚刚你记住的三张图是 ? (请选择三个选项)</h3>
      <el-checkbox-group v-model="checkedItems" :min="0" :max="3" @change="getQuestion6">
        <el-checkbox v-for="item in items" :key="item" :label="item">{{ item }}</el-checkbox>
      </el-checkbox-group>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import useStore from '@/stores/index';
const {mmse} =useStore()
const checkedItems = ref(JSON.parse(sessionStorage.getItem('answer6'))||[])
const items = [
  '苹果(Apple)',
  '香蕉(Banana)',
  '橙子(Orange)',
  '狗(Dog)',
  '大象(Elephant)',
  '樱桃(Cherry)',
  '梨(Pear)',
  '胡萝卜(Carrot)',
  '火车(train)',
  '熊(Bear)',
  '狮子(Lion)',
  '茄子(Eggplant)',
  '报纸(paper)',
  '南瓜(Pumpkin)',
  '菠菜(Spinach)',
  '青椒(Bell Pepper)',
  '生菜(Lettuce)',
  '沙发(Sofa)',
  '床(Bed)',
  '椅子(Chair)',
  '书架(Bookshelf)',
  '衣柜(Wardrobe)'

]
const getQuestion6=()=>{
  mmse.setQuestion6(checkedItems.value)
}
</script>

<style lang="scss" scoped>
.question6Box {
  margin-left: 200px;
  height: 490px;

  h2 {
    margin-bottom: 40px;
  }
  .questions {
    h3 {
      margin-bottom: 30px;
    }
    .el-checkbox{
      margin-bottom: 15px;
    }
  }
}
</style>
