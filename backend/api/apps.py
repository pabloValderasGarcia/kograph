from django.apps import AppConfig
from decouple import config
import boto3

# | --------------------------------------------------------------------------- |
# | ---------------------- AWS (INTELIGENCIA ARTIFICIAL) ---------------------- |
# | --------------------------------------------------------------------------- |

# Configuración cliente AWS Rekognition
def configure_rekognition_client():
    global rekognition_client

    # AWS Credenciales
    aws_access_key_id = config('aws_access_key_id')
    aws_secret_access_key = config('aws_secret_access_key')
    aws_session_token = config('aws_session_token')
    aws_region = config('aws_region')

    try:
        rekognition_client = boto3.client('rekognition',
                            aws_access_key_id=aws_access_key_id,
                            aws_secret_access_key=aws_secret_access_key,
                            aws_session_token=aws_session_token,
                            region_name=aws_region)

        print("\033[92mCredentials configured correctly.\033[0m\n")

        # Devuelve el cliente rekognition
        return rekognition_client
    except Exception as e:
        # Si el error es por la existencia del bucket
        if hasattr(e, 'response') and hasattr(e.response, 'Error') and hasattr(e.response.Error, 'Code'):
            print("\033[91mERROR\033[0m")
        # Si el error es por la id errónea
        elif 'InvalidAccessKeyId' in str(e):
            print("\033[91mInvalid session AWS Access Key ID...\033[0m")
        # Si el error es por la key errónea
        elif 'SignatureDoesNotMatch' in str(e):
            print("\033[91mInvalid session AWS Secret Access Key...\033[0m")
        # Si el error es por el token inválido
        elif 'InvalidToken' in str(e):
            print("\033[91mInvalid session AWS Token...\033[0m")
        # Si el error es por el token expirado
        elif 'ExpiredToken' in str(e):
            print("\033[91mAWS Token has expired...\033[0m")
        # Si el error es por la región inválida
        elif 'endpoint URL' in str(e):
            print("\033[91mInvalid session AWS Region...\033[0m")
        # Si el error es por el bucket inválido
        elif 'HeadBucket' in str(e):
            print("\033[91mInvalid session AWS Bucket...\033[0m")
        # Cualquier otro error
        else:
            print(f"\033[91mError: {str(e)}\033[0m")
        return None, None

class ApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api'

    def ready(self):
        rekognition_client = configure_rekognition_client()