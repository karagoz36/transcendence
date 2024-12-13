from rest_framework.request import Request
from django.http.response import HttpResponse
from django.shortcuts import render
from django.shortcuts import render, redirect
from channels.layers import get_channel_layer, BaseChannelLayer
from django.contrib.auth.models import User
from asgiref.sync import async_to_sync

async def response(request: Request) -> HttpResponse:
	user: User = request.user
	layer: BaseChannelLayer = get_channel_layer()
	await (layer.group_send)(f"{user.username}_notifications", {
		"type": "sendMessage",
		"message": "test"
	})
	return render(request, "index.html", {"USERNAME": user.username})