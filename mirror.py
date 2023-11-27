import fitz  # PyMuPDF
from PyPDF2 import PdfWriter, PdfReader, Transformation
from PyPDF2.generic import RectangleObject
from PyPDF2._page import PageObject

def create_blank_page(width, height):
    # Crea un oggetto PdfFileWriter
    pdf_writer = PdfWriter()

    # Aggiungi una pagina vuota al writer con le dimensioni specificate
    page = pdf_writer.add_blank_page(width, height)

    return page

def mirrorLR(input_path, output_path):
    # Apri il file PDF con PyMuPDF per ottenere le informazioni sulla dimensione del documento
    pdf_document = fitz.open(input_path)
    page = pdf_document[0]  # Assumiamo che il bleed sia applicato solo alla prima pagina

    # Ottieni le dimensioni originali della pagina
    original_width = page.rect.width
    original_height = page.rect.height

    # Creare un nuovo oggetto PDFWriter
    pdf_writer = PdfWriter()

    # Apri il file PDF con PyPDF2
    pdf_reader = PdfReader(input_path)


        # Per ogni pagina nel documento 
    for page_num in range(len(pdf_reader.pages)):
            # Estrai la pagina
        if page_num%10==0:
            print(page_num,'/',len(pdf_reader.pages))
        pdf_page = pdf_reader.pages[page_num]
        mirror = Transformation((-1,0,0,1,pdf_page.mediabox[2],0))

        new_pdf_page = create_blank_page(original_width, original_height)
        new_pdf_page.merge_page(pdf_page)
        new_pdf_page.add_transformation(mirror)
        pdf_writer.add_page(new_pdf_page)

        if page_num >10:
            break

    # Salva il nuovo documento con il margine di bleed aggiunto
    with open(output_path, 'wb') as output_pdf:
        pdf_writer.write(output_pdf)


def mirrorTD(input_path, output_path):
    # Apri il file PDF con PyMuPDF per ottenere le informazioni sulla dimensione del documento
    pdf_document = fitz.open(input_path)
    page = pdf_document[0]  # Assumiamo che il bleed sia applicato solo alla prima pagina

    # Ottieni le dimensioni originali della pagina
    original_width = page.rect.width
    original_height = page.rect.height

    # Creare un nuovo oggetto PDFWriter
    pdf_writer = PdfWriter()

    # Apri il file PDF con PyPDF2
    pdf_reader = PdfReader(input_path)


        # Per ogni pagina nel documento 
    for page_num in range(len(pdf_reader.pages)):
            # Estrai la pagina
        if page_num%10==0:
            print(page_num,'/',len(pdf_reader.pages))
        pdf_page = pdf_reader.pages[page_num]
        mirror = Transformation((1,0,0,-1,0,pdf_page.mediabox[3]))

        new_pdf_page = create_blank_page(original_width, original_height)
        new_pdf_page.merge_page(pdf_page)
        new_pdf_page.add_transformation(mirror)
        pdf_writer.add_page(new_pdf_page)

        if page_num >10:
            break

    # Salva il nuovo documento con il margine di bleed aggiunto
    with open(output_path, 'wb') as output_pdf:
        pdf_writer.write(output_pdf)

if __name__ == "__main__":
    input_path = "dark.pdf"
    output_path_lr = "dark_out_lr.pdf"
    output_path_td = "dark_out_td.pdf"

    mirrorLR(input_path, output_path_lr)
    mirrorTD(input_path, output_path_td)
