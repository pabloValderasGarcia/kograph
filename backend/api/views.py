from decouple import config

# AWS Credentials
aws_access_key_id = config('aws_access_key_id')
aws_secret_access_key = config('aws_secret_access_key')
aws_session_token = config('aws_session_token')
aws_region = config('aws_region')