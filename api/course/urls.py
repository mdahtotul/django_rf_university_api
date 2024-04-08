from django.urls import path
from rest_framework.routers import SimpleRouter

from .views import *

router = SimpleRouter()
router.register(r"courses", viewset=CourseViewSet)

urlpatterns = router.urls + [
    path(
        "courses/department/<int:department_id>/",
        DepartmentCourseViewSet.as_view(),
    ),
]
