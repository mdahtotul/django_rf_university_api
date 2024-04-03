from rest_framework.routers import SimpleRouter

from .views import *

router = SimpleRouter()
router.register(r"faculties", viewset=FacultyViewSet)
router.register(r"departments", viewset=DepartmentViewSet)


urlpatterns = router.urls
