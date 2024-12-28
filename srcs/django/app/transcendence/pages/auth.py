from django.contrib.auth.models import User, AnonymousUser
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.request import Request
from rest_framework.response import Response
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from channels.layers import get_channel_layer, BaseChannelLayer
from django.contrib.auth import logout, login
from celery import shared_task
from celery.utils.log import get_task_logger
from django.http import JsonResponse
from django.conf import settings
import requests

logger = get_task_logger(__name__)

async def closeWebSockets(id: int):
	layer: BaseChannelLayer = get_channel_layer()
	await layer.group_send(f"{id}_notifications", {
		"type": "closeConnection"
	})

async def logoutUser(request: Request) -> Response:
	response = render(request, "auth.html")
	response.delete_cookie("access_token")
	response.delete_cookie("sessionid")
	await closeWebSockets(request.user.id)
	return response

async def response(request: Request):
	if "logout" in request.query_params:
		return await logoutUser(request)
	user: User = request.user
	if not type(user) is AnonymousUser:
		return redirect("/")
	error = ""
	status = 200

	if "error" in request.query_params.keys():
		status = 401
		error = request.query_params["error"]
	return render(request, "auth.html", {"ERROR_MESSAGE": error}, status=status)

async def response42(request: Request):
	client_id = settings.OAUTH2_PROVIDER.get('CLIENT_ID')
	client_secret = settings.OAUTH2_PROVIDER.get('CLIENT_SECRET')
	redirect_uri = settings.OAUTH2_PROVIDER.get('REDIRECT_URI')
	scope = "public"
	state = "random_state_string"

	authorize_url = (
		f"https://api.intra.42.fr/oauth/authorize"
		f"?client_id={client_id}"
		f"&redirect_uri={redirect_uri}"
		f"&response_type=code"
		f"&scope={scope}"
		f"&state={state}"
	)
	return redirect(authorize_url)

def get_tokens_for_user(user):
    """Génère un JWT pour l'utilisateur donné."""
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

def callback_from_42(request):
    code = request.GET.get('code')
    state = request.GET.get('state')

    if state != "random_state_string":
        return JsonResponse({'error': 'Invalid state'}, status=400)

    # Échanger le code contre un access_token
    token_url = "https://api.intra.42.fr/oauth/token"
    token_data = {
        'grant_type': 'authorization_code',
        'client_id': settings.OAUTH2_PROVIDER['CLIENT_ID'],
        'client_secret': settings.OAUTH2_PROVIDER['CLIENT_SECRET'],
        'redirect_uri': settings.OAUTH2_PROVIDER['REDIRECT_URI'],
        'code': code,
    }

    response = requests.post(token_url, data=token_data)
    if response.status_code != 200:
        return JsonResponse({'error': 'Failed to obtain access token'}, status=400)

    response_data = response.json()
    access_token = response_data.get('access_token')
    if not access_token:
        return JsonResponse({'error': 'Access token is missing'}, status=400)

    # Utiliser l'access_token pour récupérer les infos utilisateur
    user_info_url = "https://api.intra.42.fr/v2/me"
    headers = {'Authorization': f'Bearer {access_token}'}
    user_info_response = requests.get(user_info_url, headers=headers)

    if user_info_response.status_code != 200:
        return JsonResponse({'error': 'Failed to fetch user info'}, status=400)

    user_info = user_info_response.json()
    user, created = User.objects.get_or_create(username=user_info['login'])

    if created:
        user.first_name = user_info.get('first_name', '')
        user.last_name = user_info.get('last_name', '')
        user.email = user_info.get('email', '')
        user.save()

    # Connecter l'utilisateur
    login(request, user)
    tokens = get_tokens_for_user(user)
    response = redirect('/')
    response.set_cookie('access_token', tokens['access'], httponly=True, samesite='Lax', max_age=86400)
    response.set_cookie('refresh_token', tokens['refresh'], httponly=True, samesite='Lax', max_age=86400)
    return response

# def callback_from_42(request: Request):
#     code = request.GET.get('code')
#     state = request.GET.get('state')

#     if state != "random_state_string":
#         return JsonResponse({'error': 'Invalid state'}, status=400)

#     # Échanger le code contre un access_token
#     token_url = "https://api.intra.42.fr/oauth/token"
#     client_id = settings.OAUTH2_PROVIDER.get('CLIENT_ID')
#     client_secret = settings.OAUTH2_PROVIDER.get('CLIENT_SECRET')
#     redirect_uri = settings.OAUTH2_PROVIDER.get('REDIRECT_URI')

#     # Paramètres de l'échange
#     token_data = {
#         'grant_type': 'authorization_code',
#         'client_id': client_id,
#         'client_secret': client_secret,
#         'redirect_uri': redirect_uri,
#         'code': code,
#     }

#     # Faire la requête pour obtenir le token
#     response = requests.post(token_url, data=token_data)
#     response_data = response.json()
#     access_token = response_data.get('access_token')
#     if not access_token:
#         return JsonResponse({'error': 'Failed to obtain access token'}, status=400)

#     # access_token pour récup les infos user
#     user_info_url = "https://api.intra.42.fr/v2/me"
#     headers = {
#         'Authorization': f'Bearer {access_token}',
#     }
#     user_info_response = requests.get(user_info_url, headers=headers)
#     user_info = user_info_response.json()
#     user, created = User.objects.get_or_create(username=user_info['login'])
#     # Pour plus tard: utiliser l'api pour récup nom, prénom, email.
#     # user.first_name = user_info.get('first_name', '')
    
#     login(request, user)
#     return redirect('/')

@shared_task
def sendingEmail(otp, email):
    try:
        send_mail(
            subject="Transcendence - Verification code",
            message=f"Your verification code is {otp}",
            from_email="noreply@example.com",
            recipient_list=[email],
            fail_silently=False,
        )
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False
