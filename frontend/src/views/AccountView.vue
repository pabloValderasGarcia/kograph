<script>
import LogoItem from '@/components/nav/LogoItem.vue';
import UserDropdown from '@/components/nav/UserDropdown.vue';
import UserPicture from '@/components/nav/UserPicture.vue';
import axios from 'axios';
import { notify } from 'notiwind';
import { Pie } from 'vue-chartjs';
import { Bar } from 'vue-chartjs';
import { Line } from 'vue-chartjs';
import { Chart as ChartJS, Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale, PointElement, LineElement, ArcElement } from 'chart.js';
ChartJS.register(Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale, PointElement, LineElement, ArcElement)

export default {
  watch: {
  },
    name: 'AccountView',
    data() {
        return {
            username: null,
            email: null,
            // Charts
            filesData: [],
            feelingsData: [],
            topElementsData: {},
            userActivityData: [],
            darkMode: document.body.classList.contains('dark-mode')
        }
    },
    async mounted() {
        window.addEventListener('darkModeChanged', this.handleDarkModeChanged);

        // Comprobamos si existe usuario
        if (this.$store.state.access !== '') {
            this.fetchUserData();
            document.title = `Account - Kograph`;
        } else {
            this.$router.push('/');
        }
        setInterval(() => {
            if (this.$store.state.access == '') {
                this.$router.push('/');
            }
        }, 59000);

        // Obtención ficheros
        const token = localStorage.getItem('access');
        const response = await axios.post(`${process.env.VUE_APP_SERVER_URL}/file/get/`, {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });
        this.filesData = response.data;

        // Iniciar Charts
        await this.initChartsData();
    },
    beforeUnmount() {
        window.removeEventListener('darkModeChanged', this.handleDarkModeChanged);
    },
    methods: {
        // Método para comprobar si el modo oscuro se ha cambiado
        handleDarkModeChanged() {
            this.darkMode = localStorage.getItem('darkMode') === 'true';
        },
        // Obtener el userData
        fetchUserData() {
            axios.get(`${process.env.VUE_APP_SERVER_URL}/auth/users/me/`, {
                headers: {
                    'Authorization': `Bearer ${this.$store.state.access}`
                }
            }).then(response => {
                this.$store.state.user = response.data;
                this.username = this.$store.state.user.username;
                this.email = this.$store.state.user.email;
            }).catch(() => {
                notify({
                    group: "foo",
                    title: "Error",
                    text: "Session token has expired.",
                    type: "error"
                }, 5000);
                this.$store.commit('removeAccess');
            });
        },
        // Abrir el input para cambiar foto de perfil
        openFileInput() {
            this.$refs.fileInput.click();
        },
        // Actualizar foto de perfil del usuario
        async handleFileChange(event) {
            const file = event.target.files[0];

            try {
                const formData = new FormData();
                formData.append('picture', file);
                formData.append('email', this.$store.state.user.email);
                const response = await axios.put(`${process.env.VUE_APP_SERVER_URL}/auth/users/me/`, formData, {
                    headers: {
                        'Authorization': `Bearer ${this.$store.state.access}`
                    }
                });

                // Actualizar la imagen de perfil del usuario en el cliente
                this.$store.state.user = response.data;
                notify({
                    group: "foo",
                    title: "Success",
                    text: "User picture updated successfully.",
                    type: "success"
                }, 4000);
            } catch (error) {
                notify({
                    group: "foo",
                    title: "Error",
                    text: "Failed to update user picture.",
                    type: "error"
                }, 4000);
            }
        },
        // Actualizar campo del usuario
        async updateUser(field) {
			try {
                // Petición
                const response = await axios.put(`${process.env.VUE_APP_SERVER_URL}/auth/users/me/`, { 
                    username: field == 'username' ? this.username : this.$store.state.user.username,
                    email: field == 'email' ? this.email : this.$store.state.user.email
                }, {
                    headers: {
                        'Authorization': `Bearer ${this.$store.state.access}`
                    }
                });

                notify({
                    group: "foo",
                    title: "Success",
                    text: `User updated successfully.`,
                    type: "success"
                }, 4000);
                
                // Actualizar campos
                this.$store.state.user = response.data;
                if (field == 'username') this.username = response.data.username;
                if (field == 'email') {
                    this.email = response.data.email;
                    this.logout();
                }
            } catch (error) {
                notify({
                    group: "foo",
                    title: "Error",
                    text: `Failed to update user.`,
                    type: "error"
                }, 4000);
            }
		},
        // Logout
        logout() {
            if (document.getElementById('uploaded_alert')) document.getElementById('uploaded_alert').remove();
            this.$store.commit('removeAccess');
            this.$nextTick(() => {
                this.$router.push('/');
            });
            notify({
                group: "foo",
                title: "Success",
                text: "Successfully logout.",
                type: "success"
            }, 4000);
        },
        // Iniciar data de CHARTS
        async initChartsData() {
            // | ----------------------------------------------- |
            // | ------------------ BAR CHART ------------------ |
            // | ----------------------------------------------- |

            // Obtener cantidad de top 5 sentimientos (alegría, tristeza, ira, miedo, asco)
            this.feelingsData = [0, 0, 0, 0, 0];
            this.filesData.forEach(file => {
                // Verificar si hay datos en aws_feelings
                if (file.aws_feelings && file.aws_feelings.length > 0) {
                    // Dividir las emociones en una lista
                    const emotions = file.aws_feelings.split(',');
                    // Incrementar los contadores según la presencia de cada emoción
                    emotions.forEach(emotion => {
                        const trimmedEmotion = emotion.trim();
                        switch (trimmedEmotion) {
                            case 'Happy':
                                this.feelingsData[0]++;
                                break;
                            case 'Sad':
                                this.feelingsData[1]++;
                                break;
                            case 'Angry':
                                this.feelingsData[2]++;
                                break;
                            case 'Fear':
                                this.feelingsData[3]++;
                                break;
                            case 'Disgusted':
                                this.feelingsData[4]++;
                                break;
                        }
                    });
                }
            });

            // | ----------------------------------------------- |
            // | ------------------ PIE CHART ------------------ |
            // | ----------------------------------------------- |

            // Obtener cantidad de top 5 elementos más encontrados
            const tagCount = {};
            this.filesData.forEach(file => {
                // Obtener las etiquetas del campo aws_tags
                if (file.aws_tags) {
                    const tags = file.aws_tags.split(',');
                    tags.forEach(tag => {
                        tagCount[tag] = (tagCount[tag] || 0) + 1;
                    });
                }
            });

            // Ordenar descendentemente
            const sortedTagCount = Object.fromEntries(
                Object.entries(tagCount).sort(([,a],[,b]) => b - a)
            );

            // Tomar las 5 etiquetas principales y almacenarlas en topElementsData
            this.topElementsData = Object.fromEntries(
                Object.entries(sortedTagCount).slice(0, 5)
            );

            // | ------------------------------------------------ |
            // | ------------------ LINE CHART ------------------ |
            // | ------------------------------------------------ |

            // Obtener cantidad de ficheros creados x mes
            const currentYear = new Date().getFullYear();
            let userActivityData = Array(12).fill(0);
            this.filesData.forEach(file => {
                const createdAt = new Date(file.created_at);
                const fileYear = createdAt.getFullYear();
                
                // Comprobar si el archivo es del año actual
                if (fileYear === currentYear) {
                    const monthIndex = createdAt.getMonth();
                    userActivityData[monthIndex]++;
                }
            });

            // Devolver array de ficheros por mes
            this.userActivityData = userActivityData;
        }
    },
    components: { LogoItem, UserDropdown, UserPicture, Pie, Bar, Line }
}
</script>

