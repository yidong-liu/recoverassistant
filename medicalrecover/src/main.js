import './assets/base.css'
import './assets/main.css'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import { createApp } from 'vue'
import { createPinia } from 'pinia'
import mitt from 'mitt'
import App from './App.vue'
import router from './router'
// 引入阿里云字体图标css
import '@/assets/icons/iconfont.css'
import '@/assets/icons/iconfont.js'
//初始化浏览器初始页面
import 'normalize.css/normalize.css'
let app = createApp(App)
let pinia = createPinia()
app.use(pinia)
app.use(router)
app.use(ElementPlus)
app.config.globalProperties.$mitt = mitt()

app.mount('#app')