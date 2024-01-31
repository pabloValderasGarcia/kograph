# | ---------------------------------------------------------------------- |
# | ---------------------- IMPORTACIONES NECESARIAS ---------------------- |
# | ---------------------------------------------------------------------- |

from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth.tokens import default_token_generator    
from rest_framework.parsers import MultiPartParser, FormParser
from djoser.serializers import PasswordResetConfirmSerializer
from django.contrib.auth.decorators import login_required
from moviepy.video.io.VideoFileClip import VideoFileClip
from backend.serializers import PasswordResetSerializer
from rest_framework.generics import UpdateAPIView
from templated_mail.mail import BaseEmailMessage
from rest_framework.permissions import AllowAny
from rest_framework.exceptions import Throttled
from backend.serializers import FileSerializer
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.http import Http404, FileResponse
from rest_framework.response import Response
from rest_framework.views import APIView
from .apps import rekognition_client
from django.core.cache import cache
from django.utils import timezone
from rest_framework import status
from djoser.conf import settings
from .models import Album, File
from datetime import timedelta
from djoser import utils
import backend.settings
from io import BytesIO
from PIL import Image
import numpy as np
import imageio
import uuid
import re
import os

# Obtener información sobre los métodos HTTP
@api_view(['OPTIONS'])
@permission_classes([AllowAny])
def options_view():
    return Response()

# | ---------------------------------------------------------------- |
# | ---------------------- EMAIL Y CONTRASEÑA ---------------------- |
# | ---------------------------------------------------------------- |

# Vista para enviar enlace de activación de cuenta
class ActivationAccount(BaseEmailMessage):
    template_name = "email/activation_account.html"

    def get_context_data(self):
        context = super().get_context_data()

        # Obtención de parámetros necesarios para el mensaje del correo
        user = context.get("user")
        context["uid"] = utils.encode_uid(user.pk)
        context["token"] = default_token_generator.make_token(user)
        context["url"] = settings.ACTIVATION_URL.format(**context)
        context["domain"] = os.getenv("FRONTEND_BASE_URL").split('://', 1)[-1]
        context["site_name"] = os.getenv("APP_NAME")

        return context

# Vista para enviar enlace de reseteo de contraseña
class PasswordResetEmail(BaseEmailMessage):
    template_name = "email/password_reset.html"

    def get_context_data(self):
        context = super().get_context_data()

        # Obtención de parámetros necesarios para el mensaje del correo
        user = context.get("user")
        user_id = user.pk
        
        # Verificar que el correo ya ha sido enviado para evitar ataques DDoS
        last_reset_email_time = cache.get(f'reset_email_sent_{user_id}')
        if last_reset_email_time:
            time_difference = timezone.now() - last_reset_email_time
            if time_difference.total_seconds() < 300:
                raise Throttled(detail='Please, wait approximately 5 minutes from your last sended email.')
        
        # Obtención de parámetros necesarios para el mensaje del correo
        context["uid"] = utils.encode_uid(user.pk)
        context["token"] = default_token_generator.make_token(user)
        context["url"] = settings.PASSWORD_RESET_CONFIRM_URL.format(**context)
        context["domain"] = os.getenv("FRONTEND_BASE_URL").split('://', 1)[-1]
        context["site_name"] = os.getenv("APP_NAME")

        # Guardamos en cache el tiempo que ha pasado desde que el correo fue enviado (para comparar arriba)
        cache.set(f'reset_email_sent_{user.pk}', timezone.now())
        
        return context
        
# Vista para verificar el reseteo de contraseña en frontend
class PasswordResetView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        # Usamos el serializador de contraseña
        serializer = PasswordResetSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Iniciamos las variables necesarias
        new_password = request.data.get('new_password')
        re_new_password = request.data.get('re_new_password')
        uid = kwargs.get('uid')
        
        # Verificamos si el usuario está autenticado
        if self.request.user.is_authenticated:
            user = self.request.user
        else:
            user = get_object_or_404(get_user_model(), pk=uid)

        # Verificamos si ambas contraseñas son iguales
        if new_password != re_new_password:
            return Response({'detail': 'Passwords do not match'}, status=status.HTTP_400_BAD_REQUEST)

        # Guardamos contraseña y usuario
        user.set_password(new_password)
        user.save()

        return Response({'detail': 'Password reset successfully.'}, status=status.HTTP_200_OK)
    
