import { defineStore } from "pinia"
import { reactive, ref } from 'vue'
import { uploadSentence } from '@/api'
const useMmseStore = defineStore('mmse', () => {
  let myAnswer = reactive({
    year: sessionStorage.getItem('year') || '',
    season: sessionStorage.getItem('season') || '',
    month: sessionStorage.getItem('month') || '',
    day: sessionStorage.getItem('day') || '',
    week: sessionStorage.getItem('week') || '',
    floor: sessionStorage.getItem('floor') || '',
    hospital: sessionStorage.getItem('hospital') || '',
    region: JSON.parse(sessionStorage.getItem('region')) || '',
    fruits: sessionStorage.getItem('fruits') || '',
    paper: sessionStorage.getItem('paper') || '',
    train: sessionStorage.getItem('train') || '',
    calculation1: sessionStorage.getItem('calculation1') || '',
    calculation2: sessionStorage.getItem('calculation2') || '',
    calculation3: sessionStorage.getItem('calculation3') || '',
    calculation4: sessionStorage.getItem('calculation4') || '',
    audioUrl: sessionStorage.getItem('audioUrl') || null,
    answer5Score: sessionStorage.getItem('answer5Score') || 0,
    answer6: JSON.parse(sessionStorage.getItem('answer6')) || [],
    answer7: JSON.parse(sessionStorage.getItem('answer7')) || {
      input1: '',
      input2: '',
      input3: ''
    },
    answer8: sessionStorage.getItem('answer8') || '',
    canvasImage: sessionStorage.getItem('canvasImage') || '',
    videoURL: sessionStorage.getItem('videoURL') || '',
    answer9Score: sessionStorage.getItem('answer9Score') || 0,
    answer10Score: sessionStorage.getItem('answer10Score') || 0
  })

  const reset = () => {
    const initialAnswer = {
      year: '',
      season: '',
      month: '',
      day: '',
      week: '',
      floor: '',
      hospital: '',
      region: '',
      fruits: '',
      paper: '',
      train: '',
      calculation1: '',
      calculation2: '',
      calculation3: '',
      calculation4: '',
      audioUrl: null,
      answer5Score: 0,
      answer6: [],
      answer7: {
        input1: '',
        input2: '',
        input3: ''
      },
      answer8: '',
      canvasImage: '',
      videoURL: '',
      answer9Score: 0,
      answer10Score: 0
    }

    // 重置 myAnswer 对象为初始状态
    Object.keys(myAnswer).forEach(key => {
      myAnswer[key] = initialAnswer[key]
    })


  }
  //获得测试分数
  // 创建一个新的 Date 对象，它将自动获取当前日期和时间
  const currentDate = new Date()

  // 获取当前日期
  const currentDay = currentDate.getDate()

  // 获取当前星期几（注意：星期日是 0，星期一是 1，以此类推）
  const currentDayOfWeek = currentDate.getDay()

  // 获取当前月份
  const currentMonth = currentDate.getMonth() + 1

  // 根据月份判断当前季节
  let currentSeason = ref(null)
  switch (currentMonth) {
    case 3:
    case 4:
    case 5:
      currentSeason.value = 'A'
      break
    case 6:
    case 7:
    case 8:
      currentSeason.value = 'B'
      break
    case 9:
    case 10:
    case 11:
      currentSeason.value = 'C'
      break
    case 12:
    case 1:
    case 2:
      currentSeason.value = 'D'
      break
    default:
      currentSeason.value = '未知'
      break
  }
  // 将数字表示的星期转换为文本表示
  const daysOfWeek = ['星期7', '星期1', '星期2', '星期3', '星期4', '星期5', '星期6']
  const currentWeekDay = daysOfWeek[currentDayOfWeek]
  //第一题

  const setYear = (myYear) => {
    myAnswer.year = myYear
    sessionStorage.setItem('year', myYear)

  }
  const setSeason = (mySeason) => {
    myAnswer.season = mySeason
    sessionStorage.setItem('season', mySeason)
  }

  const setMonth = (myMonth) => {
    myAnswer.month = myMonth
    sessionStorage.setItem('month', myMonth)
  }

  const setDay = (myDay) => {
    myAnswer.day = myDay
    sessionStorage.setItem('day', myDay)
  }

  const setWeek = (myWeek) => {
    myAnswer.week = myWeek
    sessionStorage.setItem('week', myWeek)
  }

  //第二题

  const setFloor = (myFloor) => {
    myAnswer.floor = myFloor
    sessionStorage.setItem('floor', myFloor)
  }

  const setHospital = (myHospital) => {
    myAnswer.hospital = myHospital
    sessionStorage.setItem('hospital', myHospital)
  }

  const setRegion = (myRegion) => {
    myAnswer.region = myRegion
    //console.log(myAnswer.region)
    sessionStorage.setItem('region', JSON.stringify(myRegion))
  }
  //第三题
  const setFruits = (myFruits) => {
    myAnswer.fruits = myFruits
    sessionStorage.setItem('fruits', myFruits)
  }

  const setPaper = (myPaper) => {
    myAnswer.paper = myPaper
    sessionStorage.setItem('paper', myPaper)
  }

  const setTrain = (myTrain) => {
    myAnswer.train = myTrain
    sessionStorage.setItem('train', myTrain)
  }

  //第四题

  const setCalculation1 = (myCalculation1) => {
    myAnswer.calculation1 = myCalculation1
    sessionStorage.setItem('calculation1', myCalculation1)
  }

  const setCalculation2 = (myCalculation2) => {
    myAnswer.calculation2 = myCalculation2
    sessionStorage.setItem('calculation2', myCalculation2)
  }

  const setCalculation3 = (myCalculation3) => {
    myAnswer.calculation3 = myCalculation3
    sessionStorage.setItem('calculation3', myCalculation3)
  }

  const setCalculation4 = (myCalculation4) => {
    myAnswer.calculation4 = myCalculation4
    sessionStorage.setItem('calculation4', myCalculation4)
  }

  //第五题
  let setAudio = (value) => {
    myAnswer.audioUrl = value
  }
  const setAnswer5Score = (score) => {
    myAnswer.answer5Score = score
    sessionStorage.setItem('answer5Score', score)

  }
  //第6题
  let setQuestion6 = (value) => {
    myAnswer.answer6 = value
    sessionStorage.setItem('answer6', JSON.stringify(value))
  }
  //第七题
  let setQuestion7 = (value) => {
    myAnswer.answer7 = value
    sessionStorage.setItem('answer7', JSON.stringify(value))
  }
  //第8题
  let setQuestion8 = (value) => {
    myAnswer.answer8 = value
    sessionStorage.setItem('answer8', value)
  }
  //第9题

  let setCanvasImage = (value) => {
    myAnswer.canvasImage = value
  }
  const setAnswer9Score = (score) => {
    myAnswer.answer9Score = score
    sessionStorage.setItem('answer9Score', score)

  }

  //第十题
  // 存储数据到会话存储
  const storeDataToSessionStorage = (dataURL) => {
    myAnswer.videoURL = dataURL
    sessionStorage.setItem('videoURL', dataURL)
  }
  const setAnswer10Score = (score) => {
    myAnswer.answer10Score = score
    sessionStorage.setItem('answer10Score', score)

  }
  // 将 Blob 对象转换为数据 URL
  const blobToDataURL = (blob, callback) => {
    const reader = new FileReader()
    reader.onload = function (event) {
      const dataURL = event.target.result
      myAnswer.videoURL = dataURL
      callback(dataURL)
    }
    reader.readAsDataURL(blob)
  }

  let trueAnswer = {
    year: 'C',
    region: ['湖南省', '长沙市', '天心区'],
    hospital: 'B',
    floor: "第2楼",
    fruits: "A",
    paper: "A",
    train: "A",
    calculation1: "B",
    calculation2: "A",
    calculation3: "A",
    calculation4: "D",
    answer6: ["苹果(Apple)", "报纸(paper)", "火车(train)"],
    answer7: { input1: "卫星", input2: "飞机", input3: "火箭" },
  }

  /*   let number=ref(0) */

  const getMyScore = async () => {
    try {
      let score = 0

      //console.log(myAnswer)
      //console.log(score)
      for (let key in trueAnswer) {
        if (myAnswer[key] == trueAnswer[key]) {
          if (key === 'year') {
            score += 2
          }
          if (key === 'hospital' || key === 'floor' || key === 'fruits' || key === 'paper') {
            score += 3
          }
          if (key == 'train') {
            score += 4
          }
          if (key === 'calculation1' || key === 'calculation2' || key === 'calculation3' || key === 'calculation4') {
            score += 2.5
          }
        }

      }
      if (currentSeason.value === myAnswer.season) {
        score += 2
      }
      if (currentMonth + '月' === myAnswer.month) {
        score += 2
      }
      if (currentDay + '号' === myAnswer.day) {
        score += 2
      }
      if (currentWeekDay === myAnswer.week) {
        score += 2
      }
      let count1 = 0
      for (let i = 0; i < 3; i++) {

        if (myAnswer.region[i] == trueAnswer.region[i]) {
          count1++
        }
        if (count1 == 3) {

          score += 4

        }
        if (trueAnswer.answer6.includes(myAnswer.answer6[i])) {
          if (i == 2) {
            score += 4
          } else {
            score += 3
          }
        }

      }
      if (myAnswer.answer7.input1 === trueAnswer.answer7.input1) {
        score += 3
      }
      if (myAnswer.answer7.input2 === trueAnswer.answer7.input2) {
        score += 3
      }
      if (myAnswer.answer7.input3 === trueAnswer.answer7.input3) {
        score += 4
      }
      if (myAnswer.answer8) {
        let result = await uploadSentence(myAnswer.answer8)
        if (result.data.code == 200) {
          score += 10
          
        }
      }
      if (myAnswer.answer5Score) {
        //console.log(myAnswer.answer5Score)
        score += myAnswer.answer5Score * 1 / 10

      }
      if (myAnswer.answer9Score) {
        //console.log(myAnswer.answer9Score)
        score += myAnswer.answer9Score * 1 / 10

      }
      if (myAnswer.answer10Score) {
        //console.log(myAnswer.answer10Score)
        score += myAnswer.answer10Score * 1 / 10

      }
      //console.log(score)

      return Math.ceil(score)

    } catch (error) {
      console.log(error.message)

    }

  }






  return {
    setYear,
    setSeason,
    setMonth,
    setDay,
    setWeek,
    setHospital,
    setFloor,
    setRegion,
    setFruits,
    setPaper,
    setTrain,
    setCalculation1,
    setCalculation2,
    setCalculation3,
    setCalculation4,
    setAudio,
    setQuestion6,
    setQuestion7,
    setQuestion8,
    setCanvasImage,
    blobToDataURL,
    storeDataToSessionStorage,
    getMyScore,
    setAnswer5Score,
    setAnswer9Score,
    setAnswer10Score,
    reset
  }
})
export default useMmseStore