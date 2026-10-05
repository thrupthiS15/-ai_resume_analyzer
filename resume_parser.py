import docx
from pypdf import PdfReader

def extract_text_from_pdf(file) -> str:
    text = ""
    try:
        reader = PdfReader(file)
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + " "
    except Exception as e:
        print(f"Error parsing PDF: {e}")
    return text

def extract_text_from_docx(file) -> str:
    text = ""
    try:
        doc = docx.Document(file)
        for para in doc.paragraphs:
            if para.text:
                text += para.text + "\n"
    except Exception as e:
        print(f"Error parsing DOCX: {e}")
    return text
