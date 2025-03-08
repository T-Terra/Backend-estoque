from .views.peca import PecaViewSet, AuthenticationJwt, AuthJwtRefreshToken
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'api/pecas', PecaViewSet)
router.register(r'api/auth', AuthenticationJwt, basename='auth')
router.register(
    r'api/refreshtoken', AuthJwtRefreshToken, basename='refreshtoken'
)

urlpatterns = router.urls
