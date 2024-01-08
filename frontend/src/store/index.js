import { createStore } from 'vuex';
import axios from 'axios'

export default createStore({
    state: {
        access: '',
        refresh: '',
        user: null,
        darkMode: true
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
            localStorage.removeItem('darkMode');
            localStorage.setItem('darkModeChanged', false);
            delete axios.defaults.headers.common['Authorization'];
        },
        setDarkMode(state, value) {
            localStorage.setItem('darkMode', value);
            document.body.classList.toggle('dark-mode', eval(value));
            this.darkMode = eval(value);
            window.dispatchEvent(new Event('darkModeChanged'));
        },
        setDarkModeChanged(state, value) {
            localStorage.setItem('darkModeChanged', true);
            this.commit('setDarkMode', value);
        }
    },
});