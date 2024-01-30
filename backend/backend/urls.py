# | ---------------------------------------------------------------------- |
# | ---------------------- IMPORTACIONES NECESARIAS ---------------------- |
# | ---------------------------------------------------------------------- |

from api.views import options_view, GetAlbums, CreateAlbum, DeleteAlbum, GetFiles, UploadFile, DeleteFile, SearchPerson, ShowFile, UpdateFile, ValidateLinkView, CheckEmail, PasswordResetView
from django.conf.urls.static import static
from django.urls import path, include
from django.contrib import admin
from django.conf import settings

# | -------------------------------------------------- |
# | ---------------------- URLS ---------------------- |
# | -------------------------------------------------- |

urlpatterns = [
    # ADMIN y OPTIONS
    path('admin/', admin.site.urls),
    path('options/', options_view),
    # ALBUM
    path('album/get/', GetAlbums.as_view(), name='get_albums'),
    path('album/create/', UploadFile.as_view(), name='create_album'),
    path('album/delete/', DeleteFile.as_view(), name='delete_album'),
    # FILE
    path('file/get/', GetFiles.as_view(), name='get_files'),
    path('file/upload/', UploadFile.as_view(), name='upload_file'),
    path('file/delete/', DeleteFile.as_view(), name='delete_file'),
    path('file/search_person/', SearchPerson.as_view(), name='search_person'),
    path('file/show/<int:file_id>/', ShowFile.as_view(), name='show_file'),
    path('file/update/<int:pk>/', UpdateFile.as_view(), name='update_file'),
    # EMAIL
    path('validate_link/', ValidateLinkView.as_view(), name='validate_link'),
    path('auth/users/check_email/', CheckEmail.as_view(), name='check_email'),
    path('auth/users/reset_password_confirm/<str:uid>/<str:token>/', PasswordResetView.as_view(), name='password_reset_confirm'),
    # AUTH
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
]

# Servir archivos estáticos en modo DEBUG
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)