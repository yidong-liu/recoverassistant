import echarts from '@/utils/ecahrt'
 const initEchart=(id,option)=>{
  let myChart = echarts.init(document.getElementById(id))
  window.addEventListener('resize', function() {
    myChart.resize();
  });
  myChart.setOption(option)
  return myChart

}
export default initEchart