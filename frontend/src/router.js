import {createRouter, createWebHistory} from 'vue-router'
import Home from './components/Home.vue'
import Report from './components/Report.vue'

export default 
    createRouter({
        history: createWebHistory(),
        routes: [
            {path:'/', component: Home},
            {path:'/report/:id', component: Report},
        ]
    })