<template>
  <div class="question10Box">
    <h2>行动力</h2>
    <div class="questions">
      <div class="content">
        <h3>请按以下指令完成录制</h3>
        <div class="direction">
          <h4>1.做出数字6的手势</h4>
          <h4>2.鼓掌</h4>
          <h4>3.发出哈哈哈的声音</h4>
        </div>
      </div>

      <div class="details">
        <div class="videoBox">
          <video controls style="width: 100%; height: 100%" ref="videoEl">
            您的浏览器不支持视频标签。
          </video>
        </div>
        <div class="videoRecordButton">
          <el-button type="primary" @click="beginRecord">开始录像</el-button>
          <el-button type="primary" @click="stopRecord">停止录像</el-button>
          <el-button type="primary" @click="playViedo">播放视频</el-button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import useStore from '@/stores/index'
import { uploadVideo } from '@/api'
import open from '@/utils/message'
const { mmse } = useStore()
let videoEl = ref(null)
let videoData = []
let cameraStream = null
let mediaRecorder = null
const beginRecord = () => {
  videoData = []
  // 检查浏览器是否支持 MediaRecorder
  if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
    const constraints = {
      audio: true,
      video: {
        width: 600,
        height: 300
      }
    }

    navigator.mediaDevices
      .getUserMedia(constraints)
      .then(function (stream) {
        cameraStream = stream
        //console.log(cameraStream)
        videoEl.controls = false
        videoEl.value.srcObject = cameraStream
        videoEl.value.play()
        if (typeof MediaRecorder.isTypeSupported === 'function') {
          const mimeType = MediaRecorder.isTypeSupported('video/webm') ? 'video/webm' : 'video/mp4'
          mediaRecorder = new MediaRecorder(cameraStream, { mimeType: mimeType })
        } else {
          mediaRecorder = new MediaRecorder(cameraStream)
        }
        mediaRecorder.start()
        mediaRecorder.addEventListener('dataavailable', function (ev) {
          videoData.push(ev.data)
        })
        mediaRecorder.addEventListener('stop', async function () {
          videoData = new Blob(videoData, { type: 'video/webm' })
          uploadMyViedo(videoData)
          mmse.blobToDataURL(videoData, function (dataURL) {
            mmse.storeDataToSessionStorage(dataURL)
          })
          videoEl.value.srcObject = null
          // 把视频数据转为 URL 传给 video 的 src
          videoEl.value.src = URL.createObjectURL(videoData)
          videoEl.value.controls = true
          // 删除媒体流
          cameraStream = null
        })
      })
      .catch(function (error) {
        console.error('错误:', error)
      })
  } else {
    console.error('浏览器不支持 MediaRecorder')
  }
}
const stopRecord = () => {
  if (mediaRecorder && mediaRecorder.state === 'recording') {
    mediaRecorder.stop()
  }

  if (cameraStream) {
    cameraStream.getTracks().forEach((track) => track.stop())
  }
}
const playViedo = () => {
  videoEl.value.play()
}
const uploadMyViedo = async (videoData) => {
  try {
    if (!videoData) {
      open('视频为空，请录制你的视频', 'error')
      return
    }
    let result = await uploadVideo(videoData)
    //console.log(result.data.data)
    if (result.data.code == '200') {
      mmse.setAnswer10Score(result.data.data)
    } else {
      open('视频录制出现错误，请重新尝试', 'error')
      throw new Error('题目5出现错误,请重试')
    }
  } catch (error) {
    console.log(error.message)
  }
}
onMounted(() => {
  videoEl.value.src = sessionStorage.getItem('videoURL')
})
</script>

<style lang="scss" scoped>
.question10Box {
  margin-left: 100px;
  height: 490px;
  h2 {
    margin-bottom: 40px;
    
  }
  .questions {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;

    .content {
      display: flex;
      flex-direction: column;
      h3 {
        margin-bottom: 25px;
      }
      .direction {
        h4 {
          height: 60px;
          line-height: 60px;
        }
        margin-right: 40px;
      }
    }
    .details {
      
      .videoBox {
        height: 300px;
        width: 600px;
        
      }
      .videoRecordButton {
        margin-top: 10px;
      }
    }
  }
}
</style>