# Vista para verificar que existe el usuario con x email registrado
class CheckEmail(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def get(self, request):
        # Iniciamos las variables necesarias y comprobamos si existe
        User = get_user_model()
        email = request.GET.get('email')
        user = User.objects.filter(email=email).exists()
        if user:
            return Response(True)
        else:
            return Response(False)
        
# Vista para verificar enlaces válidos
class ValidateLinkView(APIView):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.token_generator = default_token_generator

    def get(self, request):
        # Iniciamos las variables necesarias
        uid = request.GET.get('uid')
        token = request.GET.get('token')

        # Verificamos si el token ha sido usado (a través de caché)
        activation_token_used = cache.get('activation_token_used')
        if activation_token_used:
            return Response({'detail': 'Invalid reset link.'}, status=status.HTTP_400_BAD_REQUEST)
        cache.set('activation_token_used', True)

        # A través de serializadores comprobamos que sea válido
        serializer = PasswordResetConfirmSerializer(
            data={'uid': uid, 'token': token, 'new_password': 'temp_password'},
            context={'request': request, 'view': self, 'token_generator': self.token_generator}
        )
        if serializer.is_valid():
            return Response({'detail': 'Reset link is valid.'}, status=status.HTTP_200_OK)
        else:
            return Response({'detail': 'Invalid reset link.'}, status=status.HTTP_400_BAD_REQUEST)
        
# | -------------------------------------------------------------- |
# | ---------------------- MANEJO DE ALBUMS ---------------------- |
# | -------------------------------------------------------------- |
        
# Vista para conseguir álbums
class GetAlbums(APIView):
    def get(self, request):
        # Iniciamos variables necesarias
        user_id = request.user.id
        user_albums = Album.objects.filter(user_id=user_id)
        serializer = FileSerializer(user_albums, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

# Vista para crear álbum
class CreateAlbum(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request):
        # Iniciamos variables necesarias
        user_id = str(request.user.id)
        file_data = request.FILES.get('file')
        title = str(request.data.get('title')) + '_' + str(uuid.uuid1())
        type = request.data.get('type')
        origin_created_at = request.data.get('origin_created_at')

        # Verificamos si el archivo es una imágen/vídeo y no es duplicado
        existing_files = File.objects.filter(user=request.user)
        new_file_data = file_data.read()
        for existing_file in existing_files:
            if existing_file.is_duplicate(new_file_data):
                return Response({'detail': 'File is a duplicate and cannot be uploaded.'}, status=status.HTTP_400_BAD_REQUEST)
            
        serializer = FileSerializer(data={'user': user_id, 'file': file_data, 'title': title, 'type': type, 'origin_created_at': origin_created_at})
        
        # Verificamos que sea válido
        if serializer.is_valid() and (type == 'video' or type == 'image'):
            file_instance = serializer.save()

            # Creación de miniatura en caso de vídeo
            if type == 'video':
                # Reemplazamos los demás caractéres por ''
                file_basename = os.path.basename(re.sub(r'[^\w.\s-]', '', file_data.name))

                # Reemplazamos espacios por '_'
                file_basename = re.sub(r'\s', '_', file_basename)
                file_path = os.path.join(backend.settings.BASE_DIR, 'files', file_basename)

                # Generamos el thumbnail del fichero
                thumbnail_path = generate_thumbnail(file_instance, file_path, file_basename)

                # Actualizamos el fichero con el campo thumbnail
                file_instance = File.objects.get(title=title)
                file_instance.thumbnail = thumbnail_path
                file_instance.save()

            return Response({'detail': 'File/s uploaded successfully.'}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Vista para eliminar álbums según ids
class DeleteAlbum(APIView):
    def post(self, request, *args, **kwargs):
        # Recogemos los ids
        album_ids = request.data.get('album_ids', [])
        
        # Verificamos que existan ids
        if not album_ids:
            return Response({'detail': 'No file IDs provided'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Filtra los archivos a eliminar por IDs
            albums_to_delete = Album.objects.filter(id__in=album_ids)
            for album in albums_to_delete:
                # Elimina el archivo
                album.delete()

            return Response({'detail': 'Album/s deleted successfully'}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'detail': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        
# | -------------------------------------------------------------------------------- |
# | ---------------------- MANEJO DE FICHEROS (imagen, vídeo) ---------------------- |
# | -------------------------------------------------------------------------------- |

# Función para conseguir imagen de forma privada (en producción)
@login_required
def serve_protected_file(request, file_path):
    user = request.user

    # File correspondiente al archivo solicitado
    file = get_object_or_404(File, file="files/" + file_path)

    # Verifica si el usuario tiene permisos para acceder al archivo
    if file.user != user:
        raise Http404("You don't have access to this file.")

    # Construye la ruta completa al archivo
    full_path = os.path.join(settings.MEDIA_ROOT, file.file.name)

    # Sirve el archivo usando FileResponse
    response = FileResponse(open(full_path, 'rb'), content_type='application/octet-stream')
    response['Content-Disposition'] = f'attachment; filename={file_path}'

    return response
        
# Vista para conseguir ficheros
class GetFiles(APIView):
    def post(self, request):
        # Iniciamos variables necesarias
        search_value = request.data.get('search', '')
        user_id = request.user.id
        user_files = File.objects.filter(user_id=user_id)
        
        # Si está buscando devolvemos los ficheros donde algunos de sus campos incluya el valor x
        if search_value:
            user_files = user_files.filter(title__icontains=search_value) | user_files.filter(description__icontains=search_value)
        
        serializer = FileSerializer(user_files, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
# Vista para subir archivo
class UploadFile(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request):
        # Iniciamos variables necesarias
        user_id = str(request.user.id)
        file_data = request.FILES.get('file')
        title = request.data.get('title')
        type = request.data.get('type')
        origin_created_at = request.data.get('origin_created_at')

        # Verificamos si el archivo es una imágen/vídeo y no es duplicado
        existing_files = File.objects.filter(user=request.user)
        new_file_data = file_data.read()
        for existing_file in existing_files:
            if existing_file.is_duplicate(new_file_data):
                return Response({'detail': 'File is a duplicate and cannot be uploaded.'}, status=status.HTTP_400_BAD_REQUEST)
            
        serializer = FileSerializer(data={'user': user_id, 'file': file_data, 'title': title, 'type': type, 'origin_created_at': origin_created_at})
        
        # Verificamos que sea válido
        if serializer.is_valid() and (type == 'video' or type == 'image'):
            file_instance = serializer.save()

            # Creación de miniatura en caso de vídeo
            if type == 'video':
                # Reemplazamos los demás caractéres por ''
                file_basename = os.path.basename(re.sub(r'[^\w.\s-]', '', file_data.name))

                # Reemplazamos espacios por '_'
                file_basename = re.sub(r'\s', '_', file_basename)
                file_path = os.path.join(backend.settings.BASE_DIR, 'files', file_basename)

                # Generamos el thumbnail del fichero
                thumbnail_path = generate_thumbnail(file_instance, file_path, file_basename)

                # Actualizamos el fichero con el campo thumbnail
                file_instance.thumbnail = thumbnail_path
                file_instance.save()

            return Response({'detail': 'File/s uploaded successfully.'}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
# Función para generar una miniatura de un vídeo
def generate_thumbnail(file_instance, video_path, video_basename):
    try:
        # Variables necesarias
        clip = VideoFileClip(video_path)
        thumbnail = clip.get_frame(0)
        thumbnail_path = str(video_basename) + str(uuid.uuid4())

        # Guardar la miniatura como imagen
        thumbnail_dir = os.path.join(backend.settings.BASE_DIR, 'thumbnails')
        if not os.path.exists(thumbnail_dir):
            os.makedirs(thumbnail_dir)
        thumbnail_path_full = os.path.join(thumbnail_dir, thumbnail_path + ".png")
        imageio.imwrite(thumbnail_path_full, np.uint8(thumbnail))

        # Guardar la duración del vídeo
        file_instance.duration = timedelta(seconds=int(clip.duration))
        file_instance.save()

        return thumbnail_path
    except Exception as e:
        print(f"Error generating thumbnail: {str(e)}")
        return None

# Vista para eliminar ficheros según su id
class DeleteFile(APIView):
    def post(self, request, *args, **kwargs):
        # Recogemos los ids
        file_ids = request.data.get('file_ids', [])
        
        # Verificamos que existan ids
        if not file_ids:
            return Response({'detail': 'No file IDs provided'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Filtra los archivos a eliminar por IDs
            files_to_delete = File.objects.filter(id__in=file_ids)
            for file in files_to_delete:
                # Elimina el archivo
                file.delete()

            return Response({'detail': 'File/s deleted successfully'}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'detail': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
# Vista para eliminar ficheros según sus ids
class ShowFile(APIView):
    def get(self, request, *args, **kwargs):
        # Recogemos el id
        file_id = self.kwargs.get('file_id')
        
        # Verificamos que exista el id
        if not file_id:
            return Response({'detail': 'No file ID provided'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Verificar que el objeto rekognition_client esté configurado
        if rekognition_client is None:
            return Response({'detail': 'Rekognition client not configured.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        try:
            # Conseguimos y devolvemos el fichero
            file = File.objects.get(id=file_id)
            serializer = FileSerializer(file)
            data = serializer.data.copy()
            if self.request.query_params.get('aws'):
                data['aws'] = {
                    'faces': get_faces_info(str(backend.settings.BASE_DIR) + '\\' + os.path.normpath(str(file.file))),
                    'labels': get_labels(str(backend.settings.BASE_DIR) + '\\' + os.path.normpath(str(file.file)))
                }
            return Response(data, status=status.HTTP_200_OK)

        except File.DoesNotExist:
            return Response({'detail': 'File not found'}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({'detail': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
# Vista para actualizar un fichero según su id
class UpdateFile(UpdateAPIView):
    queryset = File.objects.all()
    serializer_class = FileSerializer

    def update(self, request, *args, **kwargs):
        instance = self.get_object()

        # Obtener el campo y el nuevo valor desde los datos de la solicitud
        property = request.data.get('property')
        value = request.data.get('value')

        # Validar si el campo existe en el modelo
        if not hasattr(instance, property):
            return Response({'detail': 'Invalid field to update.'}, status=status.HTTP_400_BAD_REQUEST)

        # Actualizar el campo y guardar la instancia
        setattr(instance, property, value)
        instance.save()

        serializer = self.get_serializer(instance)
        return Response(serializer.data)

# Vista para encontrar ficheros con caras iguales
class SearchPerson(APIView):
    def post(self, request):
        user_id = request.user.id
        user_files = File.objects.filter(user_id=user_id)

        # Verificar que el objeto rekognition_client esté configurado
        if rekognition_client is None:
            return Response({'detail': 'Rekognition client not configured.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        # Obtener la información de las caras en el archivo objetivo
        file = request.FILES['files']
        file_bytes = file.read()

        # Buscar archivos que coincidan con las caras de file_target
        matching_files = find_matching_files(user_files, file_bytes)

        # Serializar y devolver la lista de archivos coincidentes
        matching_serializer = FileSerializer(matching_files, many=True)
        return Response(matching_serializer.data, status=status.HTTP_200_OK)
    
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
        file_faces_info = get_faces_info(str(backend.settings.BASE_DIR) + '\\' + os.path.normpath(str(file.file)))

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