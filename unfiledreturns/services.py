
import pandas as pd
from django.core.files.storage import default_storage
import re


def read_excel_file(uploaded_file):
    filename = default_storage.save('temp/' + uploaded_file.name, uploaded_file)
    filepath = default_storage.path(filename)
    df = pd.read_excel(filepath)
    return df


def is_valid_tin(tin):
    return bool(re.match(r'^\d{9}$', tin))


