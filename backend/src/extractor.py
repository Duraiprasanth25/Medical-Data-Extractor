from pdf2image import convert_from_path

import pytesseract
import util
import json

from parser_prescription import PrescriptionParser
from parser_patient_details import PatientDetailsParser

POPPLER_PATH = r'C:\poppler-24.02.0\Library\bin'
pytesseract.pytesseract.tesseract_cmd=r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def extract (file_path, file_format):
    #step 1 - extracting text frm pdf file
    pages = convert_from_path(file_path, poppler_path = POPPLER_PATH)
    document_text = ''

    if len(pages)>0:
        page = pages[0]
        processed_image = util.preprocess_image(page)
        text = pytesseract.image_to_string(processed_image, lang='eng')
        document_text = document_text + '\n' + text

    #step 2: extract fields from text
    if file_format == "prescription":
        extracted_data = PrescriptionParser(document_text).parse()

    elif file_format == "patient_details":
        extracted_data = PatientDetailsParser(document_text).parse()

    else:
        raise exception (f"Invalid document format: {file_format}")

    return extracted_data

if __name__ == '__main__':
    data1 = extract('../resources/prescription/pre_2.pdf', 'prescription'),
    data2 = extract('../resources/patient_details/pd_2.pdf', 'patient_details')

    print(json.dumps(data1))
    print(data2)