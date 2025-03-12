from django.contrib import admin
from .models.peca import Peca
from .models.jwt_access_token import JwtAccessToken

# Register your models here.
admin.site.register(Peca)
admin.site.register(JwtAccessToken)
