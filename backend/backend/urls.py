from django.contrib import admin
from django.urls import path, include
from api.views import options_view, ValidateLinkView, CheckEmail, PasswordResetView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('options/', options_view),
    path('validate_link/', ValidateLinkView.as_view(), name='validate_link'),
    path('auth/users/check_email/', CheckEmail.as_view(), name='check_email'),
    path('auth/users/reset_password_confirm/<str:uid>/<str:token>/', PasswordResetView.as_view(), name='password_reset'),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
]