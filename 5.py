import pdfplumber

def textExtract():
    pdf = pdfplumber.open('ex2.pdf')  # Replace with your PDF file path
    text = ""
    # Step 3: Extract text from tables
    for page in pdf.pages:
        tables = page.extract_tables()

        for table in tables:
            for row in table:
                for cell in row:
                    print(cell) 
                    text+=cell
 
    pdf.close()