<template>
    <div>
        <!-- NAV -->
        <div class="nav">
            <div class="tooltip ttl back" @click="this.$router.go(-1)">
                <font-awesome-icon icon="arrow-left"/>
                <p>Back</p>
            </div>
            <LogoItem @click="this.$router.push('/all')" />
            <UserDropdown />
        </div>
        <!-- ACCOUNT -->
        <div class="account">
            <!-- SIDEBAR -->
            <div class="sidebar">
                <p class="active"><font-awesome-icon icon="user"/>Profile</p>
                <p><font-awesome-icon icon="lock"/>Password</p>
                <p><font-awesome-icon icon="gear"/>Others</p>
            </div>
            <!-- INFO -->
            <div class="info">
                <div class="picture" v-if="this.$store.state.user">
                    <UserPicture />
                    <input type="file" ref="fileInput" style="display: none" @change="handleFileChange">
                    <div class="tooltip ttl back" @click="openFileInput">
                        <font-awesome-icon icon="pen-to-square" />
                        <p>Change&nbsp;picture</p>
                    </div>
                </div>
                <div v-if="this.$store.state.user">
                    <div class="info_input">
                        <label for="username"><font-awesome-icon icon="user"/>Username</label>
                        <input id="username" name="username" v-model="this.username" autocomplete="username" @keyup.enter="updateUser('username')"/>
                        <font-awesome-icon icon="floppy-disk" @click="updateUser('username')" v-if="this.$store.state.user.username != this.username"/>
                    </div>
                    <div class="info_input">
                        <label for="email"><font-awesome-icon icon="envelope"/>Email address</label>
                        <input id="email" name="email" type="email" v-model="this.email"  @keyup.enter="updateUser('email')"/>
                        <font-awesome-icon icon="floppy-disk" @click="updateUser('email')" v-if="this.$store.state.user.email != this.email"/>
                    </div>
                </div>
                <div v-if="this.$store.state.user">
                    <label><font-awesome-icon icon="chart-simple"/>AI Activity</label>
                    <div class="ai_activity">
                        <div class="others">
                            <!-- EMOCIONES -->
                            <Bar v-if="this.feelingsData.some(value => value !== 0)"
                                id="bar"
                                :options="{
                                    responsive: true,
                                    plugins: {
                                        tooltip: {
                                            padding: 15,
                                            boxPadding: 5
                                        },
                                        legend: {
                                            display: true,
                                            align: 'center',
                                            position: 'top',
                                            labels: {
                                                color: this.darkMode ? 'white' : 'black',
                                                font: {
                                                    size: 13,
                                                    family: 'Lato'
                                                },
                                            },
                                            onClick: null
                                        }
                                    },
                                    layout: {
                                        padding: 30
                                    },
                                    scales: {
                                        x: {
                                            display: false
                                        },
                                        y: {
                                            ticks: {
                                                color: this.darkMode ? 'white' : 'black',
                                                font: {
                                                    size: 10,
                                                },
                                                precision: 0
                                            }
                                        }
                                    }
                                }"
                                :data="{
                                    legend: '',
                                    labels: [ 'Happy', 'Sad', 'Angry', 'Fear', 'Disgusted' ],
                                    datasets: [ { 
                                        label: ['Emotions Files'],
                                        backgroundColor: ['#FF9F69', '#318ba7', '#EC5959', '#242424', '#65276F'],
                                        data: this.feelingsData
                                    } ]
                                }"
                            />
                            <div v-else>
                                No suitable files to display
                            </div>
                            <!-- TOP 5 ELEMENTOS MÁS COMUNES EN FOTOS -->
                            <Pie v-if="Object.keys(this.topElementsData).length > 0"
                                id="pie"
                                :options="{
                                    responsive: true,
                                    plugins: {
                                        tooltip: {
                                            padding: 15,
                                            boxPadding: 5
                                        },
                                        legend: {
                                            display: true,
                                            align: 'center',
                                            position: 'right',
                                            labels: {
                                                color: this.darkMode ? 'white' : 'black',
                                                font: {
                                                    size: 13,
                                                    family: 'Lato'
                                                },
                                            }
                                        }
                                    },
                                    layout: {
                                        padding: {
                                            left: 40,
                                            right: 40
                                        },
                                    }
                                }"
                                :data="{
                                    labels: Object.keys(this.topElementsData),
                                    datasets: [ {
                                        label: ['Found In'], 
                                        backgroundColor: ['#318ba7', '#E1C842', '#E57C6E', '#2ab72a', '#E5A76E'],
                                        borderWidth: 0,
                                        data: Object.values(this.topElementsData)
                                    } ]
                                }"
                            />
                            <div v-else>
                                No suitable files to display
                            </div>
                        </div>
                        <div class="others">
                            <!-- ACTIVIDAD DEL USUARIO -->
                            <Line
                                id="line"
                                :options="{
                                    responsive: true,
                                    maintainAspectRatio: false,
                                    plugins: {
                                        tooltip: {
                                            padding: 15,
                                            boxPadding: 5
                                        },
                                        legend: {
                                            display: true,
                                            align: 'center',
                                            position: 'top',
                                            labels: {
                                                color: this.darkMode ? 'white' : 'black',
                                                font: {
                                                    size: 13,
                                                    family: 'Lato'
                                                },
                                            },
                                            onClick: null
                                        }
                                    },
                                    layout: {
                                        padding: {
                                            top: 40,
                                            bottom: 40,
                                            left: 50,
                                            right: 50
                                        }
                                    },
                                    scales: {
                                        x: {
                                            ticks: {
                                                color: this.darkMode ? 'white' : 'black',
                                                font: {
                                                    size: 10,
                                                }
                                            }
                                        },
                                        y: {
                                            display: this.userActivityData.some(value => value !== 0),
                                            ticks: {
                                                color: this.darkMode ? 'white' : 'black',
                                                font: {
                                                    size: 10,
                                                },
                                                precision: 0
                                            },
                                            min: 1,
                                            callback: function(value) {
                                                if (value === 0) {
                                                    return '';
                                                }
                                                return value;
                                            }
                                        }
                                    }
                                }"
                                :data="{
                                    labels: [ 'January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'October', 'September', 'November', 'December' ],
                                    datasets: [ {
                                        label: ['Uploaded Files'],
                                        borderColor: '#318ba7',
                                        backgroundColor: '#318ba7',
                                        data: this.userActivityData
                                    } ]
                                }"
                            />
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<style scoped>
.nav {
    padding: 10px 45px;
    width: 100%;
    display: flex;
    align-items: center;
    justify-content: space-between;
    box-sizing: border-box;
    gap: 25px;
    z-index: 99;
    background-color: white !important;
}

