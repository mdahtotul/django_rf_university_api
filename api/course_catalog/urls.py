from rest_framework import routers

from .views import *

router = routers.SimpleRouter()

router.register(r"subjects", viewset=SubjectViewSet)
router.register(r"chapters", viewset=ChapterViewSet)


urlpatterns = router.urls
