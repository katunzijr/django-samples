from rest_framework import serializers
from .models import LiableToFileReturn


class LiableToFileReturnSerializer(serializers.ModelSerializer):
    class Meta:
        model = LiableToFileReturn
        fields = (
            'tin',
            'name',
            'business',
            'return_type'
        )