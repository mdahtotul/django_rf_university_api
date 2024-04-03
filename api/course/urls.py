from rest_framework.routers import SimpleRouter
from .views import *

router = SimpleRouter()
router.register(r"courses", viewset=CourseViewSet)

urlpatterns = router.urls
