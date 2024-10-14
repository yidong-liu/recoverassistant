<template>
  <div class="question9Box">
    <h2>临摹</h2>
    <div class="textBox">
      <h3>
        请照下方的图 用鼠标在右边方框内 做出一幅一样的图(<span style="color: red"
          >请在作图后保存图片</span
        >)
      </h3>
      <div class="detail">
        <img src="@/assets/images/testImg.png" alt="图形" style="width: 300px; height: 250px" />
        <div class="canvasContainer">
          <canvas
            width="400"
            height="300"
            ref="cvs"
            @mousedown="startDrawing"
            @mousemove="draw"
            @mouseup="stopDrawing"
            @mouseleave="stopDrawing"
            style="border: 1px solid rgb(151, 221, 45)"
          >
            您的浏览器不支持canvas,请更换谷歌浏览器或升级您的浏览器
          </canvas>
          <div class="buttonGroup">
            <el-button type="success" plain @click="clearCanvas">清除画布</el-button>
            <el-button type="success" plain @click="saveImage">保存图片</el-button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import useStore from '@/stores/index'

import { uploadImage } from '@/api'
const { mmse } = useStore()
const cvs = ref(null)
let lastX = ref(0)
let lastY = ref(0)
let isDrawing = ref(false)
const startDrawing = (event) => {
  isDrawing.value = true
  lastX.value = event.offsetX
  lastY.value = event.offsetY
}

const draw = (event) => {
  if (!isDrawing.value) return
  const canvas = cvs.value
  const ctx = canvas.getContext('2d')

  ctx.strokeStyle = '#000' // 设置画笔颜色
  ctx.lineWidth = 2 // 设置线条宽度
  ctx.lineJoin = 'round' // 设置线条连接样式
  ctx.lineCap = 'round' // 设置线条端点样式

  ctx.beginPath()
  ctx.moveTo(lastX.value, lastY.value) // 移动画笔到起始点
  ctx.lineTo(event.offsetX, event.offsetY) // 从起始点到当前鼠标位置绘制线条
  ctx.stroke()
  lastX.value = event.offsetX
  lastY.value = event.offsetY
}

const stopDrawing = () => {
  isDrawing.value = false
}

const clearCanvas = () => {
  const canvas = cvs.value
  const ctx = canvas.getContext('2d')
  ctx.clearRect(0, 0, canvas.width, canvas.height)
  if (sessionStorage.getItem('canvasImage')) {
    sessionStorage.removeItem('canvasImage')
  }
}
// 保存Canvas中的图像数据到本地存储
const saveCanvasImage = () => {
  const canvas = cvs.value
  const dataURL = canvas.toDataURL()
  sessionStorage.setItem('canvasImage', dataURL)
  mmse.setCanvasImage(dataURL)
}

// 加载本地存储中的Canvas图像数据
const loadCanvasImage = () => {
  const canvas = cvs.value
  const dataURL = sessionStorage.getItem('canvasImage')
  if (dataURL) {
    const img = new Image()
    img.onload = function () {
      canvas.getContext('2d').drawImage(img, 0, 0)
    }
    img.src = dataURL
  }
}

// 在页面加载时加载Canvas图像数据
onMounted(() => {
  loadCanvasImage()
})

const saveImage = async () => {
  try {
    saveCanvasImage()
    const canvas = cvs.value
    const dataURL = canvas.toDataURL() // 将 Canvas 内容转换为 base64 编码的图像数据
    //console.log(dataURL)
    // 在这里将 dataURL 上传至服务器
    let result = await uploadImage(dataURL)
    //console.log(result)
    if(result.data.code=='200'){
      mmse.setAnswer9Score(result.data.data)

    }else{
      throw new Error('题目5出现错误')
    }
  } catch (error) {
    console.log(error.message)
  }
}
</script>

<style lang="scss" scoped>
.question9Box {
  margin-left: 150px;
  height: 490px;

  h2 {
    margin-bottom: 40px;
  }
  .textBox {
    h3 {
      margin-bottom: 25px;
    }

    .detail {
      display: flex;
      align-items: center;
      .canvasContainer {
        margin-left: 60px;
        display: inline-block;
        .buttonGroup {
          width: 100%;
          display: flex;
          padding: 8px 10px;
          justify-content: space-between;
        }
      }
    }
  }
}
</style>
