from django.db.models import Q, Value, CharField
from django.db.models.functions import Concat

from core.constants import ROLE_ADMIN, ROLE_STAFF, ROLE_USER


class UserFilterService:
    def user_filter_queryset(
        self,
        queryset=None,
        request=None,
        name=None,
        email=None,
        phone=None,
    ):
        if request.user.role == ROLE_ADMIN:
            queryset = queryset
        elif request.user.role == ROLE_STAFF:
            queryset = queryset.filter(role__in=[ROLE_STAFF, ROLE_USER])
        elif request.user.role == ROLE_USER:
            queryset = queryset.filter(role=ROLE_USER)

        if name:
            queryset = (
                queryset.annotate(
                    full_name=Concat(
                        "first_name", Value(" "), "last_name", output_field=CharField()
                    ),
                )
                .filter(
                    Q(first_name__icontains=name)
                    | Q(last_name__icontains=name)
                    | Q(full_name__icontains=name)
                )
                .distinct()
            )

        if email:
            queryset = queryset.filter(email__icontains=email)
        if phone:
            queryset = queryset.filter(phone__icontains=phone)

        return queryset
