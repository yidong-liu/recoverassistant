<template>
  <div class="content">
    <leftbar></leftbar>
    <div class="rightContent">
      <topBar></topBar>  
      <RouterView></RouterView>
    </div>
  </div>
</template>

<script setup>
import leftbar from '@/components/leftBar.vue'
import topBar from '@/components/topBar.vue';
import { RouterView } from 'vue-router';
</script>


<style lang="scss" scoped>
.content{
  display: flex;
}
.rightContent{
  width: 100%;
  height: 100vh;
  flex: 1;
  overflow: hidden;
}
</style>