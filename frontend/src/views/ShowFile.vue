<script>
import axios from 'axios';
import { notify } from 'notiwind';
export default {
	name: 'ShowFile',
    data() {
		return {
			width: null,
			height: null,
			file: null,
			initWidth: null,
			initHeight: null,
			showSideBar: true,
			isLoading: false,
			// AWS
			showAWS: false,
			awsButtonClicked: false,
			// Update
			titleText: null,
			descriptionText: null,
			editingTitle: false,
			editingDescription: false,
        }
    },
    async mounted() {
		window.addEventListener('resize', this.handleResize);

		// Obtenemos la información de la imagen
		const file_id = this.$route.params.id;
        if (file_id) {
			const response = await axios.get(`${process.env.VUE_APP_SERVER_URL}/file/show/${file_id}/`);
            this.file = response.data;
			this.titleText = this.file.title;
			this.descriptionText = this.file.description;
			document.title = `${this.file.title} - Kograph`;
        }
    },
	beforeUnmount() {
		window.removeEventListener('resize', this.handleResize);
	},
	updated() {
		// Verifica si el textarea existe y ajusta su altura
		if (this.$refs.textarea) {
			this.adjustTextareaHeight({
				target: this.$refs.textarea
			});
		}
	},
    computed: {
		// Obtiene la url entera del servidor de la imagen
		fullFileUrl() {
			return (file) => {
				return `${process.env.VUE_APP_SERVER_URL}${file.file}`;
            };
        },
		// Formatea la fecha de creación/modificación
		formattedDate() {
			const date = new Date(this.file.origin_created_at);
			const options = { month: 'long', day: 'numeric', year: 'numeric', hour: 'numeric', minute: 'numeric', hour12: true };
			return date.toLocaleDateString('en-US', options);
		},
		// Filtra AWSInfo para recoger las instancias y las ordena para el buen funcionamiento del tooltip
		filteredInstances() {
            return this.file.aws.labels.reduce((result, label) => {
				if (label.Instances && label.Instances.length > 0 && label.Confidence > 90) {
					result.push(
						...label.Instances.map(instance => ({
							name: label.Name,
							confidence: Math.round(label.Confidence) + '%',
							instance
						}))
					);
				}
				return result;
			}, []).sort((a, b) => {
				const sizeA = a.instance.BoundingBox.Width * a.instance.BoundingBox.Height;
				const positionA = a.instance.BoundingBox.Left + a.instance.BoundingBox.Top;
				const sizeB = b.instance.BoundingBox.Width * b.instance.BoundingBox.Height;
				const positionB = b.instance.BoundingBox.Left + b.instance.BoundingBox.Top;

				// Ordenar por tamaño y posición
				if (sizeA !== sizeB) {
					return sizeB - sizeA;
				} else {
					return positionB - positionA;
				}
			});
        }
    },
	methods: {
		// Métodos para editar x elemento (nombre, descripción...)
		editElement(property) {
			if (property === 'title') {
				this.editingTitle = !this.editingTitle;
			} else if (property === 'description') {
				this.editingDescription = !this.editingDescription;
			}
		},
		async updateElement(property, value) {
			try {
				if (value !== this.file[property]) {
					const response = await axios.put(`${process.env.VUE_APP_SERVER_URL}/file/update/${this.file.id}/`, { 
						property: property,
						value: value
					});
					this.file[property] = response.data[property];
					document.title = `${this.file.title} - Kograph`;
					
					notify({
						group: "foo",
						title: "Success",
						text: `Field '${property}' updated successfully.`,
						type: "success"
					}, 4000);

					if (property === 'title') {
						this.editingTitle = false;
					} else if (property === 'description') {
						this.editingDescription = false;
					}
				} else {
					notify({
						group: "foo",
						title: "Error",
						text: `Field '${property}' cannot have the same value.`,
						type: "error"
					}, 4000);
				}
            } catch (error) {
                notify({
                    group: "foo",
                    title: "Error",
                    text: `Failed to update '${property}'.`,
                    type: "error"
                }, 4000);
            }
		},
		// Método para mostrar toda la información recogida de AWS
		async showAWSTags() {
			if (!this.awsButtonClicked) {
				this.awsButtonClicked = true;
				this.isLoading = true;
				if (!this.file.aws) {
					this.handleResize();
					const response = await axios.get(`${process.env.VUE_APP_SERVER_URL}/file/show/${this.file.id}/?aws=true`);
					this.file = response.data;
					if (this.file.aws.faces && this.file.aws.labels) {
						this.showAWS = true;
						notify({
							group: "foo",
							title: "Success",
							text: "All possible tags shown.",
							type: "success"
						}, 4000);
					} else {
						notify({
							group: "foo",
							title: "Error",
							text: "No element detected.",
							type: "error"
						}, 4000);
					}
				} else {
					this.showAWS = !this.showAWS;
				}
				this.isLoading = false;
			} else if (this.file.aws) {
				this.showAWS = !this.showAWS;
			}
		},
		// Método para mostrar/ocultar la sidebar
		toggleSideBar() {
			const sidebar = document.getElementById('sidebar');
			if (sidebar) {
				if (sidebar.classList.contains('sidebar_hide')) {
					sidebar.classList.remove('sidebar_hide');
					sidebar.style.marginRight = 'unset';
					this.showSideBar = true;
				} else {
					this.handleResize();
					sidebar.classList.add('sidebar_hide');
					sidebar.style.marginRight = '-' + ((sidebar.offsetWidth/window.innerWidth)*100+5.8) + '%';
					this.showSideBar = false;
				}
			}
		},
		// Método para conseguir que la AWSInfo sea relativa a la imagen
		async handleResize() {
			const sidebar = document.getElementById('sidebar');
			if (sidebar) {
				if (sidebar.classList.contains('sidebar_hide')) {
					sidebar.style.marginRight = '-' + ((sidebar.offsetWidth/window.innerWidth)*100) + '%';
				}
			}

			if (this.file) {
				if (this.file.type === 'image') {
					// Conseguir ancho y alto de la imagen
					const element = new Image();
					element.src = this.fullFileUrl(this.file);
					await new Promise((resolve, reject) => {
						element.onload = resolve;
						element.onerror = reject;
					});
					this.width = element.width;
					this.height = element.height;

					// Conseguir que el AWS Info esté relativo a la imagen
					if (this.width && this.height) {
						const img = document.querySelector('.image_container img');
						var ratio = this.width / this.height;
						this.width = img.height * ratio;
						this.height = img.height;
						if (this.width > img.width && this.height) {
							this.width = img.width;
							this.height = img.width/ratio;
						}
						if (this.height < img.parentElement.offsetHeight) {
							if (!this.initHeight) this.initHeight = img.parentElement.offsetHeight;
							img.parentElement.style.height = 'fit-content';
						}
						if (this.width > img.parentElement.offsetWidth) {
							if (!this.initWidth) this.initWidth = img.parentElement.offsetWidth;
							img.parentElement.style.width = '100%';
						}
						if (this.initHeight) {
							if ((this.initHeight - 1 < this.height && this.height < this.initHeight + 1) || this.height > this.initHeight) {
								img.parentElement.style.height = '100%';
								img.parentElement.style.width = 'unset';
							}
						}
					}
				}
			}
		},
		// Método para conseguir los estilos de las etiquetas AWS
		getBoundingBoxStyle(boundingBox, prior=false) {
			return {
				'width': boundingBox.BoundingBox.Width * 100 + '%',
				'height': boundingBox.BoundingBox.Height * 100 + '%',
				'left': boundingBox.BoundingBox.Left * 100 + '%',
				'top': boundingBox.BoundingBox.Top * 100 + '%',
				'z-index': prior ? '99' : '',
			};
		},
		// Método para ajustar la altura del textarea
		adjustTextareaHeight(event) {
			const textarea = event.target;
			textarea.style.height = 'auto';
			textarea.style.height = `${textarea.scrollHeight}px`;
			textarea.style.minHeight = `${textarea.scrollHeight}px`;
		},
		// Método para colocar el tooltip en top 0 en caso de que "toque techo" con la página
		getTooltipStyle(element) {
			const boundingBoxTop = element.BoundingBox.Top * 100;
			const tooltipTop = boundingBoxTop <= 1 ? 0 : -42;

			return {
				'top': `${tooltipTop}px`,
			};
		}
	},
}
</script>

