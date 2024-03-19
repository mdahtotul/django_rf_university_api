from rest_framework import permissions, viewsets, status
from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework import exceptions
from django_filters import rest_framework as filters

from core.permissions import *
from .models import Address
from .filters import AddressFilter
from .serializers import AddressSerializer


class AddressPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 1000
    ordering = ["-id"]


class AddressViewSet(viewsets.ModelViewSet):
    queryset = Address.objects.all().order_by("-id")
    serializer_class = AddressSerializer
    permission_classes = [AdminOrReadOnly]
    pagination_class = AddressPagination
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = AddressFilter

    def get_permissions(self):
        if self.action == "create":
            return [permissions.IsAuthenticated()]
        return super().get_permissions()

    # formatting exception response
    def handle_exception(self, exc):
        if isinstance(exc, exceptions.ValidationError):
            errors = ""
            for field, errors_list in exc.detail.items():
                errors = (
                    f"{errors_list[0]}[{field} field]"
                    if len(errors_list) > 0
                    else "Internal server error"
                )
            return Response({"details": errors}, status=status.HTTP_400_BAD_REQUEST)
        else:
            response = exception_handler(exc, self.request)
            if response is None:
                return Response(
                    {"details": str(exc)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
            return Response({"details": response.data}, status=response.status_code)
