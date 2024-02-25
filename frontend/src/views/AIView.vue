<script>
import L from 'leaflet';
import axios from 'axios';
import EXIF from 'exif-js';
import 'leaflet/dist/leaflet.css';
import { mapState, mapMutations } from 'vuex';
import 'leaflet-fullscreen/dist/Leaflet.fullscreen.js';
import 'leaflet-fullscreen/dist/leaflet.fullscreen.css';
import '@drustack/leaflet.resetview/dist/L.Control.ResetView.min.css';
import '@drustack/leaflet.resetview/dist/L.Control.ResetView.min.js';
export default {
    name: 'AIView',
    async mounted() {
        // Obtención ficheros
        if (this.originalFilesData.length == 0) {
            const token = localStorage.getItem('access');
            const response = await axios.post(`${process.env.VUE_APP_SERVER_URL}/file/get/`, {
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            });
            this.setOriginalFilesData(response.data);
        }

        // Iniciar mapa
        if (!this.aiMap) this.initMap();
        else {
            // Si ya está iniciado, reemplazar el anterior mapa por el nuevo para buena carga al volver desde otro componente
            let oldMap = document.getElementById('map');
            oldMap.parentNode.replaceChild(this.aiMapElement, oldMap);
        }
    },
    beforeUnmount() {
        // Guardar elemento mapa antes de desmontar para almacenarlo en store y tenerlo al volver desde otro componente
        this.setAIMapElement(document.getElementById('map'));
    },
    updated() {
        // Invalidar size para el buen ajuste del mapa al contenedor
        if (this.aiMap) this.aiMap.invalidateSize();
    },
    computed: {
        ...mapState(['originalFilesData', 'aiMap', 'aiMapElement'])
    },
    methods: {
        ...mapMutations(['setOriginalFilesData', 'setAIMap', 'setAIMapElement']),
        // Método para iniciar el mapa
        async initMap() {
            // Crear capas
            var osm = L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
                maxZoom: 20,
                attribution: '&copy; OpenStreetMap | The locations of the photos to be shown may not be entirely true'
            });
            var streetsLayer = L.tileLayer('http://{s}.google.com/vt/lyrs=m&x={x}&y={y}&z={z}',{
                maxZoom: 20,
                subdomains:['mt0','mt1','mt2','mt3'],
                attribution: '&copy; Google Maps | The locations of the photos to be shown may not be entirely true'
            });
            var hybridLayer = L.tileLayer('http://{s}.google.com/vt/lyrs=s,h&x={x}&y={y}&z={z}',{
                maxZoom: 20,
                subdomains:['mt0','mt1','mt2','mt3'],
                attribution: '&copy; Google Maps | The locations of the photos to be shown may not be entirely true'
            });
            var satelliteLayer = L.tileLayer('http://{s}.google.com/vt/lyrs=s&x={x}&y={y}&z={z}',{
                maxZoom: 20,
                subdomains:['mt0','mt1','mt2','mt3'],
                attribution: '&copy; Google Maps | The locations of the photos to be shown may not be entirely true'
            });
            var terrainLayer = L.tileLayer('http://{s}.google.com/vt/lyrs=p&x={x}&y={y}&z={z}',{
                maxZoom: 20,
                subdomains:['mt0','mt1','mt2','mt3'],
                attribution: '&copy; Google Maps | The locations of the photos to be shown may not be entirely true'
            });

            // Crear mapa
            var map = L.map('map', {
                center: [44, 11],
                zoom: 2,
                minZoom: 2,
                maxBounds: L.latLngBounds(L.latLng(-90, -180), L.latLng(90, 180)), // Límites del mundo
                layers: [osm]
            });
            var baseMaps = {
                "OpenStreetMap": osm,
                "Google Streets": streetsLayer,
                "Google Hybrid": hybridLayer,
                "Google Satellite": satelliteLayer,
                "Google Terrain": terrainLayer,
            };

            // Crear control de capas
            L.control.layers(baseMaps).addTo(map);

            // Agregar control para pantalla completa
            L.control.fullscreen({
                position: 'topleft'
            }).addTo(map);

            // Agregar control para reset
            L.control.resetView({
                position: "topright",
                latlng: L.latLng([44, 11]),
                zoom: 2,
                title: 'Reset view'
            }).addTo(map);

            // Array de coordenadas de los marcadores
            const markers = [
                // { id: 2445, file: '/files/ds2.jpg', title: '1708703829918.jpg' },
            ];
            // const markers = this.originalFilesData;
            
            // Creación de iconos de ficheros
            var vm = this;
            markers.forEach(marker => {
                var img = new Image();
                img.src = `${process.env.VUE_APP_SERVER_URL}${marker.file}`;
                img.onload = async function() {
                    // Marcador mostrado en mapa
                    EXIF.getData(this, async function() {
                        var lat = EXIF.getTag(this, "GPSLatitude");
                        var lng = EXIF.getTag(this, "GPSLongitude");

                        // Convertir las coordenadas DMS a decimal u obtener coordenadas con IA en caso contrario
                        if (lat && lng) {
                            // Convertir latitud y longitud de grados, minutos y segundos a decimal
                            var latRef = EXIF.getTag(this, "GPSLatitudeRef") || "N";  
                            var lngRef = EXIF.getTag(this, "GPSLongitudeRef") || "W";
                            lat = (lat[0] + lat[1]/60 + lat[2]/3600) * (latRef == "N" ? 1 : -1);
                            lng = (lng[0] + lng[1]/60 + lng[2]/3600) * (lngRef == "W" ? -1 : 1);

                            // Crear y configurar el marcador
                            vm.createMarker(img, lat, lng, marker);
                        } else {
                            try {
                                // Leer la imagen desde la URL
                                const imageResponse = await axios.get(`${process.env.VUE_APP_SERVER_URL}${marker.file}`, { responseType: 'blob' });
                                
                                // Convertir los datos binarios de la imagen a base64
                                const reader = new FileReader();
                                reader.readAsDataURL(imageResponse.data);
                                reader.onloadend = async function() {
                                    // Obtener solo la parte de los datos base64
                                    const imgPath = reader.result.split(',')[1];

                                    // Preparar el formulario con el token y la imagen codificada en base64
                                    const formData = new FormData();
                                    formData.append('TOKEN', 'PY7RBKPH6Q0U4VWDRHFC');
                                    formData.append('IMAGE', imgPath);

                                    // Enviar la solicitud POST a Picarta.ai
                                    const response = await axios.post('https://picarta.ai/classify', formData, {
                                        headers: {
                                            'Content-Type': 'application/json'
                                        }
                                    });
                                    
                                    // Obtener latitud y longitud de la respuesta
                                    lat = response.data.ai_lat;
                                    lng = response.data.ai_lon;

                                    // Crear y configurar el marcador
                                    vm.createMarker(img, lat, lng, marker, response.data);
                                };
                            } catch (error) {/**/}
                        }
                    });
                }
            });
            vm.setAIMap(map);
        },
        // Método para crear un marker del mapa
        createMarker(img, lat, lng, marker, data=null) {
            // Crear el marcador
            var vm = this;
            var markerIcon = L.marker([lat, lng], {
                autoPopup: false
            }).addTo(this.aiMap);

            // Configurar el icono del marcador
            var iconSize = [img.width * (40 / img.height), 40];
            markerIcon.setIcon(L.icon({
                iconUrl: `${process.env.VUE_APP_SERVER_URL}${marker.file}`,
                iconSize: iconSize,
                iconAnchor: [iconSize[0] / 2, iconSize[1]],
                popupAnchor: [0, -iconSize[1]]
            }));

            // Asociar pop-up con el marcador
            var popupContent = document.createElement('p');
            if (data) {
                popupContent.innerHTML = `<b class="bold">Country: </b> ${data.ai_country}<br/><b class="bold">Province: </b> ${data.province}<br/><b class="bold">City: </b> ${data.city}<br/><b class="bold">File: </b>`;
            } else {
                popupContent.innerHTML = `<b class="bold">File: </b>`;
            }

            // Crear un nuevo span
            var spanElement = document.createElement('span');
            spanElement.textContent = marker.title;
            spanElement.style.color = 'blue';
            spanElement.style.cursor = 'pointer';
            
            // Agregar el evento de clic al nuevo span
            spanElement.addEventListener('click', function() {
                vm.$router.push(`/file/${marker.id}`);
            });
            
            // Anidar el nuevo span dentro del popupContent
            popupContent.appendChild(spanElement);
            popupContent.style.margin = '0';

            // Poner texto en marcador
            markerIcon.bindPopup(popupContent, {closeButton: false});
            markerIcon.on('click', function() {
                // Verificar si el popup está abierto
                if (!markerIcon.getPopup().isOpen()) markerIcon.closePopup();
                else markerIcon.openPopup();
            });
        }
    }
}
</script>

