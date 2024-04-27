from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.shortcuts import render
from django.http import HttpResponseBadRequest
from django import forms
from django.core.files.storage import default_storage
from django.core.exceptions import ValidationError
import pandas as pd
from .models import LiableToFileReturn
from .serializer import LiableToFileReturnSerializer


class UploadFileForm(forms.Form):
    file = forms.FileField()
    return_type = forms.CharField()


def read_excel_file(uploaded_file):
    filename = default_storage.save('temp/' + uploaded_file.name, uploaded_file)
    filepath = default_storage.path(filename)
    df = pd.read_excel(filepath)
    return df

def upload(request):
    form = UploadFileForm(request.POST, request.FILES)
    return render(request, "excel_file_upload.html", {"form": form, })

class ExcelFileUpload(APIView):
    # serializer_class = LiableToFileReturnSerializer

    def post(self, request):
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = form.cleaned_data['file']

            invalid_data = []
            unsaves_data = []
            saves_data = []
            extracted_data = {}

            try:
                desired_columns = ['TIN', 'NAME', 'BUSINESS', 'RETUEN_TYPE']
                # df = read_excel_file(uploaded_file)
                df = pd.read_excel(uploaded_file)
                filtered_df = df[desired_columns]
                
                column_mapping = {
                    'TIN': 'tin',
                    'NAME': 'name',
                    'BUSINESS': 'business',
                    'RETUEN_TYPE': 'return_type',
                }

                for index, row in filtered_df.iterrows():
                    try:
                        # Extract data based on column mapping
                        extracted_data = {column_mapping[col]: row[col] for col in column_mapping}

                        # Create a new model instance and populate fields
                        new_model_instance = LiableToFileReturn(**extracted_data)

                        # Save the model instance to the database
                        try:
                            new_model_instance.save()
                            saves_data.append({
                                'row_index': index,
                                'row_data': extracted_data,
                            })
                        except Exception as e:
                            unsaves_data.append({
                                'row_index': index,
                                'row_data': extracted_data,
                                'db_error': str(e)  # Convert exception to string
                            })

                    except (KeyError, ValidationError) as e:
                        # Handle potential errors (e.g., missing columns, invalid data)
                        invalid_data.append({
                            'row_index': index,
                            'row_data': extracted_data,
                            'validation_error': str(e)  # Convert exception to string
                        })

                return Response(
                    data={"data": {
                        "invalid_data": invalid_data,
                        "saves_data": saves_data,
                        "unsaves_data": unsaves_data
                    }},
                    status=status.HTTP_200_OK
                )
            
            except Exception as e:
                return Response(
                    data={"error": f'Error processing {uploaded_file.name} file: {e}'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )

        else:
            return Response(
                data={"error": "Invalid File Uploaded"}, 
                status=status.HTTP_400_BAD_REQUEST
            )



