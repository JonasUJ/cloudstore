from django.db import models


class AccessToken(models.Model):
    token = models.CharField(max_length=20)

    def __str__(self):
        return self.token
