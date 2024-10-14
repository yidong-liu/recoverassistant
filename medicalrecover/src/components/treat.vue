<template>
  <div class="overlay">
    <div class="treatUpdateBOx">
      <div class="treatTop">
        <span>诊断</span>
        <span @click="hideButton">❌</span>
      </div>
      <div class="treatForm">
        <div class="treatTxt">
          <h3>诊治</h3>
          <el-input v-model="treatSituation" :rows="6" type="textarea" placeholder="Please input" />
        </div>
        <div class="suggestion">
          <h3>建议</h3>
          <el-input v-model="suggestion" :rows="6" type="textarea" placeholder="Please input" />
        </div>
      </div>
      <div style="width: 100%">
        <el-button type="danger" @click="submit">提交</el-button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { defineProps } from 'vue'
import { ref } from 'vue'
import { setSituation, setSuggestion } from '@/api'
import open from '@/utils/message'
const treatSituation = ref('')
const suggestion = ref('')
const props = defineProps(['getHide', 'id'])
const hideButton = () => {
  props.getHide(false)
}
const submit = async () => {
  try {
    if (treatSituation.value == '' && suggestion.value == '') {
      open('诊断和建议不能都为空', 'error')
      return
    }
    let id = props.id
    let result1, result2
    if (treatSituation.value !== '') {
      result1 = await setSituation(id, treatSituation.value)
      location.reload()
    }
    if (suggestion.value !== '') {
      result2 = await setSuggestion(id, suggestion.value)
      location.reload()
    }

    
    if (result1?.data.code == '200' && result2?.data.code == '200') {
      open('诊治和给与建议成功', 'success')
      location.reload()
    }else if(result1?.data.code == '200' ){
      open('诊治成功', 'success')
      location.reload()

    }else if(result2?.data.code == '200'){
      open('给与建议成功', 'success')
      location.reload()

    }else{
      open('出现了一点小错误，请重试','error')
    }
  } catch (error) {
    console.log(error.message)
  }
}
</script>

<style lang="scss" scoped>
.overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5); /* 半透明黑色背景 */
  z-index: 1002; /* 确保在最上层 */
  display: flex;
  align-items: center;
  justify-content: center;
  .treatUpdateBOx {
    width: 800px;
    height: 500px;
    background-color: #fff;
    .treatTop {
      padding: 20px 20px 5px 20px;
      display: flex;
      justify-content: space-between;
      span:first-child {
        font-size: 20px;
      }
    }
    .treatForm {
      padding: 10px 20px;
      .treatTxt,
      .suggestion {
        margin-bottom: 10px;
        h3 {
          padding: 10px 0;
        }
      }
    }
    .el-button--danger {
      float: right;
      margin-right: 30px;
    }
  }
}
</style>
