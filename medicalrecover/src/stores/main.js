import { defineStore } from "pinia"
import {ref} from 'vue'
import { getUserInformation } from '@/api';
const useMainStore = defineStore('main', () => {
 let token = ref(localStorage.getItem('token')||null)
 const setToken=(myToken)=>{
  //console.log(myToken)
  token.value=myToken
  localStorage.setItem('token',myToken)
  localStorage.setItem('isAuthenticated','true')
 }
 const getToken=()=>{
    token.value=localStorage.getItem('token')
 }
 const removeToken=()=>{
  token.value=null
  localStorage.removeItem('token')
  localStorage.removeItem('role')
  localStorage.removeItem('isAuthenticated')
 }

 const getInformation=async()=>{
  
  let role=localStorage.getItem('role')
  let result=await getUserInformation(role)
  //console.log(result)
  let data=result.data.data
  let code=result.data.code
  if(code==200){
    //console.log(data)
    return data
  }else{
    throw new Error(`${result.data.message}`)
  }
}
  return {token,setToken,getToken,removeToken,getInformation }
})
export default useMainStore