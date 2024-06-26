from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.core.exceptions import ValidationError
from rest_framework.parsers import FormParser, MultiPartParser, JSONParser
from datetime import date
import os
import uuid
import pandas as pd

from .models import *
from .serializer import *
from .services import is_valid_tin


class UnfiledReturnMonthlyAPIView(APIView):
    parser_classes = (MultiPartParser, FormParser, JSONParser)
    serializer_class = UnfiledReturnMonthlySerializer
    def get_object(self, taxpayer_id, category_id, month, year):
        try:
            return UnfiledReturnMonthly.objects.filter(
                TAXPAYER_ID = taxpayer_id, 
                CATEGORY_ID = category_id, 
                MONTH = month,
                YEAR = year,
            ).first()
        except UnfiledReturnMonthly.DoesNotExist:
            return None

    def get(self, request):
        objects = UnfiledReturnMonthly.objects.all()
        serializer = UnfiledReturnMonthlySerializer(objects, many=True)
        return Response(serializer.data)

    def post(self, request):
        uploaded_file = request.data.get("excel_file")

        if uploaded_file:
            filename, file_extension = os.path.splitext(uploaded_file.name)
            file_extension = file_extension.lower()

            invalid_data = []
            unsaved_data = []
            saved_data = []
            extracted_data = {}

            if file_extension == '.xlsx' or file_extension == '.xls':
                # df = read_excel_file(uploaded_file)
                df = pd.read_excel(uploaded_file).dropna(how='all')
            elif file_extension == '.csv':
                df = pd.read_csv(uploaded_file).dropna(how='all')
            else:
                return Response(
                    data={"error": f'Only Excel Files (.xls or .xlsx or .csv) are allowed!'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            try:
                desired_columns = ['TIN', 'CATEGORY_ID', 'MONTH']
                filtered_df = df[desired_columns]
                
                column_mapping = {
                    'TIN': 'TAXPAYER_ID',
                    'CATEGORY_ID': 'CATEGORY_ID',
                    'MONTH': 'MONTH',
                }
                current_year = date.today().year
                sys_url = request.build_absolute_uri('/')
                unsaved_data_path = f'media/excel/unsaved_data_{str(uuid.uuid4())}.xlsx'
                invalid_data_path = f'media/excel/invalid_data_{str(uuid.uuid4())}.xlsx'
                i = 0

                for index, row in filtered_df.iterrows():
                    try:
                        # Extract data based on column mapping
                        extracted_data = {column_mapping[col]: row[col] for col in column_mapping}

                        # Create a new model instance and populate fields
                        new_model_instance = UnfiledReturnMonthly(YEAR=current_year, **extracted_data)

                        # Save the model instance to the database
                        try:
                            new_model_instance.save()
                            saved_data.append({
                                'row_index': index,
                                'row_data': extracted_data,
                            })
                            i += i
                        except Exception as e:
                            unsaved_data.append({
                                'row_index': index,
                                'row_data': extracted_data,
                                'db_error': str(e)  # Convert exception to string
                            })
                            if os.path.isfile(unsaved_data_path):
                                existing_unsaved_data = pd.read_excel(unsaved_data_path)
                            else:
                                existing_unsaved_data = None
                            new_unsaved_data = filtered_df.iloc[i].to_frame().T
                            if existing_unsaved_data is not None:
                                udf = pd.concat([existing_unsaved_data, new_unsaved_data], ignore_index=False)
                            else:
                                udf = new_unsaved_data
                            udf.to_excel(unsaved_data_path, index=False)
                            i += i

                    except (KeyError, ValidationError) as e:
                        # Handle potential errors (e.g., missing columns, invalid data)
                        invalid_data.append({
                            'row_index': index,
                            'row_data': extracted_data,
                            'validation_error': str(e)  # Convert exception to string
                        })
                        if os.path.isfile():
                            existing_invalid_data = pd.read_excel(invalid_data_path)
                        else:
                            existing_invalid_data = None
                        new_invalid_data = filtered_df.iloc[i].to_frame().T
                        if existing_invalid_data is not None:
                            idf = pd.concat([existing_invalid_data, new_invalid_data], ignore_index=True)
                        else:
                            idf = new_invalid_data
                        idf.to_excel(invalid_data_path, index=False)
                        i += i

                return Response(
                    data={
                        "saved": {
                            "count": len(saved_data),
                            "data": saved_data,
                        },
                        "unsaved": {
                            "count": len(unsaved_data),
                            "data": unsaved_data,
                            "excel_path": sys_url+unsaved_data_path if unsaved_data else "",
                        },
                        "invalid": {
                            "count": len(invalid_data),
                            "data": invalid_data,
                            "excel_path": sys_url+invalid_data_path if invalid_data else "",
                        },
                    },
                    status=status.HTTP_200_OK
                )
            
            except Exception as e:
                return Response(
                    data={"error": f'Error processing {uploaded_file.name} file: {e}'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
        else:
            taxpayer_id = request.GET.get("taxpayer_id")
            if not is_valid_tin(taxpayer_id):
                return Response(
                    {'message': f"Not valid TIN: {taxpayer_id}"}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            request_data = {
                'TAXPAYER_ID': taxpayer_id,
                'CATEGORY_ID': request.GET.get("category"),
                'MONTH': request.GET.get("start_month"),
                'YEAR': date.today().year,
            }
            serializer = UnfiledReturnMonthlySerializer(data=request_data)
            
            if serializer.is_valid():
                serializer.save()

                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

    def patch(self, request):
        taxpayer_id = request.data.get('taxpayer_id')
        category_id = request.data.get('category_id')
        month = request.data.get('month')
        year = request.data.get('year')

        instance = self.get_object(taxpayer_id, category_id, month, year)
        if not instance:
            return Response({'error': f'Unfiled return not found!'}, status=status.HTTP_404_NOT_FOUND)
        
        if 'approval_status' in request.data:
            instance.STATUS = request.data.get('approval_status')
        if 'is_visible_to_tp' in request.data:
            instance.IS_VISIBLE_TO_TP = request.data.get('is_visible_to_tp')
        if 'is_filed' in request.data:
            instance.IS_FILLED = request.data.get('is_filed')
        
        try:
            a = instance.save()
            print(a)
            return Response({'message': f'Updated successful'}, status=status.HTTP_202_ACCEPTED)
        except Exception as e:
            return Response({'error': f'{e}'}, status=status.HTTP_400_BAD_REQUEST)
        