body.dark-mode .nav {
    background-color: #242424 !important;
}

.tooltip {
    position: relative;
}

.tooltip > p {
    width: auto;
	border-radius: 5px;
	padding: 8px 15px;
	position: absolute;
	bottom: -40px;
	right: 0;
	opacity: 0;
	transition: opacity .3s ease-in-out;
	background-color: #E8E8E8;
    pointer-events: none;
}

body.dark-mode .tooltip > p {
    background-color: #373737;
}

.tooltip:hover > p {
    opacity: 1;
}

.ttl p {
    width: fit-content;
	top: unset !important;
	left: 0 !important;
	bottom: -40px !important;
}

.back {
    aspect-ratio: 1/1;
	cursor: pointer;
	padding: 13px;
	border-radius: 50px;
    background-color: #E8E8E8;
}

body.dark-mode .back {
    background-color: #373737;
}

/* ACCOUNT */
.account {
    display: flex;
}

.sidebar {
    flex: 1;
    padding: 25px 0;
    display: flex;
    flex-direction: column;
}

.sidebar p {
    cursor: pointer;
    display: flex;
    gap: 10px;
    padding: 15px 30px;
    width: 100%;
}

.sidebar p:hover {
    background-color: #E8E8E8;
}

.sidebar p.active {
    background-color: #E8E8E8;
}

