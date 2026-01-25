import { createRouter, createWebHashHistory } from 'vue-router'
import Index from '@/views/Index.vue'
import Home from '@/views/Home.vue'
import About from '@/views/About.vue'
import PersonalHome from '@/views/home/PersonalHome.vue'
import ImgGet from '@/views/home/ImgGet.vue'
import Workflow from '@/views/home/Workflow.vue'
import DataAnalyse from '@/views/home/DataAnalyse.vue'
import Chat from '@/views/home/Chat.vue'
import Setting from '@/views/home/Setting.vue'

const routes = [
    {path:'/',name:'index',component:Index},
    {
        path:'/home',
        name:'home',
        component:Home,
        children:[
            {
                path:'',
                name:'personalHome',
                component:PersonalHome
            },
            {
                path:'imgGet',
                name:'imgGet',
                component:ImgGet
            },
            {
                path:'workflow',
                name:'workflow',
                component:Workflow
            },
            {
                path:'dataAnalyse',
                name:'dataAnalyse',
                component:DataAnalyse
            },
            {
                path:'chat',
                name:'chat',
                component:Chat
            },
            {
                path:'setting',
                name:'setting',
                component:Setting
            }
        ]
    },
    {path:'/about',name:'about',component:About},
]

const router = createRouter({
        history:createWebHashHistory(),
        routes,
        scrollBehavior() {
            // 始终滚动到顶部
            return { top: 0 }
        }
    })

export default router
