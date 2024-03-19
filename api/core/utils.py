from rest_framework import exceptions
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import exception_handler
from PIL import Image


def is_valid_image(image):
    try:
        image = Image.open(image)
        image.verify()
        return True
    except:
        return False


def custom_handle_exception(exc, request):
    if isinstance(exc, exceptions.ValidationError):
        errors = ""
        for field, errors_list in exc.detail.items():
            errors += (
                f"{errors_list[0]}[{field} field]"
                if len(errors_list) > 0
                else "Internal server error"
            )
        return Response({"details": errors}, status=status.HTTP_400_BAD_REQUEST)
    else:
        response = exception_handler(exc, request)
        if response is None:
            return Response(
                {"details": str(exc)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        return Response(
            {"details": str(response.data.get("detail", response.data))},
            status=response.status_code,
        )
