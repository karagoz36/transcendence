from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import Token
from django.contrib.auth.models import User, AnonymousUser
from rest_framework.request import Request
from django.shortcuts import redirect

class CustomAuthentication(JWTAuthentication):
	def authenticate(self, request):
		accessToken: str = request.COOKIES.get("access_token")
		user: User = AnonymousUser()
		validatedToken: Token = None
		try:
			validatedToken = self.get_validated_token(accessToken)
			user = self.get_user(validatedToken)
		except:
			user = AnonymousUser()
		return user, validatedToken

class RequiredLoginMiddleware:
	def __init__(self, get_response):
		self.get_response = get_response

	def __call__(self, request: Request):
		user, _ = CustomAuthentication().authenticate(request=request)
		path: str = request.path
		if path.startswith("/api"):
			return self.get_response(request)
		if not path.startswith("/auth") and type(user) is AnonymousUser:
			return redirect("/auth")
		return self.get_response(request)