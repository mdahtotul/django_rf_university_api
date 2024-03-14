from rest_framework import routers
from .views import *

router = routers.SimpleRouter()
router.register(r"addresses", viewset=AddressViewSet)


urlpatterns = router.urls
