from django.template import Context, Template
import pdfkit
from django.http import HttpResponse
import os
import base64
import json
from io import BytesIO
import pyqrcode


# PDF generation options (customizable)
options = {
    'page-size': 'Letter',
    # 'margin-top': '0.75in',
    # 'margin-right': '0.75in',
    # 'margin-bottom': '0.75in',
    # 'margin-left': '0.75in',
    'encoding': "UTF-8",
}

# File paths (modify as needed)
css_path = 'static/css/form_styles.css'
image_folder = 'static/images/'
template_folder = 'templates/forms/'
form_list_path = 'form_list.json'
context = {}


def generate_qrcode(taxType, taxPayerName, filedBy, declarantTin, tin, dateOfIssue, ReferenceNumber):

    content = f"{taxType} of {taxPayerName} with\n" \
                f"TIN: {tin} filed by {filedBy} with\n" \
                f"TIN: {declarantTin} on {dateOfIssue} with\n" \
                f"reference number {ReferenceNumber}"
    
    # Generate QR code
    qr_code = pyqrcode.create(content)

    # Convert QR code to BytesIO object
    qr_code_buffer = BytesIO()
    qr_code.png(qr_code_buffer, scale=6)

    # Encode the BytesIO object as base64
    return f'data:image/png;base64,{base64.b64encode(qr_code_buffer.getvalue()).decode()}'


def read_json_form_file(form_type, tax_name):
    try:
        with open(form_list_path, "r") as f:
            data = json.load(f)
            filtered_data = [item for item in data[form_type] if item["tax_name"] == tax_name]
            return filtered_data
    except (FileNotFoundError, json.JSONDecodeError) as e:
        raise Exception(f"Error reading JSON file: {form_list_path}. Reason: {e}")


def render_pdf_file(pdf_output_path):
    """
    Renders the generated PDF as an HTTP response for download.

    Returns:
        HttpResponse: An HTTP response with the PDF content and appropriate headers
                       for download.

    Raises:
        HttpResponse: An HTTP response with status code 404 (Not Found) if the PDF
                       file doesn't exist.
    """
    try:
        with open(pdf_output_path, 'rb') as pdf_file:
            res = HttpResponse(pdf_file.read(), content_type='application/pdf')
            res['Content-Disposition'] = 'inline; filename=output_sample.pdf'
            return res
    except FileNotFoundError:
        return HttpResponse(status=404)
  

def get_image_file_as_base64_data(img_name, img_ext):
    """
    Converts an image file to base64 encoded string.

    Args:
        img_name (str): Name of the image file (without extension).
        img_ext (str): Image file extension (e.g., 'png', 'jpeg').

    Returns:
        str: Base64 encoded string representation of the image data.

    Raises:
        Exception: If the image file cannot be opened or read.
    """
    with open(image_folder+img_name+'.'+img_ext, 'rb') as image_file:
        return f'data:image/{img_ext};base64,{base64.b64encode(image_file.read()).decode()}'


def pdf_to_base64(pdf_output_path):
  """Converts a PDF file to base64 encoded string.

  Args:
      filepath: Path to the PDF file.

  Returns:
      A string containing the base64 encoded representation of the PDF file.
      Raises an exception if the file cannot be opened or read.
  """
  try:
    with open(pdf_output_path, "rb") as pdf_file:
      # Read the PDF file content in binary mode
      pdf_data = pdf_file.read()
      # Encode the binary data to base64 string
      base64_string = base64.b64encode(pdf_data).decode("utf-8")
      return base64_string
  except (FileNotFoundError, PermissionError) as e:
    raise Exception(f"Error reading PDF file: {pdf_output_path}. Reason: {e}")


def generate_pdf_form(data, entitytin, form_type, tax_name): 
    """
    Generates a PDF from a JSON data file and a template, returning an HTTP response.

    This function handles the logic for generating a PDF document based on data
    fetched from a JSON file and rendered using a Django template.

    Args:
        request (HttpRequest): The Django HTTP request object (unused in this
                              implementation).

    Returns:
        HttpResponse: An HTTP response object containing the generated PDF
                      data or an error message if there's an issue.
    """

    # Load data from JSON file
    context['general_data'] = read_json_form_file(form_type=form_type, tax_name=tax_name)
    print(context['general_data'])
    context['data'] = data

    # Load image data as base64 encoded strings (for potential use in the template)
    context['qrcode'] = generate_qrcode("Income Tax", "John Doe", "Jane Smith", entitytin, "987654321", "2023-08-15", "123456789098765431")
    context['tra_banner'] = get_image_file_as_base64_data('tra_banner', 'jpeg')
    context['signature'] = get_image_file_as_base64_data('signatures/Signature_Alfred', 'png')

    # Construct the full path to the HTML template file
    html_file_template = os.path.join(template_folder, context['general_data'][0]['html_template_path'])

    # Open the template file and read its contents
    try:
        with open(html_file_template, 'r') as f:
            template_str = Template(f.read())
    except (FileNotFoundError, json.JSONDecodeError) as e:
        raise Exception(f"Error reading HTML file: {html_file_template}. Reason: {e}")
    

    # Render the template with the context data (dictionary)
    html_file_string = template_str.render(Context(context)) 

    # Generate the PDF using pdfkit from the rendered HTML string
    pdfkit.from_string(html_file_string, template_folder+context['general_data'][0]['pdf_output_path'], options=options, css=css_path)
    print('PDF GENERATED SUCCESSFUL!') 

    # Convert the generated PDF to base64 encoded string (for optional use)
    base64_encoded_pdf = pdf_to_base64(template_folder+context['general_data'][0]['pdf_output_path'])

    # Render the generated PDF as a downloadable response
    # response = render_pdf_file(template_folder+context['general_data'][0]['pdf_output_path'])
    
    return base64_encoded_pdf


# generate_pdf_form(data = {}, entitytin = 123456789, form_type="submited", tax_name="Bed Night Levy")