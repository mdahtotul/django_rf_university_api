from rest_framework import serializers


from core.validations import SemesterYearSerializerValidations
from account.serializers import SimpleUserSerializer
from address.serializers import AddressSerializer
from institute.serializers import RetrieveDepartmentSerializer

from .models import Parent, Student, Teacher

yearSemesterValidation = SemesterYearSerializerValidations()


class RetrieveParentSerializer(serializers.ModelSerializer):
    user = SimpleUserSerializer()
    address = AddressSerializer()

    class Meta:
        model = Parent
        fields = ["id", "user", "address", "occupation"]


class CreateUpdateParentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Parent
        fields = ["user", "address", "occupation"]


class RetrieveStudentSerializer(serializers.ModelSerializer):
    user = SimpleUserSerializer()
    address = AddressSerializer()
    parent = RetrieveParentSerializer()
    department = RetrieveDepartmentSerializer()

    class Meta:
        model = Student
        fields = [
            "id",
            "student_id",
            "user",
            "parent",
            "address",
            "occupation",
            "enrollment_date",
            "cgpa",
            "credits",
            "session",
            "semester",
            "year",
            "department",
            "relationship_to_parent",
            "degree",
        ]


class CreateUpdateStudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = [
            "student_id",
            "user",
            "parent",
            "address",
            "cgpa",
            "credits",
            "degree",
            "session",
            "semester",
            "year",
            "department",
            "relationship_to_parent",
        ]

    def validate(self, data):
        if self.instance:
            yearSemesterValidation.patch_method_validate(self.instance, data)
        else:
            yearSemesterValidation.post_method_validate(data)

        return data

    # Override serializer for update method
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Check if serializer is being used for update
        if self.instance is not None:
            # Exclude fields for updates
            exclude_fields = ["student_id", "session"]
            for field_name in exclude_fields:
                self.fields.pop(field_name)


class RetrieveTeacherSerializer(serializers.ModelSerializer):
    user = SimpleUserSerializer()
    address = AddressSerializer()
    department = RetrieveDepartmentSerializer()

    class Meta:
        model = Teacher
        fields = [
            "id",
            "user",
            "address",
            "occupation",
            "department",
            "qualifications",
            "specialist",
            "joined_date",
        ]


class CreateUpdateTeacherSerializer(serializers.ModelSerializer):

    class Meta:
        model = Teacher
        fields = [
            "user",
            "address",
            "occupation",
            "department",
            "occupation",
            "salary",
            "qualifications",
            "specialist",
            "joined_date",
        ]
