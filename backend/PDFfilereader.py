import PyPDF2

class PdfFilereader():
    def __init__(self):
        self.pdf_file = None


    def set_pdf(self, pdf_path):
        self.pdf_file = open(pdf_path, 'rb')
        self.pdf_reader = PyPDF2.PdfReader(self.pdf_file)


    def PDFread(self):
        all_text = ""
        for page_num in range(len(self.pdf_reader.pages)):
            page = self.pdf_reader.pages[page_num]
            text = page.extract_text()
            all_text += text + "\n"
        return all_text
    


#instance of Filereader
reader = PdfFilereader()

#Set the PDF file path
reader.set_pdf(r"")#file insertion

# Read and print the PDF contents
pdf_contents = reader.PDFread()
print(pdf_contents)


def split_text_into_chunks(text, chunk_size):
    # Split the text into chunks of the specified size
    chunks = [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]
    return chunks

#usage
text = pdf_contents
chunk_size = 4000 #chunk size
chunks = split_text_into_chunks(text, chunk_size)
for chunk in chunks:
    print(chunk)