from django.db import models


class ApprovalStatus(models.TextChoices):
        UPLOADED = '0', 'Uploaded'
        REVIEWED = '1', 'Reviewed'
        APPROVED = '2', 'Approved'
        REJECTED = '3', 'Rejected'
        SUSPENDED = '4', 'Suspended'


class OtherReturnDuedate(models.Model):
    CATEGORY_ID = models.IntegerField()
    CATEGORY_NAME = models.CharField(max_length=100, null=True)
    DAY = models.IntegerField(null=True)
    MONTH = models.IntegerField()
    YEAR = models.IntegerField()
    DUEDATE = models.DateField()
    IP_ADDRESS = models.CharField(max_length=100, null=True)
    COMPUTERNAME = models.CharField(max_length=100, null=True)
    OS_USER = models.CharField(max_length=100, null=True)
    RATE = models.CharField(max_length=100, null=True)
    ENTRYDATE = models.DateTimeField(auto_now_add=True)
    ENTERED_DATE = models.DateTimeField(auto_now_add=True)
    ENTERED_BY = models.CharField(max_length=100, null=True)
    CHANGED_DATE = models.DateTimeField(auto_now=True)
    CHANGED_BY = models.CharField(max_length=100, null=True)

    def __str__(self):
        print(self.DUEDATE) 
        return f'{self.CATEGORY_ID} - {self.YEAR} - {(self.DUEDATE).strftime("%d %B %Y")}'
    
    class Meta:
        ordering = ["-ENTERED_DATE"]
        db_table = "EFILE_T_OTHRETURNS_DUEDATE"
        verbose_name = "ReturnDuedate"
        verbose_name_plural = "ReturnDuedates"
        unique_together = (('YEAR', 'CATEGORY_ID', 'DUEDATE'),)


class UnfiledReturnAnnually(models.Model):
    TAXPAYER_ID = models.BigIntegerField()
    CATEGORY_ID = models.IntegerField()
    CATEGORY_NAME = models.CharField(max_length=100, null=True)
    YEAR = models.IntegerField()
    STATUS = models.IntegerField(choices=ApprovalStatus.choices, default=ApprovalStatus.UPLOADED)
    CREATED_AT = models.DateTimeField(auto_now_add=True)
    UPDATED_AT = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.TAXPAYER_ID} - {self.CATEGORY_NAME}'
    
    class Meta:
        ordering = ["-CREATED_AT"]
        db_table = "EFILE_UNFILED_RETURN_ANNUALLY"
        verbose_name = "UnfiledReturnAnnually"
        verbose_name_plural = "UnfiledReturnAnnuallys"
        unique_together = (('TAXPAYER_ID', 'CATEGORY_ID', 'YEAR'),)


class UnfiledReturnMonthly(models.Model):
    TAXPAYER_ID = models.BigIntegerField()
    CATEGORY_ID = models.IntegerField()
    YEAR = models.IntegerField()
    MONTH = models.IntegerField()
    DUEDATE = models.DateField()
    EXTENDED_DUEDATE = models.DateField(null=True)
    IS_FILLED = models.BooleanField(default=False)
    IS_VISIBLE_TO_TP = models.BooleanField(default=False)
    STATUS = models.IntegerField(choices=ApprovalStatus.choices, default=ApprovalStatus.UPLOADED)
    UNFILED_ANNUALLY = models.ForeignKey(UnfiledReturnAnnually, related_name="return_annually", on_delete=models.CASCADE)
    ENTRYDATE = models.DateTimeField(auto_now_add=True)
    UPDATED_AT = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.TAXPAYER_ID} - {self.DUEDATE}'
    
    class Meta:
        ordering = ["-ENTRYDATE"]
        db_table = "EFILE_UNFILED_RETURN_MONTHLY"
        verbose_name = "UnfiledReturnMonthly"
        verbose_name_plural = "UnfiledReturnMonthlys"
        unique_together = (('TAXPAYER_ID', 'CATEGORY_ID', 'DUEDATE'),)

