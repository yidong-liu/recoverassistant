import { ElMessage } from 'element-plus'
const open=(message,type)=>{
  ElMessage({
    message,
    type
  })
}
export default open