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
		user: User = self.get_user(validatedToken)
		if user is None:
			redirect("/auth")
		return user, validatedToken

class RequiredLoginMiddleware:
	def __init__(self, get_response):
		self.get_response = get_response

	def __call__(self, request: Request):
		user: User = request.user
		path: str = request.path
		print(path, flush=True)
		
		if path.startswith("/api"):
			return self.get_response(request)
		if not path.startswith("/auth") and not user.is_authenticated:
			return redirect("/auth")
		if "auth" in request.path:
			print("test")
		return self.get_response(request)