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
import re

logger = get_task_logger(__name__)

async def closeWebSockets(id: int):
	layer: BaseChannelLayer = get_channel_layer()
	await layer.group_send(f"{id}_notifications", {
		"type": "closeConnection"
	})

async def logoutUser(request: Request, success: str, err: str, status: int) -> Response:
	response = render(request, "auth.html", {"ERROR_MESSAGE": err, "SUCCESS_MESSAGE": success}, status=status)
	response.headers["Clear-Site-Data"] = '"*"'
	if "already logged in" not in err:
		await closeWebSockets(request.user.id)
	return response

async def response(request: Request):
	if "logout" not in request.query_params.keys() and request.user.username != "":
		return redirect("/")
	error = ""
	success = ""
	status = 200

	if "error" in request.query_params.keys():
		status = 401
		error = request.query_params["error"]
	if "success" in request.query_params.keys():
		success = request.query_params["success"]
	if "logout" in request.query_params.keys():
		return await logoutUser(request, success, error, status)
	return render(request, "auth.html", {"ERROR_MESSAGE": error, "SUCCESS_MESSAGE": success}, status=status)

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

	user_info_url = "https://api.intra.42.fr/v2/me"
	headers = {'Authorization': f'Bearer {access_token}'}
	user_info_response = requests.get(user_info_url, headers=headers)

	if user_info_response.status_code != 200:
		return JsonResponse({'error': 'Failed to fetch user info'}, status=400)

	user_info = user_info_response.json()
	base_username = user_info['login']
	username = base_username

	username_pattern = r'^(.*?)(\d+)?$'
	match = re.match(username_pattern, username)

	base_username = match.group(1)
	counter = int(match.group(2)) if match.group(2) else 1

	while User.objects.filter(username=username).exists():
		username = f"{base_username}{counter}"
		counter += 1

	user, created = User.objects.get_or_create(id=user_info.get('id'))

	if created:
		user.username = user_info.get('login', '')
		user.first_name = user_info.get('first_name', '')
		user.last_name = 	user_info.get('last_name', '')
		user.email = user_info.get('email', '')
		user.save()
	else:
		user = user

	login(request, user)
	tokens = get_tokens_for_user(user)
	response = redirect('/')
	response.set_cookie('access_token', tokens['access'], httponly=True, samesite='Lax', max_age=86400)
	response.set_cookie('refresh_token', tokens['refresh'], httponly=True, samesite='Lax', max_age=86400)
	return response

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
