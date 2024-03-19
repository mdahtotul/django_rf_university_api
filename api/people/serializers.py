from rest_framework import serializers

from account.serializers import SimpleUserSerializer
from address.serializers import AddressSerializer

from .models import Parent


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
