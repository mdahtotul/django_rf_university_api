from rest_framework import serializers


class SemesterYearSerializerValidations:
    """
    warning: to use this class, make sure that your serializer and model has the following fields
      - year data containing field name should be "year"
      - semester data containing field name should be "semester"
    """

    def post_method_validate(self, data):
        # logic 1: department can't support both semester and year
        # logic 2: department must have either semester or year

        year = data.get("year")
        semester = data.get("semester")

        if year and semester:
            raise serializers.ValidationError(
                "Either year or semester can contain data, but not both field."
            )
        elif not year and not semester:
            raise serializers.ValidationError(
                "Either year or semester must contain data."
            )

    def patch_method_validate(self, instance, data):
        # logic 1: department can't support both semester and year
        # logic 2: department must have either semester or year
        # according to logic 1 if year is provided then semester value will be null, otherwise vice-versa

        year = data.get("year")
        semester = data.get("semester")

        if instance:
            instance_year = instance.year
            instance_semester = instance.semester

            if year is not None and semester is not None:
                raise serializers.ValidationError(
                    "Either year or semester can contain data, but not both field."
                )
            elif year is not None:
                instance_year = year
                instance_semester = None
                data["year"] = instance_year
                data["semester"] = None
            elif semester is not None:
                instance_semester = semester
                instance_year = None
                data["semester"] = instance_semester
                data["year"] = None
