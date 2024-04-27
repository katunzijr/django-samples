from django.db import models


class LiableToFileReturn(models.Model):
    class Status(models.TextChoices):
        UPLOADED = 'UPD', 'Uploaded'
        REVIEWED = 'RVD', 'Reviwed'
        APPROVED = 'APD', 'Approved'

    tin = models.BigIntegerField(unique=True, db_column='TIN')
    name = models.CharField(max_length=100, db_column='NAME')
    business = models.CharField(max_length=100, db_column='BUSINESS')
    return_type = models.CharField(max_length=100, db_column='RETUEN_TYPE')
    status = models.CharField(max_length=3, choices=Status.choices, default=Status.APPROVED)

    def __str__(self):
        return f'{self.tin} - {self.name}'
    
    class Meta:
        db_table = "EFILE_LIABLE_TO_FILE_RETURN"
        verbose_name = "LiableToFileReturn"
        verbose_name_plural = "LiableToFileReturns"

