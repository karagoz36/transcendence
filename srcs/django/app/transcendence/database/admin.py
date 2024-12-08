from django.contrib.auth.models import User
from os import getenv
from django.apps import AppConfig

class CustomAppConfig(AppConfig):
	def createAdminUser() -> None:
		username = getenv("POSTGRES_USER")
		password = getenv("POSTGRES_PASSWORD")
		if User.objects.filter(username=username).exists():
			return
		User.objects.create_superuser(username=username, password=password)
	def ready(self):
		self.createAdminUser()
