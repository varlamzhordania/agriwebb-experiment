import {createWebHistory, createRouter} from 'vue-router'
import Login from "./components/Login.vue";
import LoginCallback from "./components/LoginCallback.vue";


const routes = [
    {path: '/', component: Login},
    {path: '/authorization/callback', component: LoginCallback},
]

const router = createRouter({
    history: createWebHistory(),
    routes,
})

export default router