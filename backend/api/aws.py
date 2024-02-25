from rest_framework.response import Response
from .apps import get_rekognition_client
from rest_framework import status
from django.conf import settings
from io import BytesIO
from PIL import Image
import os

rekognition_client = get_rekognition_client()

# Función para comprimir una imagen
def compress_image(image_bytes, quality=85):
    try:
        # Abrir la imagen desde bytes
        image = Image.open(BytesIO(image_bytes))

        # Convertir la imagen a modo de color RGB si es RGBA
        if image.mode == 'RGBA':
            image = image.convert('RGB')

        # Crear un buffer para la imagen comprimida
        compressed_image_buffer = BytesIO()

        # Guardar la imagen comprimida en el buffer
        image.save(compressed_image_buffer, format='JPEG', quality=quality)

        # Obtener los bytes de la imagen comprimida
        compressed_image_bytes = compressed_image_buffer.getvalue()

        return compressed_image_bytes

    except Exception as e:
        print(e)
        return None

# Función para conseguir los ficheros donde aparecen caras de un fichero
def find_matching_files(user_files, file_bytes):
    matching_files = []

    # Comprimimos el fichero y verificamos que exista
    compressed_image_bytes = compress_image(file_bytes)
    if not compressed_image_bytes:
        return Response({'detail': 'Invalid target image.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # Recorremos cada fichero del usuario para comprobar si x es igual
    for file in user_files:
        file_faces_info = get_faces_info(str(settings.BASE_DIR) + '\\' + os.path.normpath(str(file.file)))

        if file_faces_info is not None and len(file_faces_info) > 0:
            # Obtenemos bytes del fichero
            compressed_file_image_bytes = compress_image(file.file.read())
            
            try:
                # Utilizar rekognition_client para comparar las caras usando compare_faces
                comparison_response = rekognition_client.compare_faces(
                    TargetImage={
                        'Bytes': compressed_image_bytes
                    },
                    SourceImage={
                        'Bytes': compressed_file_image_bytes
                    }
                )

                # Verificar si hay coincidencias
                if any(match['Similarity'] >= 70.0 for match in comparison_response['FaceMatches']):
                    matching_files.append(file)
            except Exception as e:
                print(f"Error: {str(e)}")
                return None

    return matching_files

# Función para conseguir la información importante de cada cara de un fichero
def get_faces_info(file_path):
    try:
        with open(file_path, 'rb') as file:
            # Comprimir la imagen antes de enviarla
            compressed_image_bytes = compress_image(file.read())
            
            # Utilizar rekognition_client para obtener información sobre las caras en el archivo
            response = rekognition_client.detect_faces(
                Image={
                    'Bytes': compressed_image_bytes
                },
                Attributes=['ALL']
            )
                    
            # Extraer información relevante sobre las caras
            faces_info = []
            for face_detail in response['FaceDetails']:
                face_info = {
                    'BoundingBox': face_detail['BoundingBox'],
                    'Confidence': face_detail['Confidence'],
                    'Emotions': face_detail['Emotions'],
                }
                if face_info['Confidence'] >= 70.0:
                    faces_info.append(face_info)

            return faces_info

    except Exception as e:
        print(e)
        return None

# Función para conseguir etiquetas de una imagen
def get_labels(file_path):
    try:
        with open(file_path, 'rb') as file:
            # Comprimir la imagen antes de enviarla
            compressed_image_bytes = compress_image(file.read())
            
            # Utilizar rekognition_client para obtener etiquetas
            response = rekognition_client.detect_labels(
                Image={
                    'Bytes': compressed_image_bytes
                }
            )
                    
            return response['Labels']

    except Exception as e:
        print(e)
        return None