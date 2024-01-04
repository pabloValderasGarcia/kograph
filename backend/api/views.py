from decouple import config
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth.tokens import default_token_generator    
from djoser.serializers import PasswordResetConfirmSerializer
from backend.serializers import PasswordResetSerializer
from templated_mail.mail import BaseEmailMessage
from rest_framework.permissions import AllowAny
from rest_framework.exceptions import Throttled
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from django.core.cache import cache
from django.utils import timezone
from rest_framework import status
from djoser.conf import settings
from djoser import utils
import os

@api_view(['OPTIONS'])
@permission_classes([AllowAny])
def options_view():
    return Response()

# AWS Credentials
aws_access_key_id = config('aws_access_key_id')
aws_secret_access_key = config('aws_secret_access_key')
aws_session_token = config('aws_session_token')
aws_region = config('aws_region')

User = get_user_model()

# Send activation account link
class ActivationAccount(BaseEmailMessage):
    template_name = "email/activation_account.html"

    def get_context_data(self):
        context = super().get_context_data()

        user = context.get("user")
        context["uid"] = utils.encode_uid(user.pk)
        context["token"] = default_token_generator.make_token(user)
        context["url"] = settings.ACTIVATION_URL.format(**context)
        context["domain"] = os.getenv("FRONTEND_BASE_URL").split('://', 1)[-1]
        context["site_name"] = os.getenv("APP_NAME")
        return context

# Send email to reset password
class PasswordResetEmail(BaseEmailMessage):
    template_name = "email/password_reset.html"

    def get_context_data(self):
        context = super().get_context_data()

        user = context.get("user")
        user_id = user.pk

        last_reset_email_time = cache.get(f'reset_email_sent_{user_id}')
        if last_reset_email_time:
            time_difference = timezone.now() - last_reset_email_time
            if time_difference.total_seconds() < 300:
                raise Throttled(detail='Please, wait approximately 5 minutes from your last request.')
        
        context["uid"] = utils.encode_uid(user.pk)
        context["token"] = default_token_generator.make_token(user)
        context["url"] = settings.PASSWORD_RESET_CONFIRM_URL.format(**context)
        context["domain"] = os.getenv("FRONTEND_BASE_URL").split('://', 1)[-1]
        context["site_name"] = os.getenv("APP_NAME")

        cache.set(f'reset_email_sent_{user.pk}', timezone.now())
        
        return context
        
# Reset password
class PasswordResetView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = PasswordResetSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        new_password = request.data.get('new_password')
        re_new_password = request.data.get('re_new_password')
        uid = kwargs.get('uid')
        
        if self.request.user.is_authenticated:
            user = self.request.user
        else:
            user = get_object_or_404(get_user_model(), pk=uid)

        if new_password != re_new_password:
            return Response({'detail': 'Passwords do not match'}, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(new_password)
        user.save()

        return Response({'detail': 'Password reset successfully.'}, status=status.HTTP_200_OK)
    
# Validate link
class ValidateLinkView(APIView):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.token_generator = default_token_generator
    def get(self, request):
        uid = request.GET.get('uid')
        token = request.GET.get('token')

        activation_token_used = cache.get('activation_token_used')
        if activation_token_used:
            return Response({'detail': 'Invalid reset link.'}, status=status.HTTP_400_BAD_REQUEST)
        cache.set('activation_token_used', True)

        serializer = PasswordResetConfirmSerializer(
            data={'uid': uid, 'token': token, 'new_password': 'temp_password'},
            context={'request': request, 'view': self, 'token_generator': self.token_generator}
        )
        if serializer.is_valid():
            return Response({'detail': 'Reset link is valid.'}, status=status.HTTP_200_OK)
        else:
            return Response({'detail': 'Invalid reset link.'}, status=status.HTTP_400_BAD_REQUEST)
        
# Check email is registered
class CheckEmail(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def get(self, request):
        email = request.GET.get('email')
        user = User.objects.filter(email=email).exists()
        if user:
            return Response(True)
        else:
            return Response(False)