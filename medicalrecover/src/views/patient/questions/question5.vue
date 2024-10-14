<template>
  <div class="question5Box">
    <h2>注意力</h2>
    <div class="questions">
      <h3>
        点击下方第一个播放按钮听清楚语音播放内容 随后点击语音录制按钮倒转听到的语言内容 ( 注意 :
        录制自动结束)
      </h3>
      <div>
        <h4>测试音频</h4>
        <audio controls>
          <source src="../../../../public/audio/ttsmaker-祝出入平安.mp3" type="audio/mp3" />
          Your browser does not support the audio element.
        </audio>
      </div>
      <div>
        <h4>我的音频</h4>
        <audio controls ref="audioElement"></audio>
        <el-button type="info" @click="startRecording">语音录制</el-button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import useStore from '@/stores/index'
import { uploadAudio } from '@/api'
const { mmse } = useStore()
let mediaRecorder = null
let recordedChunks = []
let audioBlob = null
let mediaStream = null
const audioElement = ref(null)
const stopRecording = () => {
  if (mediaRecorder && mediaRecorder.state === 'recording') {
    mediaRecorder.stop()
    //releaseMicrophone()
  }
}
const releaseMicrophone = () => {
  // 停止媒体流以释放麦克风资源
  if (mediaStream) {
    const tracks = mediaStream.getTracks()
    tracks.forEach((track) => track.stop())
  }
}
// 将 Blob 对象转换为 Data URL
const blobToDataURL = (blob) => {
  return new Promise((resolve, reject) => {
    const reader = new FileReader()
    reader.onloadend = () => {
      resolve(reader.result)
    }
    reader.onerror = reject
    reader.readAsDataURL(blob)
  })
}

const startRecording = async () => {
  try {
    setTimeout(() => {
      stopRecording()
      
    }, 5000)
    // 获取用户媒体流
    mediaStream = await navigator.mediaDevices.getUserMedia({ audio: true })

    // 创建 MediaRecorder
    mediaRecorder = new MediaRecorder(mediaStream)

    // 设置事件处理
    mediaRecorder.ondataavailable = (event) => {
      if (event.data.size > 0) {
        recordedChunks.push(event.data)
      }
    }

    mediaRecorder.onstop = async () => {
      try {
        // 处理录制的数据
        audioBlob = new Blob(recordedChunks, { type: 'audio/wav' })
        blobToDataURL(audioBlob).then((dataURL) => {
          // 此时 dataURL 是包含音频数据的 Data URL
          //console.log(dataURL)
          // 将 dataURL 存储到 sessionStorage 中
          sessionStorage.setItem('audioUrl', dataURL)
          mmse.setAudio(dataURL)
          audioElement.value.src = dataURL
        })
        let result = await uploadAudio(audioBlob)
        //console.log(result)
        if (result.data.code == '200') {
          mmse.setAnswer5Score(result.data.data)
        }else{
          throw new Error('题目5出现错误')
        }
        // 释放麦克风资源
        releaseMicrophone()
      } catch (error) {
        console.log(error.message)
      }
    }

    // 启动录制
    mediaRecorder.start()
  } catch (error) {
    console.error('Error accessing microphone:', error)
  }
}

// 页面加载时从sessionStorage加载音频URL
onMounted(() => {
  const savedAudioUrl = sessionStorage.getItem('audioUrl')
  if (savedAudioUrl) {
    audioElement.value.src = savedAudioUrl
  }
})
</script>

<style lang="scss" scoped>
.question5Box {
  margin-left: 200px;

  height: 490px;
  h2 {
    margin-bottom: 40px;
  }
  .questions {
    h3 {
      margin-bottom: 30px;
    }
    h4 {
      margin-bottom: 10px;
    }
    audio {
      margin-bottom: 50px;
    }
    .el-button {
      float: right;
      margin-top: 80px;
    }
  }
}
</style>
