from rest_framework.routers import SimpleRouter

from .views import *

router = SimpleRouter()
router.register(r"parents", viewset=ParentViewSet)
router.register(r"students", viewset=StudentViewSet)
router.register(r"teachers", viewset=TeacherViewSet)

urlpatterns = router.urls
