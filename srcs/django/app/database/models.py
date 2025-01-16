from django.db import models
from django.contrib.auth.models import User
import pyotp

class FriendList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="friends")
    friend = models.ForeignKey(User, on_delete=models.CASCADE, related_name="friendOf")
    invitePending = models.BooleanField(default=True)

async def getFriendship(user: User, friend: User) -> FriendList|None:
	friendship: FriendList
	try:
		friendship = await FriendList.objects.select_related("user", "friend").aget(user=user, friend=friend)
		return friendship
	except:
		pass
	try:
		friendship = await FriendList.objects.select_related("user", "friend").aget(user=friend, friend=user)
		return friendship
	except:
		pass
	return None

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_2fa_enabled = models.BooleanField(default=False)
    otp_secret = models.CharField(max_length=32, blank=True, null=True)
    avatar = models.ImageField(
        upload_to='avatars/',  # Dossier où les images seront stockées
        blank=True,            # Le champ peut être laissé vide
        null=True              # Valeur NULL autorisée dans la base de données
    )
	# avatar = models.ImageField(default='avatar.png', blank=True)

    def generate_otp_secret(self):
        if not self.otp_secret:
            self.otp_secret = pyotp.random_base32()
            self.save()

    def get_otp(self):
        totp = pyotp.TOTP(self.otp_secret)
        return totp.now()

# class UserProfileBis(models.Model):
# 	username = models.ForeignKey(User, on_delete=models.CASCADE)
# 	avatar = models.ImageField(
#         upload_to='avatars/',  # Dossier où les images seront stockées
#         blank=True,            # Le champ peut être laissé vide
#         null=True              # Valeur NULL autorisée dans la base de données
#     )

class Messages(models.Model):
	friendship = models.ForeignKey(FriendList, on_delete=models.CASCADE)
	message = models.TextField()
	sender = models.ForeignKey(User, on_delete=models.CASCADE)
	created_at = models.DateTimeField(auto_now_add=True,)

class PongHistory(models.Model):
	player1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name="player1")
	player1_score = models.IntegerField()
	player2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name="player2")
	player2_score = models.IntegerField()