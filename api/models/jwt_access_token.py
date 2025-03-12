from django.db import models


class JwtAccessToken(models.Model):
    access_token = models.TextField(max_length=255, unique=True)

    class Meta:
        verbose_name = "Jwt Token"
        verbose_name_plural = "Jwt Tokens"

    def __str__(self):
        return self.access_token
