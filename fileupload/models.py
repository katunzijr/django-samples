from django.db import models
import json


# class MyModel(models.Model):
#     return_id = models.CharField(max_length=100)
#     file = models.FileField(upload_to="attachments/", max_length=100, null=True, blank=True)
#     attachments = models.F(Attachment, blank=True)
#     uploaded_on = models.DateTimeField(auto_now_add=True)
    
#     def __str__(self):
#         return self.uploaded_on.date()


class BedNightReturn(models.Model):
    return_master = models.PositiveIntegerField(db_column="return_id")
    number_of_facility = models.PositiveIntegerField()
    attachment = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "EFILE_BNL_RETURN"
        verbose_name = "BedNightReturn"
        verbose_name_plural = "BedNightReturns"

    def __str__(self):
        return f"{self.number_of_facility}"