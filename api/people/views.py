from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend

from core.permissions import *
from core.utils import custom_handle_exception
from .models import Parent
from .filters import ParentFilter
from .pagination import DefaultPagination
from .serializers import CreateUpdateParentSerializer, RetrieveParentSerializer


class ParentViewSet(viewsets.ModelViewSet):
    queryset = Parent.objects.all()
    # queryset = Parent.objects.select_related("user", "address")
    serializer_class = RetrieveParentSerializer
    permission_classes = [UserOrReadOnly | StaffOrReadOnly | AdminOrReadOnly]
    pagination_class = DefaultPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = ParentFilter

    def get_serializer_class(self):
        if self.request.method == "POST" or self.request.method == "PATCH":
            return CreateUpdateParentSerializer
        else:
            return RetrieveParentSerializer

    def handle_exception(self, exc):
        return custom_handle_exception(exc, self.request)
