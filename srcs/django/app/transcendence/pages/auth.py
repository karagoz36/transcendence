from django.contrib.auth.models import User, AnonymousUser
from rest_framework.request import Request
from rest_framework.response import Response
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from channels.layers import get_channel_layer, BaseChannelLayer
from django.contrib.auth import logout
from celery import shared_task
from celery.utils.log import get_task_logger
from django.conf import settings

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
