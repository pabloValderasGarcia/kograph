import boto3
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from decouple import config
import uuid

# AWS Credentials
aws_access_key_id = config('aws_access_key_id')
aws_secret_access_key = config('aws_secret_access_key')
aws_session_token = config('aws_session_token')
aws_region = config('aws_region')

def dynamodb_connect():
    return boto3.resource('dynamodb', aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            aws_session_token=aws_session_token,
            region_name=aws_region)

@csrf_exempt
def register_user(request):
    if request.method == 'POST':
        # Data
        data = json.loads(request.body)

        # Conectar a DynamoDB
        dynamodb = dynamodb_connect()

        # Añade un nuevo usuario con DynamoDB
        table = dynamodb.Table('user')
        response = table.scan(
            FilterExpression='username = :username OR email = :email',
            ExpressionAttributeValues={':username': data['username']}
        )

        # Si ya existe el usuario, no se puede
        if response['Count'] > 0:
            return JsonResponse({'status': 'NO', 'message': 'Username already exists'}, status=409)
        
        user_data = {
            'id': str(uuid.uuid4()),
            'email': data['email'],
            'username': data['username'],
            'password': data['password'],
        }
        table.put_item(Item=user_data)

        return JsonResponse({'status': 'OK', 'message': 'Successfully registered'})
    else:
        return JsonResponse({'status': 'NO', 'message': 'Not allowed method'}, status=405)
    
@csrf_exempt
def login_user(request):
    if request.method == 'POST':
        # Data
        data = json.loads(request.body)

        # Conectar a DynamoDB
        dynamodb = dynamodb_connect()

        # Verificar que existe el usuario en DynamoDB
        table = dynamodb.Table('user')
        response = table.scan(
            FilterExpression='username = :username',
            ExpressionAttributeValues={':username': data['username']}
        )

        if response['Count'] > 0:
            user = response['Items'][0]
            if user['password'] == data['password']:
                return JsonResponse({'status': 'OK', 'message': 'Successfully logged'})
            else:
                return JsonResponse({'status': 'NO', 'message': 'Invalid password'}, status=401)
        else:
            return JsonResponse({'status': 'NO', 'message': 'User not found'}, status=404)
    else:
        return JsonResponse({'status': 'NO', 'message': 'Not allowed method'}, status=405)