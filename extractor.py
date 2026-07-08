from pypdf import PdfReader

def extract_text(file):
    """
    Extracts text from a PDF file.
    """
    reader = PdfReader(file)
    text = ""
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"
    return text 

if __name__ == "__main__":
    result = extract_text("Kartik_Sawant_Resume.pdf")
    print(result)