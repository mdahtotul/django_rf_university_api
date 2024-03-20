from rest_framework.routers import SimpleRouter

from .views import *

router = SimpleRouter()
router.register(r"parents", viewset=ParentViewSet)
router.register(r"students", viewset=StudentViewSet)

urlpatterns = router.urls
