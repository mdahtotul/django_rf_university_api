from rest_framework import permissions, viewsets, status
from rest_framework.views import exception_handler
from rest_framework.pagination import PageNumberPagination
from django_filters import rest_framework as filters

from core.pagination import DefaultPagination
from core.permissions import *
from core.utils import format_exception
from .models import Address
from .filters import AddressFilter
from .serializers import AddressSerializer


class AddressViewSet(viewsets.ModelViewSet):
    queryset = Address.objects.all().order_by("-id")
    serializer_class = AddressSerializer
    permission_classes = [AdminOrReadOnly]
    pagination_class = DefaultPagination
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = AddressFilter

    def get_permissions(self):
        if self.action == "create":
            return [permissions.IsAuthenticated()]
        return super().get_permissions()

    # formatting exception response
    def handle_exception(self, exc):
        return format_exception(exc, self.request)
