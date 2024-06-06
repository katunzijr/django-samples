from django.db import models
import json


class BedNightLevyMaster(models.Model):
    return_id = models.IntegerField(primary_key=True)
    taxpayer_id = models.IntegerField(null=True, blank=True)
    branch_id = models.IntegerField(default=0)
    taxpayer_id_declr = models.IntegerField(null=True, blank=True)
    yearofincome = models.IntegerField()
    startdate = models.DateTimeField()
    enddate = models.DateTimeField()
    submissiondate = models.DateTimeField(auto_now_add=True)
    category = models.IntegerField(blank=True, null=True, db_column="category_id")
    residential_status = models.CharField(max_length=20, blank=True, null=True)
    entity_type = models.CharField(max_length=20, blank=True, null=True)
    entity_parent_name = models.CharField(max_length=256, blank=True, null=True)
    is_mining = models.CharField(max_length=1, default="N")
    status_ct = models.CharField(max_length=30, blank=True, null=True)
    changeuser = models.CharField(max_length=20, blank=True, null=True)
    changedate = models.DateTimeField(blank=True, null=True)
    change_app_user = models.CharField(max_length=20, blank=True, null=True)
    ip_address = models.CharField(max_length=100, blank=True, null=True)
    err_msg = models.CharField(max_length=2000, blank=True, null=True)
    site = models.BigIntegerField()  # * fetch from user details
    itaxtype_ct = models.CharField(max_length=20, blank=True, null=True)
    period = models.BigIntegerField()
    gfs_code = models.PositiveSmallIntegerField(null=True, blank=True)
    declarant_posn = models.CharField(max_length=80, blank=True, null=True)
    entrydate = models.DateTimeField(auto_now_add=True)
    staff_no = models.CharField(max_length=80, blank=True, null=True)
    duedate = models.DateTimeField(blank=True, null=True)  # * link with due date table
    assessment_no = models.CharField(max_length=20, blank=True, null=True)
    assess_final_bv = models.CharField(max_length=20, blank=True, null=True)
    net_tax_payable = models.DecimalField(max_digits=30, decimal_places=2, blank=True, null=True)
    computername = models.CharField(max_length=20, blank=True, null=True)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        db_table = "EFILE_RET_BNL_MASTER"
        verbose_name = "BedNightLevyMaster"
        verbose_name_plural = "BedNightLevyMasters"

    def __str__(self):
        return f"{self.return_id}"



class BedNightReturn(models.Model):
    return_master = models.ForeignKey(
        BedNightLevyMaster,
        related_name="bednights",
        on_delete=models.CASCADE,
        db_column="return_id",
    )
    number_of_facility = models.PositiveIntegerField()
    attachment = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        db_table = "EFILE_BNL_RETURN"
        verbose_name = "BedNightReturn"
        verbose_name_plural = "BedNightReturns"

    def __str__(self):
        return f"{self.number_of_facility}"