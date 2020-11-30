from django.db import models


class UserDB(models.Model):
    user = models.CharField(max_length=10)
