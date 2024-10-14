import { createRouter, createWebHashHistory } from 'vue-router'

const router = createRouter({
  history: createWebHashHistory(),
  routes: [
    {
      path: '/',
      redirect: "/login"


    },
    {
      path: "/login",
      component: () => import('@/views/login.vue'),
      name: 'Login'
    },
    {
      path: "/patient",
      component: () => import('@/views/index.vue'),
      children: [
        {
          path: "/patient",
          redirect: "/patient/mmse"

        },
        {
          path: 'mmse',
          component: () => import('@/views/patient/mmse.vue')


        },
        {
          path: "information",
          component: () => import('@/views/patient/information.vue')
        },
        {
          path: 'evaluation',
          component: () => import('@/views/patient/evaluation.vue')

        },
        {
          path: "medicalRecord",
          component: () => import('@/views/patient/myMedicalRecord.vue')
        }


      ],

    },

    {
      path: "/mmse/questions",
      component: () => import('@/views/patient/questions/index.vue'),
      children: [
        {
          path: "/mmse/questions",
          redirect: "/mmse/questions/question1"

        },
        {
          path: 'question1',
          component: () => import('@/views/patient/questions/question1.vue')
        },
        {
          path: 'question2',
          component: () => import('@/views/patient/questions/question2.vue')

        },
        {
          path: 'question3',
          component: () => import('@/views/patient/questions/question3.vue')

        },
        {
          path: 'question4',
          component: () => import('@/views/patient/questions/question4.vue')

        },
        {
          path: 'question5',
          component: () => import('@/views/patient/questions/question5.vue')

        },
        {
          path: 'question6',
          component: () => import('@/views/patient/questions/question6.vue')

        },
        {
          path: 'question7',
          component: () => import('@/views/patient/questions/question7.vue')

        },
        {
          path: 'question8',
          component: () => import('@/views/patient/questions/question8.vue')

        },
        {
          path: 'question9',
          component: () => import('@/views/patient/questions/question9.vue')

        },
        {
          path: 'question10',
          component: () => import('@/views/patient/questions/question10.vue')

        }
      ]
    },
    {
      path: "/doctor",
      component: () => import('@/views/index.vue'),
      children: [
        {
          path: "/doctor",
          redirect: "doctor/manage"

        },
        {
          path: 'information',
          component: () => import('@/views/doctor/information.vue')


        },
        {
          path:'manage',
          component: () => import('@/views/doctor/manage.vue')
        },
        {
          path:'myPatient',
          component: () => import('@/views/doctor/myPatient.vue')
        },
        {
          path: 'myPatient/evaluation',
          component: () => import('@/views/patient/evaluation.vue')

        },


      ],
    }

  ]
})
router.beforeEach(async (to, from) => {
  let isAuthenticated = localStorage.getItem('isAuthenticated') || false
  if (
    // 检查用户是否已登录
    !isAuthenticated &&
    // ❗️ 避免无限重定向
    to.name !== 'Login'
  ) {
    // 将用户重定向到登录页面
    return { name: 'Login' }
  }
  
  
})
export default router