<template>
    <section v-if="file != null">
        <div>
			<div v-if="file.type == 'image'" class="image_container">
				<img :src="fullFileUrl(file)" class="select-none object-contain w-full min-h-fit h-full max-h-[100vh]" />
				<div v-if="showAWS && file.aws.labels && file.aws.faces" class="aws">
					<!-- LABELS -->
					<div v-for="(item, index) in filteredInstances" :key="index">
						<div class="aws_target tooltip" :style="getBoundingBoxStyle(item.instance)">
							<p :style="getTooltipStyle(item.instance)">{{ item.name }}</p>
						</div>
					</div>
					<!-- FACES -->
					<div v-for="(face, index) in file.aws.faces" :key="index">
						<div class="aws_target tooltip" :style="getBoundingBoxStyle(face, true)">
							<p :style="getTooltipStyle(face)">Face</p>
						</div>
					</div>
				</div>
			</div>
			<div class="buttons">
				<div class="left_buttons">
					<font-awesome-icon @click="this.$router.go(-1)" icon="arrow-left"/>
					<font-awesome-icon v-if="file.type == 'image'" @click="showAWSTags" :class="isLoading ? 'loading' : ''" :icon="isLoading ? 'spinner' : 'bolt'"/>
				</div>
				<font-awesome-icon @click="toggleSideBar" :icon="showSideBar ? 'xmark' : 'chevron-left'"/>
			</div>
			<video v-if="file.type == 'video'" :src="fullFileUrl(file)" controls></video>
		</div>
        <div id="sidebar">
			<div class="title">
				<p>INFORMATION</p>
			</div>
			<div class="info">
				<div>
					<div>
						<p><font-awesome-icon :icon="['far', 'image']"/>Name</p>
						<div class="flex gap-2">
							<font-awesome-icon v-if="editingTitle && titleText != file.title" class="cursor-pointer" @click="updateElement('title', titleText)" icon="floppy-disk"/>
							<font-awesome-icon class="cursor-pointer" @click="editElement('title')" :icon="editingTitle ? 'xmark' : 'pen-to-square'"/>
						</div>
					</div>
					<p v-if="!editingTitle">{{ file.title }}</p>
					<input v-model="titleText" v-if="editingTitle" @keyup.enter="updateElement('title', titleText)"/>
				</div>
				<div>
					<div>
						<p><font-awesome-icon icon="circle-info"/>Description</p>
						<div class="flex gap-2">
							<font-awesome-icon v-if="editingDescription && descriptionText != file.description" class="cursor-pointer" @click="updateElement('description', descriptionText)" icon="floppy-disk"/>
							<font-awesome-icon class="cursor-pointer" @click="editElement('description')" :icon="editingDescription ? 'xmark' : 'pen-to-square'"/>
						</div>
					</div>
					<p v-if="!editingDescription">{{ file.description ? file.description : 'None' }}</p>
					<textarea ref="textarea" v-model="descriptionText" v-if="editingDescription" @input="adjustTextareaHeight" @focus="adjustTextareaHeight" @keydown.enter.prevent="updateElement('description', descriptionText)"/>
				</div>
				<div>
					<div>
						<p><font-awesome-icon :icon="['far', 'clock']"/>Date</p>
					</div>
					<p>{{ formattedDate }}</p>
				</div>
				<div v-if="showAWS && file.aws.labels && file.aws.labels.length > 0">
					<div>
						<p><font-awesome-icon icon="hashtag"/>AI Tags</p>
					</div>
					<div class="aws_tags">
						<p v-for="(label, index) in file.aws.labels" :key="index">{{label.Name}}</p>
					</div>
				</div>
				<div v-if="showAWS && file.aws.labels && file.aws.labels.length == 0">
					<div>
						<p><font-awesome-icon icon="hashtag"/>AI Tags</p>
					</div>
					<div class="aws_tags">
						<p>None</p>
					</div>
				</div>
			</div>
		</div>
    </section>
