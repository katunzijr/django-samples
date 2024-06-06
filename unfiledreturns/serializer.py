from rest_framework import serializers
from .models import *
from django.db import IntegrityError


class UnfiledReturnAnnuallySerializer(serializers.ModelSerializer):
    class Meta:
        model = UnfiledReturnAnnually
        fields = '__all__'


class UnfiledReturnMonthlySerializer(serializers.ModelSerializer):
    UNFILED_ANNUALLY = UnfiledReturnAnnuallySerializer(read_only=True)
    class Meta:
        model = UnfiledReturnMonthly
        fields = '__all__'
        extra_kwargs = {
            'DUEDATE': {'read_only': True}
        }

    def create(self, validated_data):
        taxpayer_id = validated_data['TAXPAYER_ID']
        category_id = validated_data['CATEGORY_ID']
        current_year = validated_data['YEAR']

        months = range(int(validated_data['MONTH']), 13)
        
        for month in months:
            duedate = OtherReturnDuedate.objects.filter(
                CATEGORY_ID = category_id,
                # YEAR = current_year,
                YEAR = 2023,
                MONTH = month,
            )
            print(duedate)
            if not duedate:
                print(f"DB Error 004: Due date for Category number {category_id} not available!")
                return validated_data
            try:
                unfiled_annually = UnfiledReturnAnnually.objects.create(
                    TAXPAYER_ID = taxpayer_id,
                    CATEGORY_ID = category_id,
                    YEAR = 2023,
                )

                if int(category_id) == 115 or int(category_id) == 140:
                    for date in duedate:
                        try:
                            UnfiledReturnMonthly.objects.create(
                                UNFILED_ANNUALLY = unfiled_annually,
                                MONTH = month,
                                DUEDATE = date.DUEDATE,
                                **validated_data,
                            )
                        except IntegrityError:
                            unfiled_annually.delete()
                            print(f'DB Error 003: Record exist for Tin {taxpayer_id}, Year {current_year}, Category {category_id} and DueDate {date["DUEDATE"]} !!')

                else:
                    try:
                        UnfiledReturnMonthly.objects.create(
                            UNFILED_ANNUALLY=unfiled_annually,
                            MONTH = month,
                            DUEDATE = duedate[0].DUEDATE,
                            **validated_data,
                        )
                    except IntegrityError:
                        unfiled_annually.delete()
                        print(f'DB Error 002: Record exist for Tin {taxpayer_id}, Year {current_year}, Category {category_id} and DueDate {date["DUEDATE"]} !!')

            except IntegrityError:
                print(f'DB Error 001: Record exist for Tin {taxpayer_id}, Year {current_year} and Category {category_id} !!')

            return validated_data
        return validated_data
