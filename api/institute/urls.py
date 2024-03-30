from rest_framework.routers import SimpleRouter

from .views import *

router = SimpleRouter()
router.register(r"faculties", viewset=FacultyViewset)
router.register(r"departments", viewset=DepartmentViewset)


urlpatterns = router.urls
