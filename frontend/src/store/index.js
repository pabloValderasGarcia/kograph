import { createStore } from 'vuex';
import axios from 'axios'

export default createStore({
    state: {
        access: '',
        refresh: '',
        user: null
    },
    mutations: {
        initializeStore(state) {
            if (localStorage.getItem('access')) {
                state.access = localStorage.getItem('access');
                state.refresh = localStorage.getItem('refresh');
                axios.defaults.headers.common['Authorization'] = 'Bearer ' + state.access;
            }
        },
        setAccess(state, access) {
            state.access = access;
            localStorage.setItem('access', access);
            axios.defaults.headers.common['Authorization'] = 'Bearer ' + access;
        },
        setRefresh(state, refresh) {
            state.refresh = refresh;
            localStorage.setItem('refresh', refresh);
        },
        removeAccess(state) {
            state.access = '';
            state.refresh = '';
            state.user = null;
            localStorage.removeItem('access');
            localStorage.removeItem('refresh');
            delete axios.defaults.headers.common['Authorization'];
        }
    },
});