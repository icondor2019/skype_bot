import json
import os
import requests
from requests.auth import HTTPBasicAuth
from app.configuration.settings import settings


def lambda_handler(event, context):
    # if settings.ENVIRONMENT == 'dev':
    #     return 'hello dev ambiente'
    # Extraer el mensaje de la solicitud de entrada
    print(event)
    # if isinstance(event['body'], str):
    #     body = json.loads(event['body'])
    # else:
    #     body = event['body']
    body = event
    
    # Extraer información del mensaje de entrada
    message = body.get('text', '')
    user_id = body['from']['id']
    
    # Aquí puedes implementar cualquier lógica, por ejemplo, responder a un comando específico
    if message.lower() == "hello":
        response_text = "Hello! How can I help you today?"
    else:
        response_text = f"You said: {message}"
    
    # Preparar la respuesta para enviar de vuelta a Skype
    reply = {
        "type": "message",
        "from": {"id": user_id},
        "text": response_text
    }
    
    # Configurar el endpoint de respuesta de Skype usando el App ID y App Password
    skype_response_url = body['serviceUrl'] + '/v3/conversations/{}/activities/{}'.format(
        body['conversation']['id'], body['id']
    )
    
    # Obtener el token de autenticación para el bot de Skype
    token_url = "https://login.microsoftonline.com/botframework.com/oauth2/v2.0/token"
    data = {
        "grant_type": "client_credentials",
        "client_id": os.environ['MICROSOFT_APP_ID'],
        "client_secret": os.environ['MICROSOFT_APP_PASSWORD'],
        "scope": "https://api.botframework.com/.default"
    }
    
    auth_response = requests.post(token_url, data=data)
    token = auth_response.json()['access_token']
    
    # Enviar el mensaje de respuesta a Skype
    headers = {
        "Authorization": "Bearer " + token,
        "Content-Type": "application/json"
    }
    
    response = requests.post(skype_response_url, headers=headers, json=reply)
    print(response.text)
    return {
        'statusCode': response.status_code,
        'body': json.dumps({'status': 'Message sent'})
    }
