import { createRouter, createWebHistory } from 'vue-router'
import store from '@/store'

// Root
import RootView from '@/views/RootView.vue'
// Auth
import ContainerSwitcher from '@/views/auth/ContainerSwitcher.vue'
import RecoveryPassword from '@/views/auth/password/RecoveryPassword.vue'
import ResetPassword from '@/views/auth/password/ResetPassword.vue'
import ActivatedAccount from '@/views/auth/password/ActivatedAccount.vue'
// Errors
import NotFoundView from '@/views/errors/NotFoundView.vue'

store.commit('initializeStore');

const routes = [
    { path: '/', component: RootView },
    { path: '/login', component: ContainerSwitcher },
    { path: '/signup', component: ContainerSwitcher },
    {
        path: '/recovery', component: RecoveryPassword, beforeEnter: (to, from, next) => {
            if (from.name === null || from.path === '/login') next();
            else next('/login');
        }
    },
    { path: '/password/reset/confirm/:uid/:token', component: ResetPassword },
    { path: '/activate/:uid/:token', component: ActivatedAccount },
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

export default router;