from typing import Callable
from django.http import HttpRequest, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.urls import reverse

class LoginRequiredMiddleware:
	def __init__(self, get_response: Callable[[HttpRequest], HttpResponse]) -> None:
		self.get_response = get_response

	def __call__(self, request: HttpRequest) -> HttpResponse:
		user: User = request.user
		response: HttpResponse = self.get_response(request)

		if "api" in request.path:
			return response
		if request.path not in ("/auth", "/auth/") and not user.is_active:
			return redirect("/auth")
		return response