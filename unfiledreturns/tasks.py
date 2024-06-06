from celery import shared_task
from django.db import connection
import datetime
from .models import *

@shared_task
def update_unfiled_visibility_periodic(fn=None, sec=None):
    cursor = connection.cursor()
    current_month = datetime.datetime.now().month
    current_year = datetime.datetime.now().year

    query = f"""
        UPDATE EFILE_UNFILED_RETURN_MONTHLY
        SET IS_VISIBLE_TO_TP = 1
        WHERE IS_VISIBLE_TO_TP = 0
        AND STATUS = 'UPD'
        AND MONTH < {current_month}
        AND YEAR = {current_year};
    """

    cursor.execute(query)
    connection.commit()
    cursor.close()

    print(f"Updating unfiled monthly to be visible to taxpayer periodic !! {fn} {sec}")


@shared_task
def generate_unfiled_visibility_annually():
    # Logic to generate taxpayer unfiled return annually
    unfiled_return_annually = UnfiledReturnAnnually(
        taxpayer_id='123456789',
        year=datetime.now().year,
        amount=1000.00,
        created_at=datetime.now()
    )
    unfiled_return_annually.save()
    return "Taxpayer unfiled_return_annually generated"