import { createRouter, createWebHistory } from 'vue-router'
// import store from '@/store'

// Home
import HomeView from '@/views/HomeView.vue'
// App
import AppView from '@/views/AppView.vue'

// Auth
import LoginView from '@/views/auth/LoginView.vue'
import RegisterView from '@/views/auth/RegisterView.vue'
// Errors
import NotFoundView from '@/views/errors/NotFoundView.vue'

const routes = [
    { path: '/', component: localStorage.getItem('token') ? AppView : HomeView },
    { path: '/login', component: LoginView },
    { path: '/register', component: RegisterView },
    { path: '/:catchAll(.*)', component: NotFoundView },
]

const router = createRouter({
    history: createWebHistory(process.env.BASE_URL),
    routes
})

router.beforeEach((to, from, next) => {
    if (to.matched.some(record => record.meta.requiresAuth)) {
        const token = localStorage.getItem('token');
        if (!token) {
            next('/login');
        } else {
            next();
        }
    } else {
        next();
    }
});

export default router