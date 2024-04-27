from rest_framework import serializers
from .models import *

# class FileUploadSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = MyModel
#         fields = ('return_id', 'attachments', 'uploaded_on',)


class MultipleFileUploadSerializer(serializers.ModelSerializer):
    # number_of_facility = serializers.IntegerField(allow_null=True, required=False)
    return_master = serializers.IntegerField(required=False)
    # return_m = return_master
    return_master_copy = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = BedNightReturn
        fields = [
            'return_master', 
            'return_master_copy',
            'attachment', 
            # 'number_of_facility'
        ]

    def get_return_master_copy(self, obj):
        return obj.return_master
