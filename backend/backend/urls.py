# | ---------------------------------------------------------------------- |
# | ---------------------- IMPORTACIONES NECESARIAS ---------------------- |
# | ---------------------------------------------------------------------- |

from api.views import options_view, UploadFile, serve_protected_file, AllImages, ValidateLinkView, CheckEmail, PasswordResetView
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
    # IMAGE
    path('file/upload/', UploadFile.as_view(), name='upload_file'),
    path('file/get_all/', AllImages.as_view(), name='all_images'),
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