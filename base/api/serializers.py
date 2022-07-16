from dataclasses import field
from rest_framework.serializers import ModelSerializer,SlugRelatedField
from base.models import Room

class RoomSerializer(ModelSerializer):
    participants = SlugRelatedField(
        read_only = True,
        many = True,
        slug_field= 'username'

    )

    class Meta:
        model = Room
        fields = '__all__'