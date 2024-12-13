from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.contrib.auth.models import User
from rest_framework.request import Request
from django.shortcuts import redirect

class CustomAuthentication(JWTAuthentication):
	def authenticate(self, request):
		if "auth" in request.path:
			return None
		accessToken: str = request.COOKIES.get("access_token")
		validatedToken = self.get_validated_token(accessToken)
		user: User|None = None
		try:
			user = self.get_user(validatedToken)
		except:
			pass
		return user, validatedToken

class RequiredLoginMiddleware:
	def __init__(self, get_response):
		self.get_response = get_response

	def __call__(self, request: Request):
		user: User = request.user
		path: str = request.path
		
		if path.startswith("/api"):
			return self.get_response(request)
		if not path.startswith("/auth") and user is None:
			return redirect("/auth")
		return self.get_response(request)