body.dark-mode .sidebar p:hover {
    background-color: #373737;
}

body.dark-mode .sidebar p.active {
    background-color: #373737;
}

.info {
    flex: 5;
    padding: 0 60px 30px 60px;
    display: flex;
    flex-direction: column;
    gap: 45px;
}

.info > div:not(:last-child) {
    display: flex;
    gap: 30px;
}

.info > div:last-child {
    display: flex;
    flex-direction: column;
    gap: 15px;
}

.info_input {
    position: relative;
    display: flex;
    flex-direction: column;
    gap: 15px;
}

.info_input:first-child {
    flex: 1;
}

.info_input:last-child {
    flex: 2;
}

.info_input div {
    display: flex;
    flex-direction: column;
    gap: 25px;
}

.info_input > input {
    padding-right: 37px;
}

.info_input > svg {
    cursor: pointer;
    position: absolute;
    top: 40px;
    right: 12px;
}

label {
    display: flex;
    gap: 10px;
    font-size: 14px;
}

.picture {
    cursor: default;
    width: 85px;
    position: relative;
}

.picture .tooltip {
    width: fit-content;
    cursor: pointer;
    position: absolute;
    bottom: 0;
    right: 0;
    color: black;
    background-color: #E8E8E8;
    padding: 8px;
    aspect-ratio: 1/1;
    border-radius: 20px;
    transition: all .2s ease-in-out;
    display: flex;
}

body.dark-mode .tooltip {
    background-color: #373737;
    color: white;
}

.picture .tooltip svg {
    font-size: 10px;
}

.ai_activity {
    flex: 1;
    display: flex;
    gap: 30px;
}

.others {
    width: 100%;
    height: fit-content;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    gap: 30px;
    overflow: auto;
    border-radius: 5px !important;
}

.others:last-child {
    background-color: #ececec;
}

body.dark-mode .others:last-child {
    background-color: #373737;
}

.others:first-child {
    flex: 1;
}

.others:last-child {
    flex: 2;
}

.others canvas, .others div {
    background-color: #E8E8E8;
    border-radius: 5px !important;
    width: 100% !important;
    max-height: 350px;
    min-height: 100px;
    display: flex;
    justify-content: center;
    align-items: center;
}

body.dark-mode .others canvas, body.dark-mode .others div {
    background-color: #373737;
}

@media screen and (max-width: 600px) {
    .nav {
        padding: 15px 20px 15px 20px;
    }
}
</style>