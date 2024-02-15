import PyPDF2

# Costante per la conversione da pixel a pollici (72 punti per pollice)
PIXELS_PER_INCH = 1 / 72

# Costante per la conversione da pixel a centimetri (28.35 punti per centimetro)
PIXELS_PER_CM = 1 / 28.35

def get_pdf_page_dimensions(pdf_file_path):
    with open(pdf_file_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        num_pages = len(reader.pages)
        dimensions = []
        for page_num in range(num_pages):
            page = reader.pages[page_num]
            dimensions.append((page.mediabox.width,page.mediabox.height))

        return dimensions

def main():
    pdf_file_path = 'data/red.pdf'  # Inserisci il percorso del tuo file PDF
    page_dimensions = get_pdf_page_dimensions(pdf_file_path)
    for i, dimension in enumerate(page_dimensions, start=1):
        print(f"Dimensioni pagina {i}: larghezza={dimension[0]}, altezza={dimension[1]}")

if __name__ == "__main__":
    main()
