from rest_framework import status
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import render 
import os
import uuid

from .serializers import *
    

def htmlview(request): 
    return render(request, "custom_multiple_file_input.html")


def save_uploaded_return_attachment_files(uploaded_files, file_paths_list, instance):
            
    for file_path in instance.attachment:
        if os.path.exists(file_path):
            os.remove(file_path)
            print(f"File {file_path} deleted successfully")
        else:
            print(f"File {file_path} does not exist")

    allowed_extensions = ['.pdf', '.xls', '.xlsx', '.doc', '.docx']
    # Process each uploaded file
    for uploaded_file in uploaded_files:
        # Assuming you want to save each file to a specific location
        # Modify the destination path as per your requirements
        original_filename = uploaded_file.name

        # generate a new filename
        filename, file_extension = os.path.splitext(original_filename)

        if file_extension.lower() in allowed_extensions:
            new_filename = f"{instance.return_master}_{filename}_{str(uuid.uuid4())}{file_extension}"
            destination_path = 'media/attachments/' + new_filename

            # Save the uploaded file
            with open(destination_path, 'wb') as destination:
                for chunk in uploaded_file.chunks():
                    destination.write(chunk)

            file_paths_list.append(destination_path)
    return file_paths_list


class MultipleFileUploadAPIView(APIView):
    parser_classes = (MultiPartParser, FormParser)
    serializer_class = MultipleFileUploadSerializer
    def get_object(self, return_master):
        try:
            return BedNightReturn.objects.filter(return_master=return_master).first()
        except BedNightReturn.DoesNotExist:
            return None

    def get(self, request, *args, **kwargs):
        queryset = BedNightReturn.objects.all()
        serializer = MultipleFileUploadSerializer(queryset, many=True)
        return Response(serializer.data)    

    def put(self, request, *args, **kwargs):
        # Retrieve the object to update based on the provided identifier
        return_master = request.POST['return_master']
        instance = self.get_object(return_master)

        if not instance:
            return Response({'error': f'Return not found'}, status=status.HTTP_404_NOT_FOUND)
        
        uploaded_files = request.FILES.getlist('attachment')

        file_paths_list = []
        if uploaded_files:
            file_paths_list = save_uploaded_return_attachment_files(uploaded_files, file_paths_list, instance)
            
        data_to_save = {"return_master": return_master, "attachment": file_paths_list}
        # Deserialize the request data
        serializer = MultipleFileUploadSerializer(instance, data_to_save)
        
        # Validate and save the data
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def post(self, request, *args, **kwargs):
        return_master = request.POST['return_master']
        uploaded_files = request.FILES.getlist('attachment')

        file_paths_list = []
        if uploaded_files:
            file_paths_list = save_uploaded_return_attachment_files(uploaded_files, file_paths_list, return_master)
 
        data_to_save = {"number_of_facility": 4, "return_master": return_master, "attachment": file_paths_list}
        serializer = self.serializer_class(data=data_to_save)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

# class FileUploadAPIView(APIView):
#     parser_classes = (MultiPartParser, FormParser)
#     serializer_class = FileUploadSerializer
    
#     def post(self, request, *args, **kwargs):
#         serializer = self.serializer_class(data=request.data)
#         if serializer.is_valid():
#             uploaded_file = serializer.validated_data["file"]
#             serializer.save()
#             return Response(
#                 serializer.data,
#                 status=status.HTTP_201_CREATED
#             )
        
#         return Response(
#             serializer.errors,
#             status=status.HTTP_400_BAD_REQUEST
#         )


