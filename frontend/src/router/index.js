import { createRouter, createWebHistory } from 'vue-router'
import store from '@/store'

// Root
import RootView from '@/views/RootView.vue'
// Auth
import LogIn from '@/views/auth/LogIn.vue'
import SignUp from '@/views/auth/SignUp.vue'
// Errors
import NotFoundView from '@/views/errors/NotFoundView.vue'

store.commit('initializeStore')

const routes = [
    { path: '/', component: RootView },
    { path: '/login', component: LogIn },
    { path: '/signup', component: SignUp },
    { path: '/:catchAll(.*)', component: NotFoundView },
]

const router = createRouter({
    history: createWebHistory(process.env.BASE_URL),
    routes
})

router.beforeEach((to, from, next) => {
    if (to.matched.some(record => record.meta.requiresAuth)) {
        const token = store.state.access;
        console.log(token);
        if (token === '') {
            next('/login');
        } else {
            next();
        }
    } else {
        next();
    }
});

export default router