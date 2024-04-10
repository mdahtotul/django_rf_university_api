from rest_framework.pagination import PageNumberPagination


def paginate_queryset(queryset, request, page_size=10, serializer_class=None):
    paginator = PageNumberPagination()
    paginator.page_size = page_size
    paginated_qs = paginator.paginate_queryset(queryset, request)
    if serializer_class is not None:
        serializer = serializer_class(paginated_qs, many=True)
        return paginator.get_paginated_response(serializer.data)

    return paginator.get_paginated_response(paginated_qs)
