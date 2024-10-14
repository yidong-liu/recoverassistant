<template>
  <transition name="fade" mode="out-in">
    <div class="leftbar" @click="goDetail">
      <div class="logo">智能康复</div>
      <div class="bar">
        <div v-for="(item, index) in leftBar" :key="index">
          <div v-if="item.role === role" :class="{ samllSize: mode, bigSize: !mode }">
            <router-link :to="item.route">
              <i :class="['iconfont', item.icon]" style="margin-right: 3px"></i>
              <span :class="{ hide: mode }">{{ item.barItemm }}</span>
            </router-link>
          </div>
        </div>
      </div>
    </div>
  </transition>
</template>

<script setup>
let mode = ref(true)
import { ref, onBeforeMount, getCurrentInstance, computed } from 'vue'
const { appContext } = getCurrentInstance()
import { useRoute } from 'vue-router'
const route = useRoute()
const role = computed(() => {
  return /doctor|patient/.exec(route.path)[0]
})
const leftBar = [
  { barItemm: 'MMSE评定', role: 'patient', icon: 'icon-ceshishenqing', route: '/patient/mmse' },
  { barItemm: '我的病历', role: 'patient', icon: 'icon-shouye', route: '/patient/medicalRecord' },
  { barItemm: '评定统计', role: 'patient', icon: 'icon-tongji', route: '/patient/evaluation' },
  { barItemm: '基本信息', role: 'patient', icon: 'icon-shezhi', route: '/patient/information' },
  { barItemm: '添加病人', role: 'doctor', icon: 'icon-shouye', route: '/doctor/manage' },
  { barItemm: '我的病人', role: 'doctor', icon: 'icon-ceshishenqing', route: '/doctor/myPatient' },
  { barItemm: '基本信息', role: 'doctor', icon: 'icon-shezhi', route: '/doctor/information' },
 

]
onBeforeMount(() => {
  appContext.config.globalProperties.$mitt.on('changeSize', (e) => {
    mode.value = e
  })
})
</script>

<style lang="scss" scoped>
.leftbar {
  height: 100vh;
  background-color: rgb(0, 21, 41);
  transition: transform 0.5s ease-in-out;

  overflow: auto;
  .fade-enter-active,
  .fade-leave-active {
    transition: transform 0.5s ease-in-out;
  }

  .fade-enter,
  .fade-leave-to {
    transform: translateX(100%);
    opacity: 0;
  }
  .logo {
    height: 55px;
    text-align: center;
    line-height: 56px;
    font-size: 12px;
    font-style: italic;
  }
  .bar {
    .hide {
      display: none;
    }
    .iconfont {
      font-size: 20px;
    }
    .samllSize {
      width: 55px;
      height: 80px;
      text-align: center;
      line-height: 80px;
     
    }
    .samllSize:hover {
      background: linear-gradient(to right, #3498db, #ffffff);
    }
    .bigSize {
      padding: 0 15px;
      display: block;
      height: 80px;
      line-height: 80px;
      text-align: center;
    }
    .bigSize:hover {
      background: linear-gradient(to right, #3498db, #ffffff);
    }
  }
}
</style>
