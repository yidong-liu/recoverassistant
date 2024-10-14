
import useMainStore from './main'
import useMmseStore from './mmse'
 
// 统一导出useStore方法
export default function useStore() {
  return {
    mainStore:useMainStore(),
    mmse:useMmseStore()
  }
}
 