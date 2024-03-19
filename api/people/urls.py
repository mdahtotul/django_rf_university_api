from rest_framework.routers import SimpleRouter

from .views import *

router = SimpleRouter()
router.register(r"parents", viewset=ParentViewSet)

urlpatterns = router.urls
