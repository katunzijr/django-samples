from exceldata.tasks import update_unfiled_monthly_status_periodic
from django.core.management.base import BaseCommand
from time import sleep


class Command(BaseCommand):
    help = 'Updates ITAX_OTHER_RETURN_UNFILED_MONTHLY table every 10 seconds'

    def handle(self, *args, **options):
        while True:
            update_unfiled_monthly_status_periodic.delay_on_commit("st", 2 * 2 * 2)
            print("Task 01 executed!")
            self.stdout.write(self.style.SUCCESS('Successfully performed weekly task'))
            sleep(2 * 2 * 2)