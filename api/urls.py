from .views.peca import PecaViewSet
from .auth.views_tokens import (
    AuthenticationJwt,
    AuthJwtRefreshToken,
    AuthRegister,
    AuthLogOut,
)
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'api/pecas', PecaViewSet)
router.register(r'api/login', AuthenticationJwt, basename='login')
router.register(r'api/register', AuthRegister, basename='register')
router.register(r'api/logout', AuthLogOut, basename='logout')
router.register(
    r'api/refreshtoken', AuthJwtRefreshToken, basename='refreshtoken'
)

urlpatterns = router.urls
