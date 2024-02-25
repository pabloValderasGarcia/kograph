<script>
// import axios from 'axios';
import { notify } from 'notiwind';
import { mapState, mapMutations } from 'vuex';
export default {
    name: 'SearcherItem',
    data() {
        return {
            clicked: false,
            running: false,
            recognition: null
        }
    },
    mounted() {
        document.addEventListener('click', this.close);
        this.initializeRecognition();
        this.$emit('clear-search', () => {
            this.setSearchValue('');
        });
    },
    beforeUnmount() {
        document.removeEventListener('click', this.close);
    },
    computed: {
        ...mapState(['isLoading', 'filesData', 'originalFilesData']),
        searchValue: {
            get() {
                return this.$store.state.searchValue;
            },
            set(value) {
                this.setSearchValue(value);
            }
        }
    },
    methods: {
        ...mapMutations(['setSearchValue', 'setIsLoading']),
        // Método para controlar el padding de la lupa del input
        close(e) {
            if (!this.$el.contains(e.target)) {
                this.clicked = false;
            }
        },
        // Método para limpiar el input
        clean() {
            this.setSearchValue('');
            this.search();
        },
        // Método para hacer la petición con un valor de búsqueda al servidor
        async search() {
            try {
                this.setIsLoading(true);
                const searchValue = this.searchValue.toLowerCase().trim(); // Convertir a minúsculas y quitar espacios adicionales
                const matchingFiles = this.originalFilesData.filter(file => {
                    return Object.values(file).some(value => {
                        if (!value) return false;
                        if (typeof value === "string") {
                            return value.toLowerCase().includes(searchValue);
                        }
                        return false;
                    });
                });
                this.$emit('search-results', { 'value': searchValue !== '', 'data': matchingFiles });
            } catch (error) {/**/}
        },
        // Método para iniciar el reconocimiento de audio (no IA)
        initializeRecognition() {
            try {
                // Creación de objeto de reconocimiento
                this.recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
                this.recognition.maxAlternatives = 1; // Obtener una única alternativa

                let interimTranscript = '';

                this.recognition.onresult = (event) => {
                    const result = event.results[event.results.length - 1];
                    if (result.isFinal) {
                        // Se ha completado una palabra, procesarla
                        interimTranscript += result[0].transcript + ' ';
                        interimTranscript = this.replaceSpokenWords(interimTranscript);
                        this.setSearchValue(interimTranscript.trim().toLowerCase());
                        this.search();
                        interimTranscript = ''; // Reiniciar para la siguiente palabra
                    } else {
                        // Resultado intermedio, seguir acumulando palabras
                        interimTranscript += result[0].transcript;
                    }
                };
                this.recognition.onstart = () => {
                    this.running = true;
                };
                this.recognition.onend = () => {
                    this.running = false;

                    // Reiniciar el reconocimiento después de un corto tiempo
                    setTimeout(() => {
                        if (this.running && !this.recognition.startTimestamp) {
                            this.recognition.start();
                        }
                    }, 500);
                };
            } catch (error) {/**/}
        },
        // Método para permitir el audio e iniciarlo o pararlo
        async speak() {
            try {
                if (!this.running) {
                    await navigator.mediaDevices.getUserMedia({ audio: true });
                    this.recognition.start();
                    this.running = true;
                }
            } catch (error) {
                notify({
                    group: "foo",
                    title: "Error",
                    text: 'Permission denied by user.',
                    type: "error"
                }, 4000);
            }
        },
        // Método para comandos de voz
        replaceSpokenWords(text) {
            // Diccionario de reemplazos
            const replacements = {
                'pon comilla simple': '\'',
                'put single quote': '\'',
                'pon comilla doble': '"',
                'put quote': '"',
                'pon punto': '.',
                'put dot': '.',
                'pon interrogante': '?',
                'put question mark': '?',
                'pon exclamación': '!',
                'put exclamation': '!',
                'pon almohadilla': '#',
                'pon hashtag': '#',
                'put hashtag': '#',
                'pon arroba': '@',
                'put at': '@',
                'pon coma': ',',
                'put comma': ',',
                'pon barra baja': '_',
                'put underscore': '_',
                'pon guión': '-',
                'put dash': '-',
            };

            // Realizar los reemplazos
            Object.entries(replacements).forEach(([word, replacement]) => {
                const regex = new RegExp(`\\b${word}\\b`, 'gi');
                text = text.replace(regex, replacement).trim();
            });

            return text;
        }
    },
}
</script>

<template>
    <div class="searcher">
        <font-awesome-icon icon="magnifying-glass" class="search_icon" v-if="!clicked" />
        <input v-model="searchValue" name="search" class="input_searcher" :class="{ '!pl-[25px]': clicked }"
            placeholder="Explore your memories" @input="search" id="input_searcher" @click="clicked = true"/>
        <div class="tooltip audio_icon" :class="{ running: running, 'pr-[25px]': searchValue.length > 0 }" @click="speak" v-if="!isLoading">
            <font-awesome-icon icon="microphone"/>
            <p>Microphone&nbsp;search</p>
        </div>
        <div class="tooltip clean_icon" v-if="searchValue.length > 0" @click="clean">
            <font-awesome-icon icon="xmark"/>
            <p>Cancel</p>
        </div>
    </div>
</template>

<style scoped>
.searcher {
    position: relative;
    user-select: none;
    flex: 1;
}

.input_searcher {
    width: 100%;
    box-sizing: border-box;
    outline: none;
    border: none;
    border-radius: 20px !important;
    background-color: #ececec;
    padding: 10px 25px 10px 50px;
    font-size: 16px;
}

body.dark-mode .input_searcher {
    color: white !important;
    background-color: #373737 !important;
}

.search_icon {
    position: absolute;
    left: 20px;
    top: 50%;
    transform: translateY(-55%);
    opacity: .6;
    pointer-events: none;
}

.clean_icon {
    cursor: pointer;
    position: absolute !important;
    right: 20px;
    top: 29%;
}

.audio_icon {
    cursor: pointer;
    position: absolute !important;
    right: 20px;
    top: 30%;
}

.running svg {
    cursor: not-allowed;
    color: #318ba7;
}

.tooltip {
    position: relative;
}

.tooltip p {
	width: auto;
	border-radius: 5px;
	padding: 8px 15px;
	position: absolute;
	bottom: -40px;
	right: 0;
	opacity: 0;
	transition: opacity .3s;
	background-color: #d7d7d7;
    pointer-events: none;
}

body.dark-mode .tooltip p {
	background-color: #373737;
}

.tooltip:hover p {
	opacity: 1;
}

</style>