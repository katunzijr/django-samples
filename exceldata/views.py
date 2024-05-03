from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.shortcuts import render
from django.http import HttpResponseBadRequest
from django.core.files.storage import default_storage
from django.core.exceptions import ValidationError
from django.db import connection
import pandas as pd
from .models import LiableToFileReturn
from rest_framework.parsers import FormParser, MultiPartParser
from datetime import date
import os
import uuid


def read_excel_file(uploaded_file):
    filename = default_storage.save('temp/' + uploaded_file.name, uploaded_file)
    filepath = default_storage.path(filename)
    df = pd.read_excel(filepath)
    return df

# class ExcelFileUpload(APIView):
#     parser_classes = (MultiPartParser, FormParser)
#     # serializer_class = LiableToFileReturn1Serializer

#     def post(self, request):

#         uploaded_file = request.FILES['file']
#         filename, file_extension = os.path.splitext(uploaded_file.name)
#         file_extension = file_extension.lower()

#         invalid_data = []
#         unsaved_data = []
#         saved_data = []
#         extracted_data = {}

#         if file_extension == '.xlsx' or file_extension == '.xls':
#             # df = read_excel_file(uploaded_file)
#             df = pd.read_excel(uploaded_file).dropna(how='all')
#         elif file_extension == '.csv':
#             df = pd.read_csv(uploaded_file).dropna(how='all')
#         else:
#             return Response(
#                     data={"error": f'Only Excel Files (.xls or .xlsx or .csv) are allowed!'}, 
#                     status=status.HTTP_400_BAD_REQUEST
#                 )

#         try:
#             desired_columns = ['TIN', 'CATEGORY_ID', 'MONTH']
#             filtered_df = df[desired_columns]
            
#             column_mapping = {
#                 'TIN': 'TAXPAYER_ID',
#                 'CATEGORY_ID': 'CATEGORY_ID',
#                 'MONTH': 'MONTH',
#             }
#             current_year = date.today().year
#             sys_url = request.build_absolute_uri('/')
#             unsaved_data_path = f'media/excel/unsaved_data_{str(uuid.uuid4())}.xlsx'
#             invalid_data_path = f'media/excel/invalid_data_{str(uuid.uuid4())}.xlsx'
#             i = 0
#             cursor = connection.cursor()

#             for index, row in filtered_df.iterrows():
#                 try:
#                     # Extract data based on column mapping
#                     extracted_data = {column_mapping[col]: row[col] for col in column_mapping}
#                     extracted_data['YEAR'] = current_year

#                     sql = f"INSERT INTO ITAX_OTHER_RETURN_UNFILED_MONTHLY (TAXPAYER_ID, CATEGORY_ID, MONTH, YEAR) VALUES (%s, %s, %s, %s)"

#                     # Save the model instance to the database
#                     try:
#                         cursor.execute(sql, list(extracted_data.values()))
#                         connection.commit()
#                         saved_data.append({
#                             'row_index': index,
#                             'row_data': extracted_data,
#                         })
#                         i += i
#                     except Exception as e:
#                         unsaved_data.append({
#                             'row_index': index,
#                             'row_data': extracted_data,
#                             'db_error': str(e)  # Convert exception to string
#                         })
#                         if os.path.isfile(unsaved_data_path):
#                             existing_unsaved_data = pd.read_excel(unsaved_data_path)
#                         else:
#                             existing_unsaved_data = None
#                         new_unsaved_data = filtered_df.iloc[i].to_frame().T
#                         if existing_unsaved_data is not None:
#                             udf = pd.concat([existing_unsaved_data, new_unsaved_data], ignore_index=False)
#                         else:
#                             udf = new_unsaved_data
#                         udf.to_excel(unsaved_data_path, index=False)
#                         i += i

#                 except (KeyError, ValidationError) as e:
#                     # Handle potential errors (e.g., missing columns, invalid data)
#                     invalid_data.append({
#                         'row_index': index,
#                         'row_data': extracted_data,
#                         'validation_error': str(e)  # Convert exception to string
#                     })
#                     if os.path.isfile():
#                         existing_invalid_data = pd.read_excel(invalid_data_path)
#                     else:
#                         existing_invalid_data = None
#                     new_invalid_data = filtered_df.iloc[i].to_frame().T
#                     if existing_invalid_data is not None:
#                         idf = pd.concat([existing_invalid_data, new_invalid_data], ignore_index=True)
#                     else:
#                         idf = new_invalid_data
#                     idf.to_excel(invalid_data_path, index=False)
#                     i += i

#             return Response(
#                 data={
#                     "saved": {
#                         "count": len(saved_data),
#                         "data": saved_data,
#                     },
#                     "unsaved": {
#                         "count": len(unsaved_data),
#                         "data": unsaved_data,
#                         "excel_path": sys_url+unsaved_data_path if unsaved_data else "",
#                     },
#                     "invalid": {
#                         "count": len(invalid_data),
#                         "data": invalid_data,
#                         "excel_path": sys_url+invalid_data_path if invalid_data else "",
#                     },
#                 },
#                 status=status.HTTP_200_OK
#             )
        
#         except Exception as e:
#             return Response(
#                 data={"error": f'Error processing {uploaded_file.name} file: {e}'}, 
#                 status=status.HTTP_400_BAD_REQUEST
#             )


class ExcelFileUpload(APIView):
    parser_classes = (MultiPartParser, FormParser)
    # serializer_class = LiableToFileReturn1Serializer

    def post(self, request):

        uploaded_file = request.FILES['file']
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
                    new_model_instance = LiableToFileReturn(YEAR=current_year, **extracted_data)

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

