from django.db import models
from enum import Enum


class ApprovalStatus(Enum):
    UPLOADED = 'Uploaded'
    REVIEWED = 'Reviwed'
    APPROVED = 'Approved'
    SUSPENDE = 'suspended'

APPROVAL_STATUS_CHOICES = [
    ('uploaded', 'Uploaded'),
    ('added', 'Added'),
    ('reviewed', 'Reviewed'),
    ('approved', 'Approved'),
    ('suspended', 'Suspended'),
]

class LiableToFileReturn(models.Model):
    TAXPAYER_ID = models.BigIntegerField(db_column='TAXPAYER_ID')
    CATEGORY_ID = models.IntegerField(db_column='CATEGORY_ID')
    YEAR = models.IntegerField(db_column='YEAR')
    MONTH = models.IntegerField(db_column='MONTH')
    DUEDATE = models.DateField(auto_now_add=True, db_column='DUEDATE')
    EXTENDED_DUEDATE = models.DateField(null=True, db_column='EXTENDED_DUEDATE')
    ENTRYDATE = models.DateField(auto_now_add=True, db_column='ENTRYDATE')
    IS_FILLED = models.BooleanField(default=False)
    IS_VISIBLE_TO_TP = models.BooleanField(default=False)
    STATUS = models.CharField(max_length=20, choices=APPROVAL_STATUS_CHOICES, default='uploaded')

    def __str__(self):
        return f'{self.TAXPAYER_ID} - {self.DUEDATE}'
    
    class Meta:
        db_table = "ITAX.OTHER_RETURN_UNFILED_MONTHLY"
        verbose_name = "LiableToFileReturn"
        verbose_name_plural = "LiableToFileReturns"


class LiableToFileReturn1(models.Model):
    class ApprovalStatus(models.TextChoices):
        UPLOADED = 'UPD', 'Uploaded'
        REVIEWED = 'RVD', 'Reviewed'
        APPROVED = 'APD', 'Approved'

    TAXPAYER_ID = models.BigIntegerField(db_column='TAXPAYER_ID')
    CATEGORY_ID = models.IntegerField(db_column='CATEGORY_ID')
    YEAR = models.IntegerField(db_column='YEAR')
    MONTH = models.IntegerField(db_column='MONTH')
    DUEDATE = models.DateField(auto_now_add=True, db_column='DUEDATE')
    EXTENDED_DUEDATE = models.DateField(null=True, db_column='EXTENDED_DUEDATE')
    ENTRYDATE = models.DateField(auto_now_add=True, db_column='ENTRYDATE')
    IS_FILLED = models.BooleanField(default=False)
    IS_VISIBLE_TO_TP = models.BooleanField(default=False)
    STATUS = models.CharField(max_length=3, choices=ApprovalStatus.choices, default=ApprovalStatus.UPLOADED)

    def __str__(self):
        return f'{self.TAXPAYER_ID} - {self.DUEDATE}'
    
    class Meta:
        db_table = "ITAX_OTHER_RETURN_UNFILED_MONTHLY"
        verbose_name = "LiableToFileReturn"
        verbose_name_plural = "LiableToFileReturns"

