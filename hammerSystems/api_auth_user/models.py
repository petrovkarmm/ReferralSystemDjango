from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    invite_code = models.CharField(max_length=6, unique=True)
    was_invited = models.BooleanField(default=False)


class Friends(models.Model):
    inviting = models.ForeignKey(User,
                                 on_delete=models.CASCADE,
                                 related_name='invited')
    # кого пригласили
    invited = models.ForeignKey(User,
                                on_delete=models.CASCADE,
                                related_name='invinting')
    # кто пригласил