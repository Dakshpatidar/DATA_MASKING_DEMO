from pypdf import PdfReader


# =====================================================
# SIMPLE PDF TEXT EXTRACTION
# =====================================================

def process_document(file):

    pdf_reader = PdfReader(file)

    text = ""

    for page in pdf_reader.pages:

        extracted = page.extract_text()

        if extracted:

            text += extracted + "\n"

    return text


# =====================================================
# SIMPLE CONTEXT RETRIEVAL
# =====================================================

def retrieve_relevant_context(user_query, document_text):

    if not document_text:

        return "No document uploaded yet."

    return document_text[:3000]