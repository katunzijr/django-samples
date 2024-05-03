from django.db import models


class LiableToFileReturn(models.Model):
    class ApprovalStatus(models.TextChoices):
        UPLOADED = 'UPD', 'Uploaded'
        REVIEWED = 'RVD', 'Reviwed'
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
        db_table = "ITAX.OTHER_RETURN_UNFILED_MONTHLY"
        verbose_name = "LiableToFileReturn"
        verbose_name_plural = "LiableToFileReturns"

class LiableToFileReturn1(models.Model):
    class ApprovalStatus(models.TextChoices):
        UPLOADED = 'UPD', 'Uploaded'
        REVIEWED = 'RVD', 'Reviwed'
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