<template>
    <div class="ai_powered">
        <div></div>
        <div id="map"></div>
    </div>
</template>

<style >
    .ai_powered {
        box-sizing: border-box;
        width: auto;
        height: 80vh;
        background-color: #ececec;
        margin: 0 30px;
        border-radius: 5px;
        display: flex;
    }
    body.dark-mode .ai_powered {
        background-color: #373737;
    }
    .bold {
        font-weight: bold;
    }

    /* AI CATEGORIES */
    
    /* AI MAP */
    #map {
        position: relative;
        z-index: 0;
        border-radius: 5px;
        flex: 1;
        height: 100%;
    }
    /* POPUPS */
    .leaflet-popup-content {
        margin: 6px 10px !important;
    }
    .leaflet-popup-content-wrapper {
        border-radius: 0 !important;
    }
    /* LEAYERS CONTROL */
    .leaflet-control-layers-expanded {
        padding: 12px !important;
    }
    .leaflet-control-layers-base {
        display: flex;
        flex-direction: column;
        gap: 7px;
    }
    .leaflet-control-layers label > span {
        display: flex;
        align-items: center;
        gap: 6px;
    }
    .leaflet-control-layers-selector {
        padding: unset !important;
        margin-top: 0 !important;
    }
    .leaflet-control-layers label > span > span {
        line-height: normal !important;
    }
</style>