</template>

<style scoped>
section {
	overflow-x: hidden;
    width: 100%;
    height: 100%;
    display: flex;
    position: absolute;
    top: 0;
    left: 0;
}
section > div:first-child {
	position: relative;
    flex: 4;
    width: 100%;
    height: 100%;
    background-color: black;
	display: flex;
	justify-content: center;
	align-items: center;
}
.buttons {
	width: 100%;
	position: absolute;
	top: 20px;
	display: flex;
	align-items: center;
	justify-content: space-between;
	padding: 0 20px;
	z-index: 9999999;
}
.buttons svg {
	aspect-ratio: 1/1;
	cursor: pointer;
	padding: 13px;
	border-radius: 50px;
	background-color: #ececec;
}
.buttons svg:hover {
	background-color: #d1d1d1;
}
body.dark-mode .buttons svg {
	background-color: #373737;
}
body.dark-mode .buttons svg:hover {
	background-color: #464646;
}
.left_buttons {
	display: flex;
	align-items: center;
	gap: 10px;
}
.image_container {
	position: relative;
	height: 100%;
	display: flex;
	justify-content: center;
	align-items: center;
	margin: 0 auto;
}
section > div:first-child video {
    width: 100%;
    height: 100%;
	object-fit: contain;
}
#sidebar {
	overflow-x: hidden;
	overflow-y: auto;
	max-height: 100vh;
	box-sizing: border-box;
	position: relative;
	width: 100%;
    flex: 1;
	padding: 35px;
	display: flex;
	flex-direction: column;
	gap: 40px;
	transition: all .3s ease-in-out;
}
.title {
	display: flex;
	align-items: center;
	gap: 20px;
}
.title svg {
	position: absolute;
	left: -65px;
	aspect-ratio: 1/1;
	cursor: pointer;
	padding: 13px;
	border-radius: 50px;
	background-color: #ececec;
}
.title svg:hover {
	background-color: #d1d1d1;
}
body.dark-mode .title svg {
    background-color: #373737;
}
body.dark-mode .title svg:hover {
    background-color: #464646;
}
.title p {
	font-weight: bold;
	user-select: none;
}
.info {
	display: flex;
	flex-direction: column;
	gap: 32px;
}
.info > div {
	display: flex;
	flex-direction: column;
	gap: 12px;
}
.info > div > div {
	display: flex;
	justify-content: space-between;
	align-items: center;
	gap: 15px;
}
.info > div > div > svg {
	width: fit-content;
	aspect-ratio: 1/1;
}
.info p:first-child {
	font-weight: bold;
	display: flex;
	align-items: center;
	gap: 10px;
}
.info p:last-child {
	line-height: 1.3em;
	overflow-wrap: break-word;
	word-break: break-all;
	display: flex;
	justify-content: space-between;
}
.aws {
	position: absolute;
	top: 0;
	left: 0;
	width: 100%;
	height: 100%;
}
.aws_target {
	position: absolute;
	border: 2px solid white;
	cursor: pointer;
}
.tooltip p {
	width: fit-content;
	border-radius: 5px;
	padding: 10px 15px;
	position: absolute;
	top: -42px;
	left: -2px;
	opacity: 0;
	transition: opacity .3s;
	background-color: white;
}
body.dark-mode .tooltip p {
	background-color: #242424;
}
.tooltip:hover p {
	opacity: 1;
}
@keyframes rotate {
	from {
		transform: rotate(0deg);
	}
	to {
		transform: rotate(360deg);
	}
}
.loading {
	animation: rotate 2s linear infinite;
}
.aws_tags {
	display: flex !important;
	flex-direction: row !important;
	align-items: center !important;
	justify-content: flex-start !important;
	flex-wrap: wrap;
	gap: 10px !important;
}
.aws_tags p {
	line-height: 1em !important;
	overflow-wrap: unset !important;
    word-break: unset !important;
	font-size: .8em;
	font-weight: normal !important;
	padding: 8px 15px;
	border: 1px solid #242424;
}
body.dark-mode .aws_tags p {
	border: 1px solid white;
}
</style>