from .views.peca import PecaViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'pecas', PecaViewSet)

urlpatterns = router.urls
